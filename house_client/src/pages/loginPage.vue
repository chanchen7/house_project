<template>
    <div>
        <div class="box"> 
            <div style="width: 15%;padding-top: 5%">
                <label>LOGIN</label>
                <div>
                    <i-input type="text" v-model="username" placeholder="用户名">
                        <Icon type="ios-person" slot="prepend"/>
                    </i-input>
                </div>
                <div class="box">
                    <i-input type="text" v-model="password" placeholder="密码">
                        <Icon type="ios-lock" slot="prepend"></Icon>
                    </i-input>
                </div>
            </div>
        </div>
        <div class="box">
            <i-button type="primary" v-on:click="userLogin">登录</i-button>
            <i-button type="text" style="margin-left: 10px" v-on:click="userRegister">注册</i-button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        userLogin: function (event) {
            this.$http.post('http://localhost:80/users/login', { username: this.username, password: this.password }).then((data) => {
                if (data.body.status == 1){
                    alert(data.body.message)
                }
                else {
                    this.$router.go(-1)
                }
            })
        },
        userRegister: function(event) {
            this.$router.push( {path: 'register'} )
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
</style>

