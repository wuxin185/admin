import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import SvgIcon from "@/icons";
// 国际化中文
import zhCn from "element-plus/es/locale/lang/zh-cn";

const app = createApp(App);
SvgIcon(app);
app.use(store);
app.use(router);
app.use(ElementPlus, {
  locale: zhCn,
});
app.mount("#app");
