<template>
  <div>
    <form>
      <input type="text" v-model="character_name" />
      <select v-model="selected_class">
        <option
          v-for="base_class in base_classes_dropdown"
          :key="base_class.id"
          :value="base_class.id"
        >
          {{ base_class.name }}
        </option>
      </select>

      <select v-model="selected_gender">
        <option value="male">male</option>
        <option value="female">female</option>
        <option value="other">other</option>
      </select>
    </form>

    <button @click="createCharacter" type="submit">Create character</button>
    <br />
    <br />

    <button
      @click="enterWorld(character)"
      v-for="character in characters"
      :key="character.id"
    >
      Name: {{ character.character_name }} Gender: {{ character.gender }} Alive:
      {{ character.alive }} Level: {{ character.level }} XP:
      {{ character.xp }} Money: {{ character.money }} Class:
      {{ character.base_class.name }} ID: {{ character.id }}
    </button>
  </div>
</template>

<script setup>
import { get, post } from "~/requests";
import { useCharacterStore } from "~/store/character";

// data
const characters = ref([]);

// form data
const base_classes_dropdown = ref([]);

// selected values
const selected_class = ref("");
const selected_gender = ref("");
const character_name = ref("");

const router = useRouter();

const fetchCharacters = async () => {
  const { data } = await get("/characters");
  characters.value = data.value.data;
};

const fetchClasses = async () => {
  const { data } = await get("/base-classes");

  if (!data.value.data.length) {
    return;
  }
  base_classes_dropdown.value = data.value.data;
};

const createCharacter = async (e) => {
  e.preventDefault();
  await post("/characters", {
    character_name: character_name.value,
    base_class_id: selected_class.value,
    gender: selected_gender.value,
  });

  await fetchCharacters();
};

const enterWorld = async (char) => {
  const characterStore = useCharacterStore();
  const { setCharacter, getCharacter } = characterStore;
  setCharacter(char);
  router.push("/world");
};

await fetchCharacters();
await fetchClasses();
</script>;
