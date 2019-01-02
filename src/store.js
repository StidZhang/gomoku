import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: ""
  },
  mutations: {
    set(state, username) {
      state.username = username
    },
    reset(state) {
      state.username = ""
    }
  },
  actions: {
    set({ commit }, username) {
      commit('set', username)
    },
    reset({ commit }) {
      commit('reset')
    }
  }
})
