<template>
<div class="board">
  <svg width="480" height="480" :viewBox="viewBoxInfo" ref="boardSvg">
    <g v-on:click="handleBoardClick">
      <rect :width="viewBoxSize" :height="viewBoxSize" fill="#DCB35C" />
      <rect :width="outSideRectSize" :height="outSideRectSize" x="1" y="1" stroke="#000" stroke-width="0.05" fill="none" />
      <line v-for="i in boardSize" v-bind:x1="2*i + 1" y1="1" v-bind:x2="2*i + 1" :y2="viewBoxSize-1" stroke="#000" stroke-width="0.05" fill="none"></line>
      <line v-for="i in boardSize" x1="1" v-bind:y1="2*i + 1" :x2="viewBoxSize-1" v-bind:y2="2*i + 1" stroke="#000" stroke-width="0.05" fill="none"></line>
      <template v-for="i in Array.from(Array(boardSize+1).keys())">
        <circle class="shadow-stone" v-for="j in Array.from(Array(boardSize+1).keys())" v-bind:cx="2*j + 1" v-bind:cy="2*i + 1" r="0.9"></circle>
      </template>
    </g>
  </svg>
</div>
</template>

<script>
export default {
  props: {
    'boardSize': Number
  },
  computed: {
    viewBoxSize() {
      return 2 + this.boardSize * 2
    },
    outSideRectSize() {
      return this.boardSize * 2
    },
    viewBoxInfo() {
      return "0 0 " + this.viewBoxSize.toString() + " " + this.viewBoxSize.toString()
    }
  },
  methods: {
    handleBoardClick: function(evt) {
      let svg = this.$refs.boardSvg
      let pt = svg.createSVGPoint()
      pt.x = evt.clientX
      pt.y = evt.clientY
      // The cursor point, translated into svg coordinates
      var cursorpt = pt.matrixTransform(svg.getScreenCTM().inverse())

      var roundedX = convertCoord(cursorpt.x)
      var roundedY = convertCoord(cursorpt.y)

      console.log("(" + roundedX + ", " + roundedY + ")")

    },
    convertCoord(coord) {
      var lower = Math.floor(coord)
      if (lower % 2 == 0) {
        return Math.ceil(coord)
      } else {
        return lower
      }
    }
  }
}
</script>

<style>
.shadow-stone {
  opacity: 0;
}
.shadow-stone:hover {
  opacity: 0.4;
}
</style>
