import Vue from 'vue'
import App from './App.vue'
import Axios from 'axios'
import iView from 'iview'
import VueHighlightJS from './hld'
import 'iview/dist/styles/iview.css'

Vue.prototype.$axios = Axios.create()

Vue.use(iView);
Vue.use(VueHighlightJS)

new Vue({
    el: '#app',
    render: h => h(App)
})