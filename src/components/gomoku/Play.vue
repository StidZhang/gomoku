<template>
  <div class="playboard">
    <Board></Board>
    <InfoBox></InfoBox>
    <SurrenderButton></SurrenderButton>
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
