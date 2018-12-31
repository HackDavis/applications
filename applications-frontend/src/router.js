import Vue from "vue";
import Router from "vue-router";
import Applicant from "./components/Applicant";
import Home from "./components/Home";
import Configure from './components/Configure';
import Settings from './components/Settings';
import Error from "./Error";
import VueResource from "vue-resource";
import VueCookie from "vue-cookie";

Vue.use(VueResource);
Vue.use(Router);
Vue.use(VueCookie);

Vue.http.interceptors.push(function() {
  return function(response) {
    if (response.status >= 400) {
      this.$router.push({
        name: "error",
        params: {
          id: response.status,
          message: response.body
        }
      });
    }
  };
});

let router = new Router({
  routes: [
    {
      path: "/review/:id?",
      component: Applicant,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/",
      component: Home
    },
    {
      path: "/error/:id?/:message?",
      name: "error",
      component: Error,
      props: true
    },
    {
      path: "/configure",
      component: Configure
    },
    {
      path: "/settings",
      component: Settings
    }
  ],
  mode: "history"
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (Vue.cookie.get("remember_token") == undefined) {
      location.href = "/login?next=" + to.fullPath;
    } else {
      next();
    }
  } else {
    next(); // make sure to always call next()!
  }
});

export default router;
