<template>
<div class="gomoku">
  <a-input placeholder="Basic usage" />
  <a-button type='primary' @click="createGame()">
    Create a game
  </a-button>
  <a-button type='primary' @click="joinGame()">
    Join game
  </a-button>
  <a-button type='primary' @click="rejectGame()">
    Reject game
  </a-button>
  <a-button type='primary' @click="logout()">
    Logout
  </a-button>
</div>
</template>

<script>
import axios from 'axios'
export default {
  mounted() {
    // Reconnect socket
    this.$socket.disconnect()
    this.$socket.connect()
  },
  sockets: {
    gomoku_status(data) {
      console.log("Reply for connected")
    },
    // Guest Related
    gomoku_invite(data) {
      this.$message.success(data)
      const key = `open${Date.now()}`;
      this.$notification.open({
        message: 'You have been invited to a game',
        description: data,
        btn: (h) => {
          return h('a-button', {
            props: {
              type: 'primary',
              size: 'small',
            },
            on: {
              click: () => {
                this.$notification.close(key)
              }
            }
          }, 'Join')
        },
        key,
        onClose: () => {
          this.$notification.close(key)
        },
      });
    },
    // Host Related
    gomoku_invite_success(data) {
      this.$message.success(data)
    },
    gomoku_invite_failed(data) {
      this.$message.success(data)
    },
    // Joining a game and get the board data
    gomoku_board(data) {
      console.log(data)
    },
    // Game Move data
    gomoku_board_update(data) {
      console.log(data)
    },
    // Game ended
    gomoku_end(data) {
      console.log(data)
    }
  },
  methods: {
    createGame() {
      var gameConfig = {
        size: 13,
        invite: "abcd"
      }
      this.$socket.emit("gomoku_create", gameConfig)
    },
    joinGame() {
      this.$socket.emit("gomoku_join")
    },
    rejectGame() {
      this.$socket.emit("gomoku_reject")
    },
    // For logout button
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
