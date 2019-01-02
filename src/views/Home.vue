<template>
  <div class="home">
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'home',
  mounted() {
    axios.get('/api/login')
      .then((response) => {
        // handle success
        var data = response.data;
        if (data.status == -1) {
          this.$router.push("/login")
        } else {
          this.$router.push("/gomoku")
        }
      })
      .catch((error) => {
        // handle error
        this.$message.error(error);
      })
  }
}
</script>
