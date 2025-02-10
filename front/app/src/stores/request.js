import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useRequestStore = defineStore("request", {
  state: () => ({
    requests: [],
  }),
  getters: {

  },
  actions: {
    // Загрузка запросов авторизованного пользователя
    async loadMyRequests() {
      const res = await resources.request.loadMyRequests();
      if (res.__state === "success") {
        this.requests = res.data
      }
      return res.data
    },
    // Загрузка детальной информации о запросе по ID
    async loadRequestDetailed(id) {
      const res = await resources.request.getRequestDetailed(id);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Создание запроса
    async createRequest(data) {
      const res = await resources.request.createRequest(data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Обновление запроса
    async updateRequest(id, data) {
      const res = await resources.request.partialUpdateRequest(id, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление запроса
    async deleteRequest(id) {
      const res = await resources.request.deleteRequest(id);
      if (res.__state === "success") {
        return true
      }
      return null
    },
  }
});