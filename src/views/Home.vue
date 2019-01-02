<template>
  <div class="home">
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'home',
  mounted() {
    // TODO: Add get login logic here
    this.$router.push("/login")
  }
}
</script>
