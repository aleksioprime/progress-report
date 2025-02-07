import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useGenerateStore = defineStore("generate", {
  state: () => ({}),
  getters: {
    // Геттеры могут быть добавлены для вычисляемых свойств
  },
  actions: {
    async generateDeepSeek(config) {
      const res = await resources.generate.generateDeepSeek(config);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
  }
});