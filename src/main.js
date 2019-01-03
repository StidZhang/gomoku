import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false

Vue.use(Antd)

Vue.use(new VueSocketIO({
  debug: true,
  // TODO: Need to examine the connection string
  connection: 'http://' + document.domain + ':' + location.port,
  vuex: {
    store,
    actionPrefix: 'SOCKET_',
    mutationPRefix: 'SOCKET_'
  }
}))

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
