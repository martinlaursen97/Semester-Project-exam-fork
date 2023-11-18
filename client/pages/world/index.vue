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
      :height="500"
      :width="500"
      :scale="scale"
      @moveUp="moveUp"
      @moveDown="moveDown"
      @moveLeft="moveLeft"
      @moveRight="moveRight"
    />
    <!-- <h2>Place form</h2>
    <form @submit.prevent="insertPlace">
      <label for="placeName">Name</label>
      <input
        type="text"
        id="placeName"
        v-model="placeName"
        placeholder="Place name"
      />
      <label for="placeX">X</label>
      <input type="number" id="placeX" v-model="placeX" placeholder="Place X" />
      <label for="placeY">Y</label>
      <input type="number" id="placeY" v-model="placeY" placeholder="Place Y" />
      <label for="placeRadius">Radius</label>
      <input
        type="number"
        id="placeRadius"
        v-model="placeRadius"
        placeholder="Place Radius"
      />
      <button type="submit">Create place</button>
    </form> -->
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