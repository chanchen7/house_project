<template lang="html">
    <div>
        <div class="box"> 
            <div style="width: 50%;padding-top: 5%">
                <label>Search</label>
                <div class="searchItem">
                    <Input type="text" v-model="query" @keyup.enter.native="searchCommunity">
                        <Button slot="append" icon="ios-search" v-on:click="searchCommunity"></Button>
                    </Input>
                </div>
            </div>
        </div>
        <div style="margin:5%">
            <ul>
                <Card v-for="(item,index) in communityList" :key="index">
                    <p slot="title">{{item.community}}</p>
                    <p>建筑年代：{{item.build_year}}, 开发商：{{item.developer}}</p>
                    <p>物业公司：{{item.house_property}}, 物业费：{{item.property_fee}}</p>
                    <p>均价：{{item.avg_price}}, 挂牌数目：{{item.count}}</p>
                    <p>日期: {{item.date}}</p>
                    <i-button type="primary" shape="circle" v-on:click="statByDay(item)" icon="md-stats"></i-button>
                </Card>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            query: '',
            communityList:[]
        }
    },
    methods: {
        searchCommunity: function(event) {
            var moment = require('moment')
            var currentdate = moment().format('YYYYMMDD');
            this.$http.post('http://139.199.223.208:80/apis/showAvgPriceByCommunity', { community: this.query, date: currentdate}).then((data) => {
                if (data.body.status == 1){
                    alert(data.body.message)
                }
                else {
                    this.communityList=data.body.data
                }
            });
        },
        statByDay: function(item) {
            // 切路由
            this.$router.push({
                name: 'CommunityStat',
                params: {
                    communityId: item.community_id,
                    community: item.community
                    }
                });
        }
    }
}
</script>

<style>
    .box{
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 10px;
    }
    .searchItem{
        display: flex
    }
</style>
