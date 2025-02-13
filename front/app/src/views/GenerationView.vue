<template>
  <h1 class="mb-3">Генерация progress-репортов</h1>

  <div class="my-2">

    <!-- Кнопки выбора и создания нового запроса -->
    <div class="p-2 d-flex align-items-center">
      <div class="me-2 d-flex" v-if="selectedRequest">
        <div class="me-2">Выбранный запрос: <b>{{ selectedRequest.name }}</b></div>
        <div class="icon-button" @click="clearSelectRequest"><i class="bi bi-dash-square-dotted"></i></div>
      </div>
      <div class="me-2" v-else>Выберите запрос или создайте новый</div>
      <button class="btn btn-primary ms-auto me-2" type="button" data-bs-toggle="offcanvas"
        data-bs-target="#canvasRequests" aria-controls="canvasRequests" @click="loadMyRequests">
        Выбрать
      </button>
      <app-button class="btn btn-success" @click="modalRequestShow">
        Создать
      </app-button>
    </div>

    <!-- Список запросов из canvas-меню -->
    <div ref="canvasRequests" class="offcanvas offcanvas-start" data-bs-scroll="true" tabindex="-1" id="canvasRequests"
      aria-labelledby="canvasRequestsLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="canvasRequestsLabel">Выберите запрос из списка</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="d-flex mb-2">
          <div class="ms-auto form-check form-switch">
            <input class="form-check-input" type="checkbox" role="switch" id="switchGlobalRequests"
              v-model="visibleGlobalRequest">
            <label class="form-check-label" for="switchGlobalRequests">
              <span v-if="!visibleGlobalRequest">Общие запросы</span>
              <span v-else>Мои запросы</span>
            </label>
          </div>
        </div>
        <div v-if="requestStore.requests.length" class="scrollable-list">
          <div class="list-group">
            <div v-for="request in requestStore.requests"
              class="list-group-item list-group-item-action d-flex align-items-center">
              <a href="javascript:void(0)" @click="loadRequestDetailed(request.id)">{{ request.name }}</a>
              <div @click="showToastDelete = true" class="ms-auto icon-button"><i class="bi bi-x-square"></i></div>
              <app-toast :show="showToastDelete" @confirm="deleteRequest(request.id)" @cancel="showToastDelete = false"
                :isLoading="isLoadingRequest">
                <div>Удалить запрос?</div>
              </app-toast>
            </div>
          </div>
        </div>
        <div v-else class="my-4">
          <span v-if="visibleGlobalRequest">Вы пока не создали ни одного запроса</span>
          <span v-else>Нет данных</span>
        </div>
      </div>
    </div>

    <!-- Модальное окно создания запроса -->
    <app-modal ref="appModalRequestRef" nameModal="requestModal" @cancel="cancelModalRequest">
      <template v-slot:header>Создание запроса</template>
      <template v-slot:body>
        <div class="text-start">
          <div class="mb-3">
            <label for="inputName" class="form-label">Название запроса</label>
            <input v-model="creatingRequest.name" type="text" class="form-control" id="inputName"
              aria-describedby="nameHelp">
          </div>
          <div class="mb-2 form-check">
            <input v-model="creatingRequest.is_global" type="checkbox" class="form-check-input" id="checkGlobal">
            <label class="form-check-label" for="checkGlobal">Глобально (смогут видеть другие пользователи)</label>
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <div class="ms-auto">
          <app-button type="button" class="btn btn-success me-2" @click="createRequest" :isLoading="isLoadingRequest">
            Сохранить
          </app-button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelModalRequest">
            Отменить
          </button>
        </div>
      </template>
    </app-modal>

  </div>

  <div v-if="selectedRequest">

    <!-- Блок настроек запроса -->
    <div class="my-3">
      <div class="accordion" id="accordionPanelsGenerate">

        <!-- Основные данные запроса -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#panelsGenerate-collapseBase" aria-expanded="true"
              aria-controls="panelsGenerate-collapseBase">
              Основные данные
            </button>
          </h2>
          <div id="panelsGenerate-collapseBase" class="accordion-collapse collapse">
            <div class="accordion-body">
              <div class="text-start">
                <div class="mb-3">
                  <label for="inputNameSelected" class="form-label">Название запроса</label>
                  <input v-model="selectedRequest.name" type="text" class="form-control" id="inputNameSelected"
                    aria-describedby="nameHelp">
                </div>
                <div class="mb-2 form-check">
                  <input v-model="selectedRequest.is_global" type="checkbox" class="form-check-input"
                    id="checkGlobalSelected">
                  <label class="form-check-label" for="checkGlobalSelected">Глобально (смогут видеть другие
                    пользователи)</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Контекст запроса -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#panelsGenerate-collapseContext" aria-expanded="true"
              aria-controls="panelsGenerate-collapseContext">
              Контекст запроса
            </button>
          </h2>
          <div id="panelsGenerate-collapseContext" class="accordion-collapse collapse">
            <div class="accordion-body">
              <app-textarea class="my-1" v-model="selectedRequest.context" name="context"
                placeholder="Введите содержимое контекста" />
            </div>
          </div>
        </div>

        <!-- Параметры запроса -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse"
              data-bs-target="#panelsGenerate-collapseParameters" aria-expanded="false"
              aria-controls="panelsGenerate-collapseParameters">
              Параметры запроса
            </button>
          </h2>
          <div id="panelsGenerate-collapseParameters" class="accordion-collapse collapse show">
            <div class="accordion-body">
              <div class="text-start" v-if="selectedRequest.parameters.length">
                <div v-for="p, index in selectedRequest.parameters" :key="p.id" class="py-2">
                  <div class="d-flex">
                    <div class="me-2 w-100">
                      <app-input class="my-1" v-model="p.title" name="title" placeholder="Введите название параметра" />
                      <app-textarea class="my-1" v-model="p.value" name="value"
                        placeholder="Введите содержимое параметра" />
                    </div>
                    <div class="ms-auto icon-button" @click="removeNewParameter(index)"><i class="bi bi-trash"></i>
                    </div>
                  </div>
                  <hr class="mb-0" v-if="selectedRequest.parameters.length != index + 1">
                </div>
              </div>
              <div v-else>
                Вы не добавили ни одного параметра
              </div>
              <div class="d-flex">
                <div class="icon-button" @click="addNewParameter"><i class="bi bi-plus-square"></i></div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Кнопки сохранения запроса -->
      <div class="d-flex" v-if="isEqualOriginalRequest">
        <div class="text-danger">Запрос изменён</div>
        <app-button class="btn btn-link m-0 p-0 ms-auto" @click="updateRequest(selectedRequest.id)"
          :isLoading="isLoadingRequest">
          Сохранить
        </app-button>
      </div>

    </div>

    <!-- Блок выполнения запроса на генерацию репорта -->
    <ul class="nav nav-tabs" id="generate" role="tablist">
      <li class="nav-item" role="presentation" v-for="el, index in generateModelElements" :key="index">
        <button class="nav-link" :class="{ 'active': index == 0 }" :id="`${el.nameElement}-tab`" data-bs-toggle="tab"
          :data-bs-target="`#${el.nameElement}-tab-pane`" type="button" role="tab"
          :aria-controls="`${el.nameElement}-tab-pane`" :aria-selected="index === 0">{{ el.name }}</button>
      </li>
    </ul>
    <div class="tab-content text-start" id="generateContent">
      <div v-for="el, index in generateModelElements" :key="index" class="tab-pane fade border border-top-0 p-2"
        :class="{ 'show active': index == 0 }" :id="`${el.nameElement}-tab-pane`" role="tabpanel"
        :aria-labelledby="`${el.nameElement}-tab`" tabindex="0">
        <div class="d-flex align-items-center my-2">
          <div class="">Модель нейронной сети: <b>{{ el.model }}</b></div>
          <app-button class="btn btn-success ms-auto" type="button" :isLoading="isLoadingGenerate"
            @click="generateReport(el.nameElement)">Генерировать</app-button>
        </div>
        <div class="border p-2 my-2">
          <div v-if="resultGenerateReport[`${el.nameElement}`]">{{ resultGenerateReport[`${el.nameElement}`].result }}
          </div>
          <div v-else><i>Нажмите на кнопку "Генерировать", чтобы увидеть результат...</i></div>
        </div>
        <div v-if="resultGenerateReport[`${el.nameElement}`]">Стомость запроса: <b>{{
          resultGenerateReport[`${el.nameElement}`].cost }} {{
              resultGenerateReport[`${el.nameElement}`].currency.toUpperCase() }}</b></div>
      </div>
    </div>

    <div class="text-start my-3">
      <h5>Комментарии</h5>

      <!-- Блок комментариев -->
      <app-crud-block v-model:locked="editingLocked" :requiredFields="['text']"
        :objects="selectedRequest.comments"
        :fetchCreate="commentStore.createComment.bind(null, selectedRequest.id)"
        :fetchUpdate="commentStore.updateComment.bind(null, selectedRequest.id)"
        :fetchDelete="commentStore.deleteComment.bind(null, selectedRequest.id)"
        @update="loadComments">

        <!-- Вывод существующих комментариев -->
        <template #data="{ obj, handleUpdate, locked }">
          <div>{{ obj.text }}</div>
        </template>

        <!-- Добавление нового комментария -->
        <template #new="{ newObject }">
          <div v-if="newObject">
            <app-textarea v-model="newObject.text" name="text" placeholder="Введите текст комментария" />
          </div>
        </template>

      </app-crud-block>
    </div>

  </div>
  <div v-else>

    <div class="d-flex align-items-center justify-content-center border rounded p-2 my-3">
      Не выбран запрос для генерации репорта
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { Offcanvas } from "bootstrap";

