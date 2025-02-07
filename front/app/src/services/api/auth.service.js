import { ApiService } from "@/services/api/api.service";
import { authClient } from "@/services/api/axios.clients";

export class AuthService extends ApiService {
  constructor() {
    super();
    this.client = authClient;
  }

  refresh(params) {
    return this.$post(`api/token/refresh/`, params);
  }

  logout(params) {
    return this.$post(`api/logout/`, params);
  }
}
