import Vue from 'vue'
import Router from 'vue-router'
import Applicant from './components/Applicant'

Vue.use(Router)

let auth = {
  loggedIn() {
    return true;
  }
}

let router = new Router({
  routes: [
    {
      path: 'applicants/:id',
      component: Applicant,
      meta: {
        requiresAuth: true
      }
    }
  ],
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!auth.loggedIn()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next() // make sure to always call next()!
  }
})

export default router
