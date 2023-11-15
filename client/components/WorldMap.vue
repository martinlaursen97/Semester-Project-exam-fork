<template>
  <div class="container">
    <canvas ref="canvasElement" style="border: 1px solid black" />
    <div class="info-box">
      <p v-if="selectedPoint">Selected Point:</p>
      <ul v-if="selectedPoint">
        <li>X: {{ selectedPoint.x }}</li>
        <li>Y: {{ selectedPoint.y }}</li>
        <li>Color: {{ selectedPoint.color }}</li>
        <li>Circled: {{ selectedPoint.circled }}</li>
        <li v-if="selectedPoint.circled">Radius: {{ selectedPoint.radius }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  height: {
    type: Number,
    default: 500,
  },
  width: {
    type: Number,
    default: 500,
  },
  scale: {
    type: Number,
    default: 10,
  },
  placePositions: {
    type: Array,
    default: () => [],
  },
  playerPosition: {
    type: Object,
    default: () => {},
  },
});

const height = props.height;
const width = props.width;
const scale = props.scale;

const canvasElement = ref();
const context = ref();

const selectedPoint = ref(null);

var placePositionsArray = props.placePositions;
var playerPosition = props.playerPosition;

onMounted(() => {
  context.value = canvasElement.value?.getContext("2d") || undefined;
  canvasElement.value.height = height;
  canvasElement.value.width = width;

  canvasElement.value.addEventListener(
    "click",
    coordinateSystemClickEventListener
  );

  render();
});

function insertPoint(x, y, color, circled = false, radius = 0) {
  placePositionsArray.push({
    x: x,
    y: y,
    color: color,
    circled: circled,
    radius: radius,
  });
}

function render() {
  context.value.clearRect(0, 0, width, height);

  const offsetX = (width - scale) / 2;
  const offsetY = (height - scale) / 2;

  placePositionsArray.forEach((point) => {
    context.value.fillStyle = point.color;
    context.value?.fillRect(point.x + offsetX, point.y + offsetY, scale, scale);

    if (point.circled) {
      const circleOffsetX = width / 2;
      const circleOffsetY = height / 2;

      drawCircleAroundPoint(
        point.x + circleOffsetX,
        point.y + circleOffsetY,
        point.radius,
        point.color
      );
    }
  });
}

function drawCircleAroundPoint(x, y, radius, color) {
  context.value?.beginPath();
  context.value?.arc(x, y, radius, 0, 2 * Math.PI);
  context.value?.stroke();
}

function selectPointAt(x, y) {
  placePositionsArray.forEach((point) => {
    const minX = point.x - scale / 2;
    const maxX = point.x + scale / 2;
    const minY = point.y - scale / 2;
    const maxY = point.y + scale / 2;

    if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
      selectedPoint.value = { ...point };
    }
  });
}

function coordinateSystemClickEventListener(event) {
  const offsetX = width / 2;
  const offsetY = height / 2;

  const rect = canvasElement.value.getBoundingClientRect();
  const x = Math.round(event.clientX - rect.left - offsetX);
  const y = Math.round(event.clientY - rect.top - offsetY);

  selectPointAt(x, y);
}
</script>

<style>
.container {
  display: flex;
}

.info-box {
  margin-left: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>