import { GenerateResource } from "./generate.resource";
import { UserResource } from "./user.resource";
import { AuthResource } from "./auth.resource";

export default {
    resource: new GenerateResource(),
    user: new UserResource(),
    auth: new AuthResource(),
};