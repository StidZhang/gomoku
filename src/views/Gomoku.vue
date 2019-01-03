<template>
  <div class="gomoku">
    <a-button type='primary' @click="logout()" class="logout-button">
      Logout
    </a-button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  sockets: {
    connect() {
      console.log('socket connected')
    }
  },
  methods: {
    logout() {
      axios.post('/api/logout')
        .then((response) => {
          console.log(response)
          this.$router.push('/')
        })
        .catch((error) => {
          console.log(error)
          this.$message.error(error)
        })
    }
  }
}
</script>
