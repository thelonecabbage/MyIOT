import Vue from 'vue'
import VueTimeago, { converter as timeagoConverter } from 'vue-timeago'
import VueApexCharts from 'vue-apexcharts'

Vue.use(VueTimeago, {
  name: 'Timeago', // Component name, `Timeago` by default
  locale: 'en', // Default locale
  // We use `date-fns` under the hood
  // So you can use all locales from it
  locales: {
    // 'zh-CN': require('date-fns/locale/zh_cn'),
    // ja: require('date-fns/locale/ja')
  }
})

Vue.filter('timeago', function (datetime) {
  return timeagoConverter(datetime, 'en', { includeSeconds: false })
})

Vue.component('apexchart', VueApexCharts)
