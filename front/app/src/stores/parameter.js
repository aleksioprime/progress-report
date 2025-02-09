import { defineStore } from "pinia";
import resources from "@/services/resources";


export const useParameterStore = defineStore("parameter", {
  state: () => ({
    sets: [
      {id: "1", name: "Оценки"},
    ],
    parameters: [
        {id: "1", title: "Оценки", comment: "Оценки студентов по предметам"},
        {id: "2", title: "Достижения", comment: "Достижения студентов"},
        {id: "3", title: "Дополнительные сведения", comment: "Дополнителные сведения"},
    ],
  }),
  getters: {

  },
  actions: {

  }
});