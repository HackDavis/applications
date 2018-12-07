import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./sass/styles.scss";
import auth from "./auth";

import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch, faEdit } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import "vue-virtual-scroller/dist/vue-virtual-scroller.css";
import VueVirtualScroller from "vue-virtual-scroller";

Vue.use(VueVirtualScroller);

library.add(faSearch, faEdit);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.prototype.$user = {
  _vm: new Vue({
    data: {
      user: null
    }
  }),
  setUser(user) {
    this._vm.$data.user = user;
  },
  getUser() {
    return this._vm.$data.user;
  }
};

Vue.mixin(auth);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
