import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/GenerationView.vue"),
    meta: {
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/callback",
    name: "callback",
    component: () => import("@/views/Callback.vue"),
    meta: {},
  }
]