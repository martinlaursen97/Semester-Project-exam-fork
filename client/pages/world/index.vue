<template>
  <div>
    <h1>World</h1>
    <h2>Character</h2>
    <p>
      Name: {{ character.character_name }} Gender: {{ character.gender }} Alive:
      {{ character.alive }} Level: {{ character.level }} XP:
      {{ character.xp }} Money: {{ character.money }} Class:
      {{ character.base_class.name }} ID: {{ character.id }}
    </p>
    <WorldMap
      :places="places"
      :player="character"
      :scale="scale"
      @moveUp="moveUp"
      @moveDown="moveDown"
      @moveLeft="moveLeft"
      @moveRight="moveRight"
    />
    <!-- // input form for "place", name, x, y, radius -->
  </div>
</template>

<script setup>
import { get, post, update } from "~/requests";
import { useCharacterStore } from "~/store/character";

const characterStore = useCharacterStore();
const { getCharacter } = characterStore;
const character = ref(getCharacter());

const places = ref([]);
const scale = 10;

const loadWorld = async () => {
  const { data } = await get("/places");
  places.value = data.value.data;
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

await loadWorld();
</script>