import { useRequestStore } from "@/stores/request";
const requestStore = useRequestStore();

import { useCommentStore } from "@/stores/comment";
const commentStore = useCommentStore();

import { useGenerateStore } from "@/stores/generate";
const generateStore = useGenerateStore();

// Переменная флага редактирования
const editingLocked = ref(false);

// Значения по-умолчанию для добавляемых параметров
const DEFAULT_PARAMETER = {
  title: "",
  comment: "",
}

// Значения по-умолчанию для создаваемых запросов
const DEFAULT_NEW_REQUEST = {
  name: "",
  is_global: false,
}

// Данные для вкладок нейронных сетей
const generateModelElements = [
  { name: "Yandex GPT", model: "Yandex GPT Lite", nameElement: "yandexgpt" },
  { name: "Chat GPT", model: "ChatGPT 4o", nameElement: "сhatgpt" },
  { name: "DeepSeek", model: "DeepSeek-Chat", nameElement: "deepseek" },
  { name: "Qwen (Alibaba)", model: "QWEN Plus", nameElement: "qwen" }
]

// Создаваемый запрос
const creatingRequest = ref({ ...DEFAULT_NEW_REQUEST });

// Загрузка запросов текущего пользователя
const loadMyRequests = async () => {
  await requestStore.loadMyRequests();
}

