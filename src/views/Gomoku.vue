<template>
<div class="gomoku">
  <div v-if="$store.state.gid">
    <PlayBoard></PlayBoard>
  </div>
  <div v-else>
    <InviteBox></InviteBox>
  </div>
  <a-button type="primary" @click="logout()">
    Logout
  </a-button>
</div>
</template>

<script>
import axios from 'axios'
import InviteBox from '@/components/gomoku/Invite'
import PlayBoard from '@/components/gomoku/Play'

export default {
  mounted() {
    // Reconnect socket
    this.$socket.disconnect()
    this.$socket.connect()
  },
  components: {
    InviteBox,
    PlayBoard
  },
  sockets: {
    gomoku_status(data) {
      // Set current game id
      this.$store.dispatch("setGid", data.current_game)
    },
    // Guest Related
    gomoku_invite(data) {
      const key = `open${Date.now()}`;
      console.log(data)
      this.$notification.open({
        message: "You have been invited to a game!",
        description: "Host " + data.host + " invited you to a game!",
        duration: 0,
        btn: (h) => {
          return h('a-button', {
            props: {
              type: 'primary',
              size: 'small',
            },
            on: {
              click: () => {
                this.joinGame(data.gameid)
                this.$notification.close(key)
              }
            }
          }, 'Join')
        },
        key,
        onClose: () => {
          this.rejectGame(data.gameid)
          this.$notification.close(key)
        },
      });
    },
    // Host Related
    gomoku_invite_success(data) {
      this.$message.success("Guest has accepted your invite!")
      this.$store.dispatch("setGid", data.gameid)
    },
    gomoku_invite_failed(data) {
      this.$message.warning("Guest has rejected your invite!")
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
      console.log("End event")
    }
  },
  methods: {
    joinGame(gameid) {
      this.$socket.emit("gomoku_join", gameid)
      this.$store.dispatch("setGid", gameid)
    },
    rejectGame(gameid) {
      this.$socket.emit("gomoku_fail", gameid)
    },
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
