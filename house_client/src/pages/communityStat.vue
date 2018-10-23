<template lang="html">
    <div class="box">
        <div id="myChart" :style="{width: '1200px', height: '300px'}"></div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            msg: 'Welcome to Your Vue.js App' + this.$route.params.communityId
        }
    },
    mounted(){
        this.drawLine();
    },
    methods:{
        drawLine(){
            var moment = require('moment')
            var currentdate = moment().format('YYYYMMDD');
            this.$http.post('http://139.199.223.208:80/apis/showAvgPriceStatByCommunity', {communityId: this.$route.params.communityId, date: currentdate}).then((data) => {
                if (data.body.status == 1){
                    alert(data.body.message)
                }
                else {
                    var dates = [];
                    var prices = [];
                    data.body.data.forEach(function(item){
                        dates.push(item.date);
                        prices.push(parseInt(item.avg_price));
                    });
                    let myChart = this.$echarts.init(document.getElementById('myChart'));
                    myChart.setOption({
                        title: {text: this.$route.params.community + " 30日均"},
                        tooltip: {},
                        xAxis: {
                            data: dates
                        },
                        yAxis:{},
                        series:[{
                            name: '小区均价',
                            type: 'line',
                            data:prices
                        }]
                    });
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
