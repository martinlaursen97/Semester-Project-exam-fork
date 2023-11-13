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
  </div>
</template>

<script setup>
import { useCharacterStore } from "~/store/character";
const characterStore = useCharacterStore();
const { getCharacter } = characterStore;

const character = ref(getCharacter());
</script>