<template>
  <h1 class="mb-3">Генерация репортов</h1>

  <div class="my-2">
    <div class="border p-2 d-flex align-items-center">
      <div class="me-2">Выберите запрос или создайте новый</div>
      <button class="btn btn-primary ms-auto me-2" type="button" data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasWithBothOptions" aria-controls="offcanvasWithBothOptions">Выбрать</button>
      <app-button class="btn btn-success" v-if="parameterStore.parameters.length">
        Создать
      </app-button>
      <!-- <app-dropdown v-model="selectedSet" :options="parameterStore.sets" name="parameterSet"
        placeholder="Не выбран набор" class="ms-auto" /> -->
    </div>

    <div class="offcanvas offcanvas-start" data-bs-scroll="true" tabindex="-1" id="offcanvasWithBothOptions"
      aria-labelledby="offcanvasWithBothOptionsLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasWithBothOptionsLabel">Выберите запрос из списка</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div v-for="set in parameterStore.sets">
          {{ set.name }}
        </div>
      </div>
    </div>


  </div>

  <div class="my-3">
    <div class="accordion" id="accordionPanelsGenerate">
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
            <textarea ref="textarea" class="form-control" placeholder="Введите содержимое контекста"
              :value="detailedSet.context" :id="`textarea-context-${detailedSet.id}`"></textarea>
          </div>
        </div>
      </div>
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
            <div class="text-start">
              <div v-for="p, index in parameterStore.parameters" :key="p.id" class="py-2">
                <div class="d-flex">
                  <div class="me-2 w-100">
                    <input type="text" class="form-control mb-1" :id="`input-${p.id}`"
                      placeholder="Введите название параметра" v-model="p.title">
                    <textarea ref="textarea" class="form-control" placeholder="Введите содержимое параметра"
                      :value="p.value" :id="`textarea-${p.id}`"></textarea>
                  </div>
                  <div class="ms-auto icon-button" @click="removeNewParameter(index)"><i class="bi bi-trash"></i></div>
                </div>
                <hr class="mb-0" v-if="parameterStore.parameters.length != index + 1">
              </div>
            </div>
            <div class="d-flex">
              <div class="icon-button" @click="addNewParameter"><i class="bi bi-plus-square"></i></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex">
      <app-button class="btn btn-link m-0 p-0 ms-auto" v-if="parameterStore.parameters.length">
        Сохранить настройки запроса
      </app-button>
    </div>
  </div>

  <ul class="nav nav-tabs" id="generate" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="yandexgpt-tab" data-bs-toggle="tab" data-bs-target="#yandexgpt-tab-pane"
        type="button" role="tab" aria-controls="yandexgpt-tab-pane" aria-selected="true">Yandex GPT</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="chatgpt-tab" data-bs-toggle="tab" data-bs-target="#chatgpt-tab-pane" type="button"
        role="tab" aria-controls="chatgpt-tab-pane" aria-selected="false">Chat GPT</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="deepseek-tab" data-bs-toggle="tab" data-bs-target="#deepseek-tab-pane" type="button"
        role="tab" aria-controls="deepseek-tab-pane" aria-selected="false">DeepSeek</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="owen-tab" data-bs-toggle="tab" data-bs-target="#owen-tab-pane" type="button"
        role="tab" aria-controls="owen-tab-pane" aria-selected="false">Owen (Alibaba)</button>
    </li>
  </ul>
  <div class="tab-content text-start" id="generateContent">
    <div class="tab-pane fade show active border border-top-0 p-2" id="yandexgpt-tab-pane" role="tabpanel"
      aria-labelledby="yandexgpt-tab" tabindex="0">
      <div class="d-flex align-items-start">
        <div class="">Генерация текста с помощью нейронной сети <b>Yandex GPT Lite</b></div>
        <app-button class="btn btn-success ms-auto" type="button"
          :isLoading="isLoadingGenerate">Генерировать</app-button>
      </div>
      <div class="border p-2 my-2">
        <i>Нажмите на кнопку "Генерировать", чтобы увидеть результат...</i>
      </div>
    </div>
    <div class="tab-pane fade border border-top-0 p-2" id="chatgpt-tab-pane" role="tabpanel"
      aria-labelledby="chatgpt-tab" tabindex="0">
      <div class="my-2">Генерация текста с помощью нейронной сети <b>ChatGPT 4o</b></div>
      <div class="border p-2 my-2">
        <i>Нажмите на кнопку "Генерировать", чтобы увидеть результат...</i>
      </div>
    </div>
    <div class="tab-pane fade border border-top-0 p-2" id="deepseek-tab-pane" role="tabpanel"
      aria-labelledby="deepseek-tab" tabindex="0">
      <div class="my-2">Генерация текста с помощью нейронной сети <b>DeepSeek-Chat</b></div>
      <div class="border p-2 my-2">
        <i>Нажмите на кнопку "Генерировать", чтобы увидеть результат...</i>
      </div>
    </div>
    <div class="tab-pane fade border border-top-0 p-2" id="owen-tab-pane" role="tabpanel" aria-labelledby="owen-tab"
      tabindex="0">
      <div class="my-2">Генерация текста с помощью нейронной сети <b>QWEN Plus</b></div>
      <div class="border p-2 my-2">
        <i>Нажмите на кнопку "Генерировать", чтобы увидеть результат...</i>
      </div>
    </div>
  </div>

  <div class="mt-2 mb-5">
    <textarea ref="textarea" class="form-control" placeholder="Оставьте отзыв о вашем запросе"
      :value="detailedSet.comment" :id="`textarea-comment-${detailedSet.id}`"></textarea>
    <div class="d-flex">
      <app-button class="btn btn-link m-0 p-0 ms-auto">
        Сохранить отзыв
      </app-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';

import { useParameterStore } from "@/stores/parameter";
const parameterStore = useParameterStore();

const isLoadingGenerate = ref(false);

const selectedSet = ref(null)

const detailedSet = ref({})

const DEFAULT_PARAMETER = {
  title: "",
  comment: "",
}

const addNewParameter = () => {
  parameterStore.parameters.push(DEFAULT_PARAMETER);
}

const removeNewParameter = (index) => {
  parameterStore.parameters.splice(index, 1);
};

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
</style>