<template>
  <div class="logout-button">
    <a-button type="primary" @click="logout()">
      Logout
    </a-button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    // For logout button
    logout() {
      axios.post('/api/logout')
        .then((response) => {
          this.$store.dispatch("resetUsername")
          this.$store.dispatch("resetGid")
          this.$router.push('/')
        })
        .catch((error) => {
          this.$message.error(error)
        })
    }
  }
}
</script>
