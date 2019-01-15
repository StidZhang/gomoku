<template>
<div class="playboard">
  <a-row>
    <a-col :span="20">
      <Board :boardSize="13" :boardInfo="boardInfo"></Board>
    </a-col>
    <a-col :span="4">
      <a-row>
        <InfoBox :gameStarted="getGameStatus()"></InfoBox>
      </a-row>
    </a-col>
  </a-row>
</div>
</template>

<script>
import Board from '@/components/gomoku/Board'
import InfoBox from '@/components/gomoku/Info'

export default {
  components: {
    Board,
    InfoBox
  },
  props: {
    "boardInfo": Array
  },
  methods: {
    getGameStatus() {
      if (this.boardInfo.length != 0) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style>
.playboard {
  width: 70%;
  text-align: center;
  margin: auto;
}
</style>
