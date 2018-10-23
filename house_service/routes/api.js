var express = require('express');
var router = express.Router();

var community = require('../modules/community')
var housePrice = require('../modules/housePrice')

router.post('/showCommunity', function (req, res, next){
    if (!req.body.community) {
      res.json({status:1, message:"检索条件为空!"})
    }
    else {
      community.findByCommunityName(req.body.community, function (err, getCommunity) {
        res.json( {status: 0, message: "获取成功", data: getCommunity})
      });
    }
  });

  router.post('/showAvgPriceByCommunity', function(req, res, next){
    if (!req.body.community) {
      res.json({status:1, message:"检索条件为空!"})
    }
    else if (!req.body.date)
    {
      res.json({status:1, message:"检索时间为空!"})
    }
    else {
      let communities = [];
      community.findByCommunityName(req.body.community).then(function(getCommunities){
        communities = getCommunities;
        return Promise.all(getCommunities.map(function(community){
            return housePrice.getAvgPriceByCommunityId(community.community_id, req.body.date);
        }));
      }).then(function(communityPrices){
        communities.forEach(function(item){
          for(var i = 0; i < communityPrices.length; ++i){
            if (item.community_id === communityPrices[i].community_id){
              item._doc.avg_price = communityPrices[i].avg_price;
              item._doc.count = communityPrices[i].all_count;
              item._doc.date = req.body.date;
              break;
            }
          }
        })
        res.json({status:0, message:"获取成功!", data:communities});
      }).catch(function(err){
        res.json({status:1, message:err});
      });
    }
  });

  router.post('/showAvgPriceStatByCommunity', function (req, res, next){
    if (!req.body.communityId) {
      res.json({status:1, message:"小区为空!"})
    }
    else if (!req.body.date)
    {
      res.json({status:1, message:"检索时间为空!"})
    }
    else {
      var moment = require('moment')
      dates = [];
      for(var i = 29; i >= 0; i--){
        dates.push(moment(req.body.date, 'YYYYMMDD').subtract(i, 'days').format('YYYYMMDD'));
      }
      return Promise.all(dates.map(function(date){
        return housePrice.getAvgPriceByCommunityId(req.body.communityId, date)
      })).then(function(datas){
        datas.sort(function(x, y){
          if (x.date < y.date) {
            return -1;
          } else if (x.date > y.date) {
            return 1;
          } else {
            return 0;
          }
        });
        res.json({status:0, message:"获取成功!", data: datas});
      }).catch(function(err){
          res.json({status:1, message:err});
      });
    }
  });

  module.exports = router;