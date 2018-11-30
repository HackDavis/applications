import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./sass/styles.scss";
import auth from "./auth";

import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch, faEdit } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faSearch, faEdit);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.mixin(auth);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
