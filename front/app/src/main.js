import '@/assets/css/style.css'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

import logger from '@/common/helpers/logger';

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "@/router";

import components from '@/common/components/index.js';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

Object.entries(components).forEach(([name, component]) => {
    app.component(name, component);
  });

app.mount("#app");

logger.info(`Загружены переменные окружения:`, import.meta.env)
