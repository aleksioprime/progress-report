import { authClient } from "./axios.clients";
import jwtService from "@/services/jwt/jwt.service";
import { jwtDecode } from "jwt-decode";
import logger from '@/common/helpers/logger';

let isRefreshing = false;
let refreshSubscribers = [];

function onRefreshed(token) {
  refreshSubscribers.forEach(callback => callback(token));
  refreshSubscribers = [];
}

function addSubscriber(callback) {
  refreshSubscribers.push(callback);
}

async function _refreshToken() {
  logger.info("Токен истёк. Обновление токена...");

  try {
    const result = await authClient.post("/api/token/refresh/", {
      refresh: jwtService.getRefreshToken(),
    });

    if (result.data.access) {
      jwtService.saveAccessToken(result.data.access);
      logger.info(`Получен новый токен, срок действия: ${_getEncodedTokenData(result.data.access)}`);
      return result.data.access;
    }
  } catch (error) {
    console.error("Failed to refresh token", error);
    return false;
  }
}

function _getEncodedTokenData(token) {
  const decodedToken = jwtDecode(token);
  return new Date(decodedToken.exp * 1000).toLocaleString();
}

export async function handleTokenRefresh() {
  if (!isRefreshing) {
    isRefreshing = true;
    return _refreshToken()
      .then(token => {
        isRefreshing = false;
        onRefreshed(token);
        return token;
      })
      .catch(error => {
        isRefreshing = false;
        throw error;
      });
  }

  return new Promise((resolve, reject) => {
    addSubscriber(token => token ? resolve(token) : reject(new Error("Token refresh failed")));
  });
}