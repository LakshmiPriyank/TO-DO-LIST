import json
from web3 import Web3, HTTPProvider
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Connect to the blockchain
blockchain = 'http://127.0.0.1:7545'

def connect():
    web3 = Web3(HTTPProvider(blockchain))
    web3.eth.defaultAccount = web3.eth.accounts[0]

    # Load the contract ABI and address
    artifact = "../build/contracts/TaskToDo.json"
    with open(artifact) as f:
        artifact_json = json.load(f)
        contract_abi = artifact_json['abi']
        contract_address = artifact_json['networks']['5777']['address']
    
    contract = web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    return web3, contract

@app.route('/tasks', methods=['GET'])
def get_tasks():
    web3, contract = connect()
    tasks = contract.functions.getAllTasks().call()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    web3, contract = connect()
    description = request.json['desc']
    
    # Prepare transaction to add a task
    tx_hash = contract.functions.addTask(description).transact({'from': web3.eth.defaultAccount})
    web3.eth.waitForTransactionReceipt(tx_hash)
    
    return jsonify({'status': 'Task added'})

@app.route('/tasks/finish/<int:id>', methods=['POST'])
def finish_task(id):
    web3, contract = connect()
    
    # Prepare transaction to mark task as finished
    tx_hash = contract.functions.markAsFinished(id).transact({'from': web3.eth.defaultAccount})
    web3.eth.waitForTransactionReceipt(tx_hash)
    
    return jsonify({'status': 'Task marked as finished'})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
