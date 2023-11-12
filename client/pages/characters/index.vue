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
      {{ character.base_class.name }}
    </button>
  </div>
</template>

<script setup>
import { get, post } from "~/requests";

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
  const { data } = await get("/base-characters");
  characters.value = data.value.data;
  console.log(data.value.data);
};

const fetchClasses = async () => {
  const { data } = await get("/base-classes");

  if (!data.value.data.length) {
    throw new Error("No base classes");
  }
  base_classes_dropdown.value = data.value.data;
};

const createCharacter = async (e) => {
  e.preventDefault();
  const { data } = await post("/base-characters", {
    character_name: character_name.value,
    base_class_id: selected_class.value,
    gender: selected_gender.value,
  });

  characters.value.push(data.value.data);
};

const enterWorld = async (character) => {
  //   const { data } = await post("/characters/enter-world", {
  //     character_id: character.id,
  //   });

  //   const { access_token } = data.value.data;

  //   if (!access_token) {
  //     throw new Error("No access token");
  //   }

  router.push("/world");
};

await fetchCharacters();
await fetchClasses();
</script>;
