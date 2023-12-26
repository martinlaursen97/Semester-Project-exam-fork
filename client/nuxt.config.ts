// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@pinia/nuxt",
  ],

  runtimeConfig: {
    public: {
      environment: process.env.ENVIRONMENT ?? "local",
      base_url: process.env.BASE_URL ?? "http://localhost:8080/api",
    },
  },
})
