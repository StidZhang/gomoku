<template>
  <div class="surrender-button">
    <a-button type="primary" @click="surrender()">
      Surrender
    </a-button>
  </div>
</template>

<script>
export default {
  methods: {
    surrender() {
      this.$socket.emit("gomoku_fail", this.$store.state.gid)
      this.$store.dispatch("resetGid")
    }
  }
}
</script>
