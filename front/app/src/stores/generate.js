import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useGenerateStore = defineStore("generate", {
  state: () => ({}),
  getters: {
    // Геттеры могут быть добавлены для вычисляемых свойств
  },
  actions: {
    async generateReport(provider, data) {
      const res = await resources.generate.generateReportProvider(provider, data);
      if (res.__state === "success") {
        return res.data
      }
      return null
    },
  }
});