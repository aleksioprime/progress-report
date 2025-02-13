<template>
  <div>

    <h1>Войдите в систему</h1>
    <div>
      <app-button class="btn btn-success" @click="authorization">Войти через SkolStream</app-button>
    </div>

  </div>
</template>

<script setup>
import { onMounted } from "vue";
import jwtService from "@/services/jwt/jwt.service";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();

const authorization = () => {

  const authUrl = `${import.meta.env.VITE_AUTH_URL}/o/authorize/?response_type=code`
    + `&client_id=${import.meta.env.VITE_OAUTH_CLIENT_ID}`
    + `&redirect_uri=${import.meta.env.VITE_BACKEND_URL}/callback`;

  window.location.href = authUrl;
}

onMounted(async () => {
  const accessToken = jwtService.getAccessToken();

  if (accessToken && authStore.isAuthenticated) {
    router.push({ name: "home" });
  }
})

</script>