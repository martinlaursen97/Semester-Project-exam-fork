<template>
  <div>
    <form @submit="login">
      <input data-test="e-mail" type="email" v-model="email" />
      <input
        data-test="password"
        type="password"
        v-model="password"
        minlength="8"
        maxlength="32"
      />
      <button data-test="loginButton" type="submit">Login</button>
    </form>
    <p>
      Don't have an account? <router-link to="/register">Register</router-link>
    </p>
    <router-link to="/forgot-password">Forgot Password</router-link>
  </div>
</template>

<script setup>
import { post } from "~/requests";

const email = ref("user0@example.com");
const password = ref("password");

const router = useRouter();

const login = async (e) => {
  e.preventDefault();

  if (!email.value || !password.value) {
    alert("Please fill out all fields");
    return;
  }

  if (password.value.length < 8 || password.value.length > 32) {
    alert("Password must be between 8 and 32 characters");
    return;
  }

  try {
    const { data, error } = await post("/auth/login-email", {
      email: email.value,
      password: password.value,
    });

    if (error.value) {
      throw new Error(error.value.data.detail);
    }

    const { access_token } = data.value.data;

    const accessToken = useCookie("access_token");
    accessToken.value = access_token;

    router.push("/characters");
  } catch (error) {
    alert(error);
    return;
  }
};
</script>
