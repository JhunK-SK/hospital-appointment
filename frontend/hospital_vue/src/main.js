import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import VCalendar from "v-calendar";
import VTooltipPlugin from "v-tooltip";

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App);

app.use(store).use(router, axios);
app.use(VCalendar, {});
app.use(VTooltipPlugin);
app.mount("#app");
