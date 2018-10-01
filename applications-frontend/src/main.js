import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./sass/styles.scss";
import auth from "./auth";

Vue.config.productionTip = false;

Vue.mixin(auth);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