const visibleGlobalRequest = ref(true);

watch(() => visibleGlobalRequest.value, async (newValue) => {
  if (newValue) {
    requestStore.loadMyRequests();
  } else {
    requestStore.loadGlobalRequests();
  }
});

// Сравнение данных текущего запроса и первоначального
const isEqualOriginalRequest = computed(() => {
  const removeComments = (obj) => {
    if (!obj) return null; // Проверяем, чтобы obj не был null или undefined
    const { comments, ...rest } = obj;
    return rest;
  };

  return JSON.stringify(removeComments(selectedOriginalRequest.value)) !== JSON.stringify(removeComments(selectedRequest.value));
});


// РАБОТА С МОДАЛЬНЫМ ОКНОМ ДЛЯ СОЗДАНИЯ ЗАПРОСА

// Переменная-флаг на CRUD-операции с запросом
const isLoadingRequest = ref(false);

// Переменная модального окна для создания запроса
const appModalRequestRef = ref(null);

// Открытие модального окна создания запроса
const modalRequestShow = async () => {
  await appModalRequestRef.value?.modalShow();
}

// Подтверждение создания запроса
const createRequest = async () => {
  if (isLoadingRequest.value) return;

  isLoadingRequest.value = true;
  const new_request = await requestStore.createRequest(creatingRequest.value);
  isLoadingRequest.value = false;

  selectedRequest.value = await requestStore.loadRequestDetailed(new_request.id);
  selectedOriginalRequest.value = JSON.parse(JSON.stringify(selectedRequest.value));

  resultGenerateReport.value = {};

  creatingRequest.value = { ...DEFAULT_NEW_REQUEST }
  await appModalRequestRef.value?.modalHide();
}

// Отмена создания запроса и закрытие модального окна
const cancelModalRequest = async () => {
  await appModalRequestRef.value?.modalHide();
  creatingRequest.value = { ...DEFAULT_NEW_REQUEST }
}

