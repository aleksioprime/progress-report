import { useAuthStore } from "@/stores/auth";
import jwtService from "@/services/jwt/jwt.service";

export const isLoggedIn = async ({ to }) => {
  const authStore = useAuthStore();

  // Получаем access_token из локального хранилища
  let accessToken = jwtService.getAccessToken();

  // Если токен отсутствует или невалиден → пробуем обновить
  if (!accessToken || !authStore.isAuthenticated) {
    try {
      console.log("Attempting token refresh...");
      await authStore.refresh(); // Обновляем токен
    } catch (error) {
      console.error("Token refresh failed:", error);
    }
  }

  // Если access-токен всё ещё отсутствует → редирект на OAuth2 `/authorize/`
  if (!accessToken) {

    const authUrl = `${import.meta.env.VITE_AUTH_URL}/o/authorize/?response_type=code`
      + `&client_id=${import.meta.env.VITE_OAUTH_CLIENT_ID}`
      + `&redirect_uri=http://localhost:8234/callback`;

    window.location.href = authUrl;
    return false;
  }

  return true;
};
