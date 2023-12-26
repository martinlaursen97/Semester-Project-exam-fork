<template>
  <div>
    <h1>Forgot Password</h1>
    <form @submit.prevent="forgotPassword">
      <input type="email" v-model="email" placeholder="Email" />
      <button type="submit">Reset Password</button>
    </form>
    <p>Back to login page: <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script setup>
import { post } from "~/requests";
const email = ref("");

const router = useRouter();

const forgotPassword = async (e) => {
  e.preventDefault();

  try {
    const { data } = await post("/auth/forgot-password", {
      email: email.value,
    });
    console.log("Forgot password response:", data);
    alert("Check your email for a reset link");
  } catch (error) {
    console.error("Error resetting password:", error);
  }

  router.push("/login");
};
</script>