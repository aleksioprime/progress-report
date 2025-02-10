import { GenerateResource } from "./generate.resource";
import { UserResource } from "./user.resource";
import { AuthResource } from "./auth.resource";
import { RequestResource } from "./request.resource";

export default {
    generate: new GenerateResource(),
    user: new UserResource(),
    auth: new AuthResource(),
    request: new RequestResource(),
};