// Переменная выбранного запроса, который редактируется
const selectedRequest = ref(null);
// Переменная выбранного запроса с оригинальным значением
const selectedOriginalRequest = ref(null);

// Загрузка детальной информации выбранного запроса
const loadRequestDetailed = async (id) => {
  selectedRequest.value = await requestStore.loadRequestDetailed(id);
  selectedOriginalRequest.value = JSON.parse(JSON.stringify(selectedRequest.value));
  offcanvasRequest.value.hide();
  resultGenerateReport.value = {};
}

// Очистка данных выбранного запроса
const clearSelectRequest = () => {
  selectedRequest.value = null;
  selectedOriginalRequest.value = JSON.parse(JSON.stringify(selectedRequest.value));
  resultGenerateReport.value = {};
}

// Обновление данных выбранного запроса
const updateRequest = async (id) => {
  if (isLoadingRequest.value) return;

  const data = {
    name: selectedRequest.value.name,
    context: selectedRequest.value.context,
    is_global: selectedRequest.value.is_global,
    parameters: selectedRequest.value.parameters
  }

  isLoadingRequest.value = true;
  const result = await requestStore.updateRequest(id, data);
  isLoadingRequest.value = false;

  if (!result) return;

  selectedRequest.value = { ...result }

  selectedOriginalRequest.value = JSON.parse(JSON.stringify(selectedRequest.value));
}

const showToastDelete = ref(false);

// Удаление запроса
const deleteRequest = async (id) => {
  if (isLoadingRequest.value) return;

  isLoadingRequest.value = true;
  const result = await requestStore.deleteRequest(id);
  isLoadingRequest.value = false;

  if (!result) return;

  if (id == selectedRequest.value?.id) {
    selectedRequest.value = null;
    selectedOriginalRequest.value = JSON.parse(JSON.stringify(selectedRequest.value));
  }

  await requestStore.loadMyRequests();
}

// Добавление параметра запроса
const addNewParameter = () => {
  selectedRequest.value.parameters.push(DEFAULT_PARAMETER);
}

// Удаление параметра запроса
const removeNewParameter = (index) => {
  selectedRequest.value.parameters.splice(index, 1);
};

// Переменная-флаг запроса на генерацию репорта
const isLoadingGenerate = ref(false);
// Результаты генерации репорта
const resultGenerateReport = ref({});

// Генерация репорта с помощью выбранного провайдера
const generateReport = async (provider) => {
  if (isLoadingGenerate.value) return;

  const data = {
    context: selectedRequest.value?.context,
    parameters: selectedRequest.value?.parameters,
  }

  isLoadingGenerate.value = true;
  const result = await generateStore.generateReport(provider, data);
  isLoadingGenerate.value = false;

  if (!result) return;

  resultGenerateReport.value[`${provider}`] = { ...result }
}

const loadComments = async () => {
  const result = await commentStore.loadRequestComments(selectedRequest.value.id);

  if (!result) return;

  selectedRequest.value.comments = [ ...result ];
}

// Переменные элементов бокового меню
const offcanvasRequest = ref(null);
const offcanvasElement = ref(null);

// Обработчик событий по клику на фон во время вызова бокового меню
const handleBackdropClick = (event) => {
  if (offcanvasElement.value && !offcanvasElement.value.contains(event.target)) {
    showToastDelete.value = false;
    offcanvasRequest.value.hide();
  }
};

onMounted(() => {
  offcanvasElement.value = document.getElementById("canvasRequests");
  if (offcanvasElement.value) {
    offcanvasRequest.value = new Offcanvas(offcanvasElement.value);

    // Добавление обработчика после открытия окна
    offcanvasElement.value.addEventListener("shown.bs.offcanvas", () => {
      document.addEventListener("click", handleBackdropClick, true);
    });

    // Удаление обработчика при закрытии окна
    offcanvasElement.value.addEventListener("hidden.bs.offcanvas", () => {
      document.removeEventListener("click", handleBackdropClick, true);
    });
  }
});

onUnmounted(() => {
  document.removeEventListener("click", handleBackdropClick, true);
});

</script>

<style scoped>
.icon-button {
  border: none;
  width: 20px;
  height: 20px;
}

.icon-button:hover {
  transform: scale(1.1);
  transition: transform 0.3s;
  cursor: pointer;
}

.scrollable-list {
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  padding: 5px;
}
</style>