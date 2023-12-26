<template>
  <div>
    <form @submit="login">
      <input data-test="e-mail" type="email" v-model="email" />
      <input data-test="password" type="password" v-model="password" />
      <button data-test="loginButton" type="submit">Login</button>
    </form>
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
  const { data } = await post("/auth/login-email", {
    email: email.value,
    password: password.value,
  });

  const { access_token } = data.value.data;

  if (!access_token) {
    throw new Error("No access token");
  }

  const accessToken = useCookie("access_token");
  accessToken.value = access_token;

  router.push("/characters");
};
</script>
