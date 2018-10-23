var mongoose = require('mongoose');
mongoose.connect('mongodb://127.0.0.1:27017/house_db');
Promise = require('bluebird');
mongoose.Promise = Promise;

module.exports = mongoose