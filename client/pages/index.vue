<template>
  <div>
    <p>Go to login page: <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script setup>
const router = useRouter();

// redirect to login if not logged in
if (!useCookie("access_token").value) {
  router.push("/login");
}
</script>