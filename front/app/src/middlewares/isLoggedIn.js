import { useAuthStore } from "@/stores/auth";
import jwtService from "@/services/jwt/jwt.service";

export const isLoggedIn = async ({ to }) => {
  const authStore = useAuthStore();

  // Получаем access_token из локального хранилища
  let accessToken = jwtService.getAccessToken();

  // Если токен отсутствует или невалиден → пробуем обновить
  if (!accessToken || !authStore.isAuthenticated) {
    if (!jwtService.getRefreshToken()) return { name: "authorization" };
    try {
      console.log("Attempting token refresh...");
      await authStore.refresh(); // Обновляем токен
    } catch (error) {
      console.error("Token refresh failed:", error);
    }
  }

  // Если access-токен всё ещё отсутствует переход на страницу авторизации
  if (!accessToken) {
    return { name: "authorization" };
  }

  return true;
};
