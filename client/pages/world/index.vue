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
    <WorldMap :placePositions="placePositions" />
  </div>
</template>

<script setup>
import { get, post } from "~/requests";
import { useCharacterStore } from "~/store/character";

const characterStore = useCharacterStore();
const { getCharacter } = characterStore;
const character = ref(getCharacter());

const placePositions = ref([]);
const playerPosition = ref({});

const fetchPlacePositions = async () => {
  const { data } = await get("/places");
  const places = data.value.data;
  const pointFormat = places.map((place) => {
    return {
      x: place.x,
      y: place.y,
      color: "blue",
      circled: true,
      radius: place.radius,
    };
  });
  return pointFormat;
};

const fetchPlayerPositions = async () => {
  const { data } = await get("/character-location");
  const places = data.value.data;
  const pointFormat = places.map((place) => {
    return {
      x: place.x,
      y: place.y,
      color: "green",
    };
  });
  return pointFormat;
};

const loadWorld = async () => {
  //const playerPosition = await fetchPlayerPositions();
  placePositions.value = await fetchPlacePositions();
  //playerPosition.value = playerPosition;
};

await loadWorld();
</script>