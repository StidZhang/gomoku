import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import Gomoku from '@/views/Gomoku.vue'
import Login from '@/components/auth/Login.vue'
import Register from '@/components/auth/Register.vue'
import store from './store.js';
import axios from 'axios'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [{
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/gomoku',
      name: 'gomoku',
      component: Gomoku,
      meta: {
        requiresLogin: true
      }
    },
    // Everything else
    {
      path: '*',
      redirect: '/'
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresLogin) {
    axios.get('/api/login')
      .then((response) => {
        // handle success
        var data = response.data;
        if (data.status == -1) {
          next("/login")
        } else {
          store.dispatch('setUsername', data.username)
          next()
        }
      })
      .catch((error) => {
        console.log(error)
        next('/login')
      })
  } else {
    next()
  }
})

export default router
