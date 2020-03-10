import Vue from 'vue'
import VueRouter from 'vue-router'
import Devices from '@/views/Devices.vue'
import Login from '@/views/Login.vue'
import $store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    beforeEnter: (to, from, next) => {
      setTimeout(() => {
        if ($store.state.user.loggedIn) {
          next({ name: 'Devices' })
        } else {
          next()
        }
      }, 0)
    },
    component: Login
  },
  {
    path: '/devices',
    name: 'Devices',
    beforeEnter: (to, from, next) => {
      setTimeout(() => {
        if ($store.state.user.loggedIn) {
          next()
        } else {
          next({ name: 'Login' })
        }
      }, 0)
    },
    component: Devices
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
