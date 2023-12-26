<template>
  <div>
    <p>Back to login page: <router-link to="/login">Login</router-link></p>
    <form>
      <input data-test="nameCharacter" type="text" v-model="character_name" />
      <select data-test="selectClass" v-model="selected_class">
        <option
          v-for="base_class in base_classes_dropdown"
          :key="base_class.id"
          :value="base_class.id"
        >
          {{ base_class.name }}
        </option>
      </select>

      <select data-test="selectGender" v-model="selected_gender">
        <option value="male">male</option>
        <option value="female">female</option>
        <option value="other">other</option>
      </select>
    </form>

    <button data-test="createCharacter" @click="createCharacter" type="submit">Create character</button>
    <br />
    <br />

    <div class="character-list">
      <div
        class="character-item"
        v-for="character in characters"
        :key="character.id"
      >
        <button @click="enterWorld(character)" data-test="enterWorld">
          Name: {{ character.character_name }} - Gender:
          {{ character.gender }} - Alive: {{ character.alive }} - Level:
          {{ character.level }} - Class: {{ character.base_class.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { get, post } from "~/requests";
import { useCharacterStore } from "~/store/character";

const characters = ref([]);
const base_classes_dropdown = ref([]);
const selected_class = ref("");
const selected_gender = ref("");
const character_name = ref("");
const router = useRouter();

const fetchCharacters = async () => {
  try {
    const { data } = await get("/characters");
    characters.value = data.value?.data;
  } catch (error) {
    console.error("Error fetching characters:", error);
  }
};

const fetchClasses = async () => {
  try {
    const { data } = await get("/base-classes");
    base_classes_dropdown.value = data.value?.data;
  } catch (error) {
    console.error("Error fetching base classes:", error);
  }
};

const createCharacter = async () => {
  if (!character_name.value) {
    alert("Name is required");
    return;
  }

  if (!selected_class.value) {
    alert("Class is required");
    return;
  }

  if (!selected_gender) {
    alert("Gender is required");
    return;
  }

  try {
    const { data, error } = await post("/characters", {
      character_name: character_name.value,
      base_class_id: selected_class.value,
      gender: selected_gender.value,
    });

    if (error.value) {
      throw new Error(error.value.data.detail);
    }

    await fetchCharacters();
  } catch (error) {
    console.error("Error creating character:", error);
    alert(error);
  }
};

const enterWorld = async (char) => {
  try {
    const characterStore = useCharacterStore();
    const { setCharacter } = characterStore;
    const { data } = await get(`/characters/place/${char.id}`);
    char.place = data.value.data;
    setCharacter(char);
    router.push("/world");
  } catch (error) {
    console.error("Error entering world:", error);
  }
};

onMounted(() => {
  fetchCharacters();
  fetchClasses();
});
</script>


<style>
.character-list {
  display: flex;
  flex-direction: column;
  align-items: left;
}

.character-item {
  margin-bottom: 4px;
}

.character-item button {
  font-size: 1.2em;
  cursor: pointer;
  border: 1px solid #ddd;
}

.character-item button:hover {
  background-color: #ddd;
}
</style>