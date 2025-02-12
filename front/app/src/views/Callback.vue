<template>
  <div class="loading">
    <h1>Авторизация...</h1>
    <p>Пожалуйста, подождите...</p>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { onMounted } from "vue";
import jwtService from "@/services/jwt/jwt.service";

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const code = route.query.code;

  if (!code) {
    console.error("Ошибка: код авторизации отсутствует!");
    return;
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v1/auth/exchange_code`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });

    const data = await response.json();

    if (data.access_token) {
      console.log("Успешно получили токен:", data);

      jwtService.saveAccessToken(data.access_token);
      jwtService.saveRefreshToken(data.refresh_token);

      router.push("/");
    } else {
      console.error("Ошибка при получении токена:", data);
    }
  } catch (error) {
    console.error("Ошибка сети или сервера:", error);
  }
});
</script>
