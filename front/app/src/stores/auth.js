import { defineStore } from "pinia";
import resources from "@/services/resources";
import jwtService from "@/services/jwt/jwt.service";
import { jwtDecode } from "jwt-decode";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null, // Текущий пользователь
  }),
  getters: {
    // Пользователь аутентифицирован?
    isAuthenticated() {
      try {
        const decodedToken = this.getAuthData();
        console.log(decodedToken);
        return decodedToken.exp > Math.floor(Date.now() / 1000);
      } catch (error) {
        console.error("Ошибка проверки токена:", error);
        return false;
      }
    },
  },
  actions: {
    // Получение данных из jwt-токена
    getAuthData() {
      return jwtDecode(jwtService.getAccessToken())
    },
    // Отправка refresh-токена для обновления аутентификации: POST /api/token/refresh
    async refresh() {
      console.log(jwtService.getRefreshToken());
      const result = await resources.auth.refresh({ 'refresh': jwtService.getRefreshToken() });
      if (result.__state === "success") {
        jwtService.saveAccessToken(result.data.access);
        resources.auth.setAuthHeader(jwtService.getAccessToken());
      } else {
        this.logout();
      }
    },
    async logout() {
      jwtService.destroyTokens();
      resources.auth.setAuthHeader("");
    },
  },
});