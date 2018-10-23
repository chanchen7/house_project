var express = require('express');
var router = express.Router();

var user = require('../modules/user')

const init_token = 'TKCris07o'

/* GET users listing. */
router.post('/login', function (req, res, next){
  if (!req.body.username) {
    res.json({status:1, message:"用户名为空!"})
  }
  if (!req.body.password) {
    res.json({status:1, message:"密码为空!"});
  }
  user.findUserLogin(req.body.username, req.body.password, function (err, userSave) {
    if (userSave.length != 0) {
      res.json({status:0, message:'登陆成功！'});
    }
    else {
      res.json({status:1, message:'用户名或密码错误！'});
    }
  });
});

router.post('/register', function (req, res, next){
  if (!req.body.username) {
    res.json({status:1, message:"用户名为空!"})
  }
  if (!req.body.password) {
    res.json({status:1, message:"密码为空!"});
  }
  user.findByUsername(req.body.username, function (err, userSave) {
    if (userSave.length != 0) {
      res.json({status:1, message:'用户已注册！'});
    }
    else {
      var registerUser = new user({
        username: req.body.username,
        password: req.body.password
      });
      registerUser.save(function() {
        res.json({status:0, message:"注册成功！"});
      });
    }
  });
});

function getMD5Password(id){

}

module.exports = router;
