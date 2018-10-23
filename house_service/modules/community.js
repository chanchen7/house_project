var mongoose = require('../common/db')

var community = new mongoose.Schema({
    community_id: String,
    community: String,
    build_year: String,
    total_households: String,
    house_property: String,
    developer: String,
    property_fee: String
})


// 查找
community.statics.findByCommunityName = function(communityName){
    var query = {};
    query['community'] = new RegExp(communityName);

    return new Promise(function (resolve, reject) {
        communityModel.find(query, function (err, getCommunities) {
            if (err){
                return reject(err);
            }
            resolve(getCommunities);
        });
    });
};

var communityModel = mongoose.model('community', community, 'community_item_set');
module.exports = communityModel;