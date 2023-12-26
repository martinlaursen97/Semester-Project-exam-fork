<template>
  <div>
    <form @submit.prevent="createPlace">
      <label data-test="placeName" for="name">Name:</label>
      <input v-model="place.name" type="text" id="name" required />

      <label data-test="Xcoordinate" for="x">X Coordinate:</label>
      <input v-model="place.x" type="number" id="x" required />

      <label data-test="Ycoordinate" for="y">Y Coordinate:</label>
      <input v-model="place.y" type="number" id="y" required />

      <label data-test="placeRadius" for="radius">Radius:</label>
      <input v-model="place.radius" type="number" id="radius" required />

      <button data-test="submitPlace" type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { post } from "~/requests";

const place = ref({
  name: "",
  x: 0,
  y: 0,
  radius: 0,
});

const emit = defineEmits(["placeCreated"]);

const createPlace = async () => {
  try {
    await post("/places", place.value);
    emit("placeCreated");
  } catch (err) {
    console.error("Error creating place:", err);
  }
};
</script>

