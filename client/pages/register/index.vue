<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="register">
      <input type="email" v-model="email" placeholder="Email" />
      <input type="password" v-model="password" placeholder="Password" />
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="Confirm Password"
      />
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>


<script setup>
import { post } from "~/requests";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const router = useRouter();

const register = async (e) => {
  e.preventDefault();

  if (!email.value || !password.value || !confirmPassword.value) {
    alert("Please fill out all fields");
    return;
  }

  if (password.value.length < 8 || password.value.length > 32) {
    alert("Password must be between 8 and 32 characters");
    return;
  }

  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match");
    return;
  }

  try {
    const { data, error } = await post("/auth/register", {
      email: email.value,
      password: password.value,
    });

    if (error.value) {
      throw new Error(error.value.data.detail);
    }

    console.log("Register response:", data);
    alert("Registration successful");
  } catch (error) {
    console.error("Error registering:", error);
    alert(error);
  }

  router.push("/login");
};
</script>
