<template>
<div class="playboard">
  <a-row>
    <a-col :span="18">
      <Board :boardSize="13"></Board>
    </a-col>
    <a-col :span="6">
      <a-row>
        <InfoBox></InfoBox>
      </a-row>
      <a-row>
        <SurrenderButton></SurrenderButton>
      </a-row>
    </a-col>
  </a-row>
</div>
</template>

<script>
import Board from '@/components/gomoku/Board'
import InfoBox from '@/components/gomoku/Info'
import SurrenderButton from '@/components/gomoku/Surrender'

export default {
  components: {
    Board,
    InfoBox,
    SurrenderButton
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
