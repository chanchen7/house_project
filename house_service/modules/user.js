var mongoose = require('../common/db');

var user = new mongoose.Schema({
    username: String,
    password: String
})

// 查找用户
user.statics.findAll = function(callBack){
    this.find({}, callBack);
};

user.statics.findByUsername = function(name, callBack){
    this.find({username : name}, callBack);
};

user.statics.findUserLogin = function(name, password, callBack){
    this.find({username:name, password:password}, callBack);
};

var userModel = mongoose.model('user', user);
module.exports = userModel;