import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import 'iview/dist/styles/iview.css'
import 'iview/dist/iview.min.js'
import qs from 'qs'

Vue.prototype.$axios = axios
Vue.prototype.$qs = qs

const iView = require('iview')
Vue.config.productionTip = false

Vue.use(iView)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
