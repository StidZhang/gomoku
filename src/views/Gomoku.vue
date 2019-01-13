<template>
<div class="gomoku">
  <div v-if="$store.state.gid">
    <PlayBoard :boardInfo="currentBoard"></PlayBoard>
  </div>
  <div v-else>
    <InviteBox></InviteBox>
  </div>
  <LogoutButton></LogoutButton>
</div>
</template>

<script>
import InviteBox from '@/components/gomoku/Invite'
import PlayBoard from '@/components/gomoku/Play'
import LogoutButton from '@/components/auth/Logout'

export default {
  mounted() {
    // Reconnect socket
    this.$socket.disconnect()
    this.$socket.connect()
  },
  components: {
    InviteBox,
    PlayBoard,
    LogoutButton
  },
  computed: {
    currentBoard: function() {
      if (this.rawBoard) {
        var boardSize = 13 // Should come from this.rawBoard.config.boardSize
        var result = []
        for (let i = 0; i < boardSize; i++) {
          var row = this.rawBoard.board.slice(i*boardSize, i*boardSize+boardSize-1)
          result.push(row)
        }
        return result
      } else {
        return []
      }
    }
  },
  data: function() {
    return {
      rawBoard: null
    }
  },
  sockets: {
    gomoku_status(data) {
      // Set current game id

      if (data.message) {
        this.$message.info(data.message)
      }
      if (data.current_game) {
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
      this.$message.success("Game is ready to start!")
      this.rawBoard = data
    },
    // Game Move data
    gomoku_board_update(data) {
      //this.currentBoard[data.x][data.y]
    },
    // Game ended
    gomoku_end(data) {
      if (data.win == this.$store.state.username) {
        this.$message.success("You win!")
      } else {
        this.$message.success("You Lost!")
      }
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
              size: 'small',
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
