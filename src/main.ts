import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
// import { VueClass } from '@vue/test-utils'
import './quasar'
import './frameworks'

Vue.config.productionTip = false
// I want to add App to the global space for debugging
declare const window: any // eslint-disable-line @typescript-eslint/no-explicit-any

window.App = new Vue({
  router,
  store,
  render: h => h(App)
})
window.App.$mount('#app')
store.dispatch('checkSesssion')
