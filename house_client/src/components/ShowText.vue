<template>
    <div id="">
        <p>
            提问：
            <input v-model="question">
        </p>
        <p>{{ answer}}</p>
    </div>
</template>

<script>
export default {
    data(){
        return {
            question:'',
            answer:'还没有问呢~'
        }
    },
    watch: {
        question: function() {
            this.answer = '等待发问~~'
            this.getAnswer()
        }
    },
    methods: {
        getAnswer: function () {
            if (this.question.indexOf('?') !== -1 || this.question.indexOf('？') !== -1) {
                this.answer = '思考中······'
                let that = this
                that.$http.post('http://robottest.uneedzf.com/api/talk2Robot', 
                { token: '97d431cd675e82740b8c0720d3ef5693', message: that.question}).then(function (res) {
                    if (res.data.code === 0) {
                        that.answer = res.data.data
                    }
                    else {
                        that.answer = res.data.message
                    }     
                })
            }
            else {
                this.answer = '提问需要?结尾~'
                return 0
            }
        }
    }
}
</script>

