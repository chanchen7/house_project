<template lang="html">
    <el-container>
        <el-header>
        <div class="block" align="left">
            <span class="demonstration"></span>
            <el-date-picker
                v-model="value1"
                type="daterange"
                unlink-panels
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                :picker-options="pickerOptions"
                @change="onChange">
            </el-date-picker>
        </div>
        </el-header>
        <el-main>
         <div id="myChart" :style="{width: '1200px', height: '600px'}">
         </div>
        </el-main>
    </el-container>
</template>

<script>
export default {
    data() {
      return {
        pickerOptions: {
          shortcuts: [{
            text: '最近7天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近30天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近90天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit('pick', [start, end]);
            }
          }],
          disabledDate(picker) {
            return picker.getTime() > Date.now() - 8.64e6
          }
        },
        value1: [(new Date()).getTime() - 3600 * 1000 * 24 * 30 , new Date()]
      };
    },
    mounted(){
      this.drawLine();
    },
    methods:{
        drawLine(){
            const loading = this.$loading({
              lock: true,
              text: 'Loading',
              spinner: 'el-icon-loading',
              background: 'rgba(255, 255, 255, 0.7)',
              target: document.getElementById('myChart')
            });

            var moment = require('moment');
            var days;
            var currentdate;
            var startDate;
            if(this.value1 == "" || this.value1 == null || this.value1 == undefined){ // "",null,undefined
                days = 30;
                currentdate = moment().format('YYYYMMDD');
                startDate = moment().subtract(30, "days").format(YYYYMMDD);
            }
            else{
                days = (moment(this.value1[1]) - moment(this.value1[0])) / (3600*24*1000);
                startDate = moment(this.value1[0]).format('YYYYMMDD')
                currentdate = moment(this.value1[1]).format('YYYYMMDD');
            }
            
            //this.$http.post('http://139.199.223.208:80/apis/showAvgPriceStatByCommunity', {communityId: this.$route.params.communityId, date: currentdate, days: days}).then((data) => {
            this.$http.post('http://127.0.0.1:80/apis/showPeriodAvgPriceStatByCommunity', {communityId: this.$route.params.communityId, startdate: startDate, enddate: currentdate}).then((data) => {
                loading.close();
                if (data.body.status == 1){
                    alert(data.body.message)
                }

                else {
                    var dates = [];
                    var prices = [];
                    var prev_price = 0;
                    data.body.data.forEach(function(item){
                        dates.push(item.date);
                        var avg_price = parseInt(item.avg_price)
                        if (avg_price == 0){
                          avg_price = prev_price;
                        }
                        prices.push(avg_price);
                        prev_price = avg_price;
                    });
                    let myChart = this.$echarts.init(document.getElementById('myChart'));
                    myChart.setOption({
                        title: {text: this.$route.params.community + " " + days + " 日均" },
                        toolbox: {
                          show:true,
                          orient: 'horizontal',
                          showTitle: true,
                          feature:{
                            magicType: {
                              type: ['line', 'bar']
                            },
                            dataView:{
                              show: true,
                              title:'数据视图',
                              lang: [this.$route.params.community],
                              readOnly:false,
                              optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var tdHeaders = '<td>时间</td>'; //表头
                                var tdBodys = ''; //表数据
                                series.forEach(function(item) {
                                    tdHeaders += '<td>' + item.name + '</td>'; //组装表头
                                });
                                var table = '<table border="1" align="center" style="width:50%;text-align:center" ><tr>' + tdHeaders + ' </tr>';
                                var days = 0;
                                var month = "";
                                var price_sum = 0;
                                var startDay = axisData[0];
                                var endDay = "";
                                //组装表数据
                                for (var i = 0, l = axisData.length; i<l; i++){
                                  var day = axisData[i].substring(axisData[i].length - 2);
                                  var temp = series[0].data[i];
                                  if (i == l-1) {
                                    days += 1;
                                    price_sum += temp;
                                    var endDay = axisData[i];
                                    tdBodys = '<td>' + (price_sum / days).toFixed(2) + '</td>';
                                    table += '<tr><td style="padding: 10 10px">' + startDay + '-' + endDay + '</td>' + tdBodys + '</tr>';
                                    break;
                                  } else if (day == '01' || day == '16') {
                                    tdBodys = '<td>' + (price_sum / days).toFixed(2) + '</td>';
                                    table += '<tr><td style="padding: 10 10px">' + startDay + '-' + endDay + '</td>' + tdBodys + '</tr>';
                                    startDay = axisData[i];
                                    price_sum = 0;
                                    days = 0;
                                  }
                                  days += 1;
                                  price_sum += temp;
                                  endDay = axisData[i];
                                }
                                table += '</table>';                                  
                                return table;
                              }
                            },
                            saveAsImage:{
                              type:'png',
                              show:true,
                              title:'保存为图片',
                            },

                            restore:{show:true}
                          }
                        },
                        xAxis: {
                            data: dates
                        },
                        yAxis:{
                          scale:true
                        },
                        series:[{
                            name: '小区均价',
                            type: 'line',
                            data:prices
                        }]
                    });
                }
            });
        },
        onChange(){
            this.drawLine();
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
