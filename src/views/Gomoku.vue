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
  mounted() {
    // this.sockets.subscribe('*')
  },
  sockets: {
    connect() {
      this.$socket.emit("connected")
    }
  },
  methods: {
    logout() {
      axios.post('/api/logout')
        .then((response) => {
          this.$store.dispatch("resetUsername")
          this.$router.push('/')
        })
        .catch((error) => {
          this.$message.error(error)
        })
    }
  }
}
</script>
