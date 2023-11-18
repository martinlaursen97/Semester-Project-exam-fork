<template>
  <div>
    <h1>World</h1>
    <h2>Character</h2>
    <p>
      Name: {{ characterName }} Gender: {{ character.gender }} Alive:
      {{ character.alive }} Level: {{ character.level }} XP:
      {{ character.xp }} Money: {{ character.money }} Class:
      {{ character.base_class.name }} ID: {{ character.id }}
    </p>
    <WorldMap
      v-if="!loading && !error"
      :places="places"
      :player="character"
      :height="500"
      :width="500"
      :scale="scale"
      @moveUp="moveUp"
      @moveDown="moveDown"
      @moveLeft="moveLeft"
      @moveRight="moveRight"
    />
    <div v-else>
      <p v-if="loading">Loading world...</p>
      <p v-if="error">Error loading world: {{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { get, update } from "~/requests";
import { useCharacterStore } from "~/store/character";

const characterStore = useCharacterStore();
const { getCharacter } = characterStore;
const character = ref(getCharacter());

const places = ref([]);
const scale = 10;
const loading = ref(true);
const error = ref(null);

const characterName = computed(() => character.value.character_name);

onMounted(() => {
  loadWorld();
});

const loadWorld = async () => {
  try {
    const { data } = await get("/places");
    places.value = data.value?.data;
  } catch (err) {
    console.error("Error loading world:", err);
    error.value = "Failed to load world data.";
  } finally {
    loading.value = false;
  }
};

const moveUp = async () => {
  await update(`/characters/move/${character.value.id}`, {
    y: character.value.character_location.y - scale,
  });
};
const moveDown = async () => {
  await update(`/characters/move/${character.value.id}`, {
    y: character.value.character_location.y + scale,
  });
};
const moveLeft = async () => {
  await update(`/characters/move/${character.value.id}`, {
    x: character.value.character_location.x - scale,
  });
};
const moveRight = async () => {
  await update(`/characters/move/${character.value.id}`, {
    x: character.value.character_location.x + scale,
  });
};
</script>
