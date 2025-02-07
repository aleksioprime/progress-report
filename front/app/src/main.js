import './style.css'
import logger from '@/common/helpers/logger';

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "@/router";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount("#app");

logger.info(`Загружены переменные окружения:`, import.meta.env)
