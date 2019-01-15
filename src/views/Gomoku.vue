<template>
<div class="gomoku">
  <div v-if="$store.state.gid">
    <PlayBoard :boardInfo="rawBoard"></PlayBoard>
  </div>
  <div v-else>
    <InviteBox></InviteBox>
  </div>
</div>
</template>

<script>
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
  data: function() {
    return {
      rawBoard: [],
      gameHost: "",
      gameGuest: "",
      boardSize: 13 // Default size is 13
    }
  },
  sockets: {
    gomoku_status(data) {
      // Set current game id
      if (data.message) {
        if (data.message.type == 40) {
          this.$message.error(data.message.content)
        } else {
          this.$message.info(data.message.content)
        }
      }
      if (data.current_game) {
        // Reconnect behavior
        this.joinGame(data.current_game)
      } else {
        this.$store.dispatch("resetGid")
      }
      for (let i = 0; i < data.invites.length; i++) {
        this.$nextTick(() => this.displayNotification(data.invites[i]))
      }
    },
    // Guest Related
    gomoku_invite(data) {
      this.displayNotification(data)
    },
    // Joining a game and get the board data
    gomoku_board(data) {
      if (data.status == 1) {
        this.$message.info("Waiting for guest to join in")
      } else {
        this.rawBoard = data.board
        this.gameHost = data.host.username
        this.gameGuest = data.guest.username
        this.boardSize = data.config.size
        if (data.status == 2 && this.gameHost == this.$store.state.username) {
          this.$message.info("It's your turn!")
        } else if (data.status == 3 && this.gameGuest == this.$store.state.username) {
          this.$message.info("Waiting for guest to join in")
        }
      }
    },
    // Game Move data
    gomoku_board_update(data) {
      if (data.username == this.gameHost) {
        // Set black stone
        this.$set(this.rawBoard, data.y*this.boardSize+data.x, 1)
      } else if (data.username == this.gameGuest) {
        // Set white stone
        this.$set(this.rawBoard, data.y*this.boardSize+data.x, 2)
      } else {
        console.log(data)
      }
      if (data.username != this.$store.state.username) {
        this.$message.info("It's your turn!")
      }
    },
    // Game ended
    gomoku_end(data) {
      if (data.win == this.$store.state.username) {
        this.$message.success("You win!")
      } else {
        this.$message.success("You Lost!")
      }
      // reset game status
      this.rawBoard = []
      this.gameHost = ""
      this.gameGuest = ""
      this.boardSize = 13
      this.$store.dispatch("resetGid")
    }
  },
  methods: {
    joinGame(gameid) {
      this.$store.dispatch("setGid", gameid)
      this.$socket.emit("gomoku_join", gameid)
    },
    rejectGame(gameid) {
      this.$socket.emit("gomoku_fail", gameid)
    },
    displayNotification(inviteInfo) {
      var gameid = inviteInfo.gameid
      var hostname = inviteInfo.host
      const key = `open${Date.now()}`
      this.$notification.open({
        message: "You have been invited to a game!",
        description: "Host " + hostname + " has invited you to a game!",
        duration: 0,
        btn: (h) => {
          return h('a-button', {
            props: {
              type: 'primary',
              size: 'medium',
            },
            on: {
              click: () => {
                this.joinGame(gameid)
                this.$notification.close(key)
              }
            }
          }, 'Join')
        },
        key,
        onClose: () => {
          this.rejectGame(gameid)
          this.$notification.close(key)
        },
      });
    }
  }
}
</script>
