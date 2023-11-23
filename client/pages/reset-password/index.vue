<template>
  <div>
    <h1>Reset Password</h1>
    <form @submit.prevent="resetPassword">
      <input type="password" v-model="password" placeholder="Password" />
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="Confirm Password"
      />
      <button type="submit">Reset Password</button>
    </form>
    <p>Back to login page: <router-link to="/login">Login</router-link></p>
  </div>
</template>


<script setup>
import { get, post } from "~/requests";
const password = ref("");
const confirmPassword = ref("");

const route = useRoute();
const router = useRouter();

const resetPassword = async (e) => {
  e.preventDefault();

  const token = route.query.token;

  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match");
    return;
  }

  try {
    const { data, error } = await post("/auth/reset-password", {
      token: token,
      new_password: password.value,
    });
    console.log("Reset password response:", data);
    if (error) {
      alert(error.value.data.detail);
    } else {
      alert("Password reset successfully");
    }
  } catch (error) {
    console.error("Error resetting password:", error);
  }

  router.push("/login");
};
</script>