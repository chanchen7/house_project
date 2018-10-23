var mongoose = require('../common/db')

var housePrice = new mongoose.Schema({
    house_id: String,
    capture_time: String,
    unit_price: String,
    total_price: String,
    follow_total: String,
    view_total: String,
    community: String,
    community_id: String
});

// 当天是否有数据采集
function hasData(date){
    return new Promise(function (resolve, reject){
        housePriceModel.aggregate([{$match : {capture_time:eval('/^'+date+'/')}}, {$limit: 1}], function(err, hasData) {
            if (err) {
                reject(err);
            }
            resolve(hasData.length > 0);
        });
    });
}

// 当日小区数据
function getCurrentDateHouses(communityId, date) {
    return new Promise(function(resolve, reject){
        housePriceModel.aggregate([{$match : {community_id:communityId, capture_time:eval('/^'+date+'/')}}], function(err, getCurrentDateHouses){
            if (err) {
                reject(err);
            }

            resolve(getCurrentDateHouses);
        });
    });
}

// 最近有数据的日期
function getNearDate(communityId, date){
    return new Promise(function(resolve, reject){
        housePriceModel.aggregate(
            [
                {$match : {community_id:communityId, capture_time:{$lt:date}}}, 
                {$sort : {capture_time : -1}}, 
                {$limit:1}
            ], function(err, firsthouse){
                if (err) {
                    reject(err);
                }
                if (firsthouse.length === 0){
                    date = '19700101';
                }
                else{
                    date = firsthouse[0].capture_time.slice(0,8);
                }
                resolve(date);
        });
    });
}

function calcAvgPrice(houseInfos, communityId, date){
    var total = 0;
    houseInfos.forEach(item => {
        total += parseInt(item.unit_price);
    });
    var data = {
        community_id:communityId, 
        avg_price:total === 0 ? '0' : parseInt(total / houseInfos.length).toString(), 
        all_count:houseInfos.length,
        date: date
    };
    return data;
}

// 查找小区指定日期报价
housePrice.statics.getAvgPriceByCommunityId = function(communityId, date){
    return getCurrentDateHouses(communityId, date).then(function(getHouses){
        if (getHouses.length > 0){
            // 计算平均值
            return calcAvgPrice(getHouses, communityId, date);
        }
        else
        {
            return hasData(date).then(function(isTrue){
                if (isTrue){
                    // 当日有数据爬取
                    return calcAvgPrice([], communityId, date);
                }
                else {
                    // 无爬取
                    return getNearDate(communityId, date).then(function(nearDate){
                        return getCurrentDateHouses(communityId, nearDate).then(function(nearHouses){
                            return calcAvgPrice(nearHouses, communityId, date);
                        });
                    });
                }
                
            });
        }
    }).catch(function(err){
        //
    });
}
    
    
            /*else{
                // 找最近的有数据的日期
                new Promise(function (resolve, reject){
                    housePriceModel.aggregate([{$match : {community_id:communityId, capture_time:{$lt:date}}}, {$sort : {capture_time : -1}}, {$limit:1}], function(err, firsthouse){
                        if (err) {
                            reject(err);
                        }
                        if (firsthouse.length === 0)
                        {
                            var data = {community_id:communityId, avg_price:'0', all_count:0};
                            resolve(data);
                        }
                        date = firsthouse[0].capture_time.slice(0,8);
                        housePriceModel.aggregate([{$match : {community_id:communityId, capture_time:eval('/^'+date+'/')}}], function(err, getCurrentDateHouses){
                            if (err) {
                                reject(err);
                            }
                
                            if (getCurrentDateHouses.length > 0){
                                // 数据存在
                                var total = 0;
                                getCurrentDateHouses.forEach(item => {
                                    total += parseInt(item.unit_price);
                                });
                                var data = {community_id:communityId, avg_price:parseInt(total / getCurrentDateHouses.length).toString(), all_count:getCurrentDateHouses.length};
                                resolve(data);
                            };
                        });
                }) 
                });
            }
        });
    });
};*/

var housePriceModel = mongoose.model('housePrice', housePrice, 'house_price_item_set');
module.exports = housePriceModel;