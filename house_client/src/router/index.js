import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import LoginPage from '../pages/loginPage.vue'
import CommunityStat from '../pages/communityStat.vue'
import Home from '../pages/index'

Vue.use(VueResource)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Home,
      meta: {
        title: 'home'
      }
    },
    {
      path: '/loginPage',
      component: LoginPage
    },
    {
      path: '/communityStat',
      name: 'CommunityStat',
      component: CommunityStat
    }
  ]
})
