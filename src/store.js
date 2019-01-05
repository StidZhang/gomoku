import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: "",
    gid: ""
  },
  mutations: {
    setUsername(state, username) {
      state.username = username
    },
    resetUsername(state) {
      state.username = ""
    },
    setGid(state, gid) {
      state.gid = gid
    },
    resetGid(state) {
      state.gid = ""
    }
  },
  actions: {
    setUsername({ commit }, username) {
      commit('setUsername', username)
    },
    resetUsername({ commit }) {
      commit('resetUsername')
    },
    setGid({ commit }, gid) {
      commit('setGid', gid)
    },
    resetGid({ commit }) {
      commit('resetGid')
    }
  }
})
