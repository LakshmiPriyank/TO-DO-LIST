const TaskToDo = artifacts.require("TaskToDo");

module.exports = function (deployer) {
    deployer.deploy(TaskToDo);
};
