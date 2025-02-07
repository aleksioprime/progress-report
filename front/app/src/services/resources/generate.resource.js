import { ApiService } from "@/services/api/api.service";

export class GenerateResource extends ApiService {
  constructor() {
    super();
  }
  async generateDeepSeek(data) {
    return this.$post(`/api/v1/generate/deepseek`, data);
  }

  async generateChatGPT(data) {
    return this.$post(`/api/v1/generate/chatgpt`, data);
  }

  async generateQWEN(data) {
    return this.$post(`/api/v1/generate/qwen`, data);
  }

  async generateYandexGPT(data) {
    return this.$post(`/api/v1/generate/yandexgpt`, data);
  }
}