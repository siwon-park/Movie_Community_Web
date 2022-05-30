import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from './plugins/vuetify'
import GAuth from 'vue-google-oauth2'

const gauthOption = {
  clientId: '66082360069-u7qtlkb0ftv8jo9bd05ucef7geosofih.apps.googleusercontent.com',
  scope: 'profile email https://www.googleapis.com/auth/plus.login',
  prompt: 'select_account'
}

Vue.use(GAuth, gauthOption)

Vue.config.productionTip = false

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
