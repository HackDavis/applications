<template>
  <nav 
    class="navbar has-shadow" 
    role="navigation" 
    aria-label="main navigation">
    <div class="container">
      <div class="navbar-brand">
        <router-link 
          class="branding navbar-item" 
          to="/">
          <img 
            class="image" 
            src="@/assets/logo.png">
          <h1 class="name is-size-2">HACK<b>DAVIS</b></h1>
        </router-link>
        <a 
          role="button" 
          class="navbar-burger" 
          aria-label="menu" 
          aria-expanded="false">
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
        </a>
      </div>
      <div class="navbar-menu">
        <div class="navbar-start">
          <router-link v-if="this.$user.getUser()"
            class="navbar-item is-size-5" 
            to="/review">Review</router-link>
          <router-link v-if="this.$user.getUser() && this.$user.getUser().role == 'admin'"
            class="navbar-item is-size-5"
            to="/configure">Configure</router-link>
          <router-link v-if="this.$user.getUser() && this.$user.getUser().role == 'admin'"
            class="navbar-item is-size-5"
            to="/upload">Upload</router-link>
          <router-link v-if="this.$user.getUser() && this.$user.getUser().role == 'admin'"
            class="navbar-item is-size-5"
            to="/settings">Settings</router-link>
        </div>
        <div class="navbar-end">
          <header-login/>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import HeaderLogin from './HeaderLogin.vue';

export default {
  components: {
      'header-login': HeaderLogin
  },
  created() {
    // the folling section of code was taken from bulma.io to manage the collapsible burger button
    document.addEventListener("DOMContentLoaded", function() {
      // Get all "navbar-burger" elements
      var $navbarBurgers = Array.prototype.slice.call(
        document.querySelectorAll(".navbar-burger"),
        0
      );

      // Check if there are any navbar burgers
      if ($navbarBurgers.length > 0) {
        // Add a click event on each of them
        $navbarBurgers.forEach(function($el) {
          $el.addEventListener("click", function() {
            // Get the target from the "data-target" attribute
            var target = $el.dataset.target;
            var $target = document.getElementById(target);

            // Toggle the class on both the "navbar-burger" and the "navbar-menu"
            $el.classList.toggle("is-active");
            $target.classList.toggle("is-active");
          });
        });
      }
    });
  }
};
</script>

<style scoped>
nav.navbar {
  margin-bottom: 1.5rem;
}

.branding {
  color: inherit !important;
}

.branding h1 {
  padding-left: 0.3em;
  padding-right: 0.3em;
}
</style>
