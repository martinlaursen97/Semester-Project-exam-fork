<template>
  <div>
    <div class="container">
      <canvas ref="canvasElement" style="border: 1px solid black" />
      <div class="info-box">
        <p v-if="selected">Selected Point:</p>
        <div v-if="selected" class="json-box">
          <pre>{{ selected }}</pre>
        </div>
      </div>
    </div>

    <div>
      <button @click="moveUp">Up</button>
      <button @click="moveDown">Down</button>
      <button @click="moveLeft">Left</button>
      <button @click="moveRight">Right</button>
    </div>
  </div>
</template>

<script setup>
import { get } from "~/requests";
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
  places: {
    type: Array,
    default: () => [],
  },
  player: {
    type: Object,
    default: () => {},
  },
});

const height = props.height;
const width = props.width;
const scale = props.scale;

const canvasElement = ref();
const context = ref();

const selected = ref(null);

var placesArray = props.places;
var player = props.player;

watch(player.character_location, async () => {
  const { data } = await get(`/characters/place/${player.id}`);

  if (selected.value.id === player.id) {
    selected.value.place = data.value.data;
  }
});

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

function render() {
  context.value.clearRect(0, 0, width, height);
  renderPlaces();
  renderPlayer();
}

function renderPlayer() {
  const characterLocation = player.character_location;
  const offsetX = (width - scale) / 2;
  const offsetY = (height - scale) / 2;

  drawPoint(
    characterLocation.x + offsetX,
    characterLocation.y + offsetY,
    "red"
  );
}

function renderPlaces() {
  const offsetX = (width - scale) / 2;
  const offsetY = (height - scale) / 2;

  placesArray.forEach((point) => {
    drawPoint(point.x + offsetX, point.y + offsetY, "blue");

    const circleOffsetX = width / 2;
    const circleOffsetY = height / 2;

    drawCircleAroundPoint(
      point.x + circleOffsetX,
      point.y + circleOffsetY,
      point.radius,
      "red"
    );
  });
}

function drawPoint(x, y, color) {
  context.value.fillStyle = color;
  context.value?.fillRect(x, y, scale, scale);
}

function drawCircleAroundPoint(x, y, radius, color) {
  context.value.fillStyle = color;
  context.value?.beginPath();
  context.value?.arc(x, y, radius, 0, 2 * Math.PI);
  context.value?.stroke();
}

function selectPointAt(x, y) {
  const playerX = player.character_location.x;
  const playerY = player.character_location.y;

  const minX = playerX - scale / 2;
  const maxX = playerX + scale / 2;
  const minY = playerY - scale / 2;
  const maxY = playerY + scale / 2;

  if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
    selected.value = { ...player };
    return;
  }

  placesArray.forEach((point) => {
    const minX = point.x - scale / 2;
    const maxX = point.x + scale / 2;
    const minY = point.y - scale / 2;
    const maxY = point.y + scale / 2;

    if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
      selected.value = { ...point };
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

const emit = defineEmits(["moveUp", "moveDown", "moveLeft", "moveRight"]);

function moveUp() {
  player.character_location.y -= scale;
  render();
  emit("moveUp");
}

function moveDown() {
  player.character_location.y += scale;
  render();
  emit("moveDown");
}

function moveLeft() {
  player.character_location.x -= scale;
  render();
  emit("moveLeft");
}

function moveRight() {
  player.character_location.x += scale;
  render();
  emit("moveRight");
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