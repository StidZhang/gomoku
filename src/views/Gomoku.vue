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
