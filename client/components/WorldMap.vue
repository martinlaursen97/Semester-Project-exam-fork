<template>
  <div>
    <div class="container">
      <canvas ref="canvasElement" style="border: 1px solid black" />
      <div class="info-box" v-if="selected">
        <p>Selected Point:</p>
        <div class="json-box">
          <pre>{{ selected }}</pre>
        </div>
      </div>
    </div>

    <div>
      <button
        v-for="direction in ['Up', 'Down', 'Left', 'Right']"
        :key="direction"
        @click="move(direction)"
      >
        {{ direction }}
      </button>
    </div>
    <PlaceForm @placeCreated="handleCreated" />
  </div>
</template>

<script setup>
import { get } from "~/requests";

const { height, width, scale, player } = defineProps([
  "height",
  "width",
  "scale",
  "player",
]);

const canvasElement = ref(null);
const context = ref(null);
const selected = ref(null);

const offset = computed(() => ({
  x: (width - scale) / 2,
  y: (height - scale) / 2,
}));

watch(player.character_location, async () => {
  // update player `place` property on location change
  const { data } = await get(`/characters/place/${player.id}`);
  if (selected.value && selected.value.id === player.id) {
    console.log(data.value.data);
    selected.value.place = data.value.data;
  }
});

const places = ref([]);

const loadWorld = async () => {
  try {
    const { data } = await get("/places");
    places.value = data.value?.data;
    console.log("places", places.value);
    render();
  } catch (err) {
    console.error("Error loading world:", err);
  }
};

const handleCreated = async () => {
  await loadWorld();
};

onMounted(async () => {
  await loadWorld();
  initializeCanvas();
  setupCanvasClickListener();
  render();
});

function initializeCanvas() {
  context.value = canvasElement.value?.getContext("2d") || undefined;
  canvasElement.value.height = height;
  canvasElement.value.width = width;
}

function setupCanvasClickListener() {
  canvasElement.value.addEventListener(
    "click",
    coordinateSystemClickEventListener
  );
}

function render() {
  clearCanvas();
  renderPlaces();
  renderPlayer();
}

function clearCanvas() {
  context.value?.clearRect(0, 0, width, height);
}

function renderPlayer() {
  const { x, y } = player.character_location;
  drawPoint(
    x + offset.value.x,
    y + offset.value.y,
    selected.value?.id === player.id ? "green" : "red"
  );
}

function renderPlaces() {
  if (!places.value) {
    return;
  }

  places.value.forEach((point) => {
    drawPoint(
      point.x + offset.value.x,
      point.y + offset.value.y,
      selected.value?.id === point.id ? "green" : "blue"
    );
    drawCircleAroundPoint(
      point.x + width / 2,
      point.y + height / 2,
      point.radius,
      "red"
    );
  });
}

function drawPoint(x, y, color) {
  setDrawingStyle(color);
  context.value?.fillRect(x, y, scale, scale);
}

function drawCircleAroundPoint(x, y, radius, color) {
  setDrawingStyle(color);
  context.value?.beginPath();
  context.value?.arc(x, y, radius, 0, 2 * Math.PI);
  context.value?.stroke();
}

function setDrawingStyle(color) {
  context.value.fillStyle = color;
}

function setSelected(point) {
  selected.value = { ...point };
  render();
}

function selectPointAt(x, y) {
  const { x: playerX, y: playerY } = player.character_location;
  const playerInRange = isPointInRange(x, y, playerX, playerY, scale / 2);

  if (playerInRange) {
    setSelected(player);
    return;
  }

  const selectedPlace = places.value.find((point) =>
    isPointInRange(x, y, point.x, point.y, scale / 2)
  );

  if (selectedPlace) {
    setSelected(selectedPlace);
  }
}

function isPointInRange(x, y, targetX, targetY, range) {
  const minX = targetX - range;
  const maxX = targetX + range;
  const minY = targetY - range;
  const maxY = targetY + range;

  return x >= minX && x <= maxX && y >= minY && y <= maxY;
}

function coordinateSystemClickEventListener(event) {
  const rect = canvasElement.value.getBoundingClientRect();
  const x = Math.round(event.clientX - rect.left - width / 2);
  const y = Math.round(event.clientY - rect.top - height / 2);
  selectPointAt(x, y);
}

const emit = defineEmits(["moveUp", "moveDown", "moveLeft", "moveRight"]);

function move(direction) {
  console.log("move");
  switch (direction) {
    case "Up":
      player.character_location.y -= scale;
      break;
    case "Down":
      player.character_location.y += scale;
      break;
    case "Left":
      player.character_location.x -= scale;
      break;
    case "Right":
      player.character_location.x += scale;
      break;
  }
  render();
  emit(`move${direction}`);
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