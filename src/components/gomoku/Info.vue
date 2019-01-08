<template>
  <div class="info-box">
    <h2>Information here</h2>
    <a-button type="primary" @click="cancel()">
      Cancel Game
    </a-button>
  </div>
</template>

<script>
export default {
  methods: {
    cancel() {
      this.$socket.emit("gomoku_fail", this.$store.state.gid)
    }
  }
}
</script>

<style>
.info-box {
  margin: auto;
}
</style>
