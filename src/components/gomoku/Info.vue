<template>
<div class="info-box">
  <a-row>
    <h2>{{ $store.state.username }}</h2>
  </a-row>
  <a-row>
    <a-button type="primary" @click="cancelGame()">
      {{ getButtonContext() }}
    </a-button>
  </a-row>
  <a-row>
    <LogoutButton></LogoutButton>
  </a-row>
</div>
</template>

<script>
import LogoutButton from '@/components/auth/Logout'

export default {
  props: {
    gameStarted: Boolean
  },
  components: {
    LogoutButton
  },
  methods: {
    cancelGame() {
      this.$socket.emit("gomoku_fail", this.$store.state.gid)
    },
    getButtonContext() {
      if (this.gameStarted) {
        return 'Surrender'
      } else {
        return 'Cancel Game'
      }
    }
  }
}
</script>

<style>
.info-box {
  margin: auto;
  text-align: center;
}
</style>
