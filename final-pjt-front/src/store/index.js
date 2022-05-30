import Vue from 'vue'
import Vuex from 'vuex'
import movies from './modules/movies'
import accounts from './modules/accounts'
import community from './modules/community'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [
    createPersistedState()
  ],
  modules: {
    movies, accounts, community,
  }
})
