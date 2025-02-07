import { ApiService } from "@/services/api/api.service";

export class UserResource extends ApiService {
  constructor() {
    super();
  }

  getUserInfo() {
    return this._wrapper1(this.authClient.get, "GET", `/api/v1/user/me`)();
  }
}