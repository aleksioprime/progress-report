import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useCommentStore = defineStore("comment", {
  state: () => ({
    comments: [],
  }),
  getters: {

  },
  actions: {
    // Загрузка комментариев к запросу
    async loadRequestComments(requestId) {
      const res = await resources.comment.getRequestComments(requestId);
      if (res.__state === "success") {
        this.comments = res.data
      }
      return res.data
    },
    // Создание комментария
    async createComment(requestId, data) {
      const res = await resources.comment.createComment(requestId, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Обновление комментария
    async updateComment(requestId, commentId, data) {
      const res = await resources.comment.partialUpdateComment(requestId, commentId, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
    // Удаление комментария
    async deleteComment(requestId, commentId) {
      const res = await resources.comment.deleteComment(requestId, commentId);
      if (res.__state === "success") {
        return true
      }
      return null
    },
  }
});