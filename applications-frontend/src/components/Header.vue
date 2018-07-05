<template>
    <nav class="navbar has-shadow" role="navigation" aria-label="main navigation">
        <div class="container">
            <div class="navbar-brand">
                <router-link class="navbar-item" to="/">
                    <img class="image is-32x32" src="@/assets/logo.png">
                </router-link>
                <h1 class="navbar-item is-size-2">Heck<b>Davis</b></h1>
                <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                </a>
            </div>
            <div class="navbar-menu">
                <div class="navbar-start">
                    <router-link class="navbar-item is-size-5" to="/review">Review</router-link>
                </div>
                <div class="navbar-end">
                    <a href="/login" class="navbar-item is-size-5">Login</a>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    created() {
        // the folling section of code was taken from bulma.io to manage the collapsible burger button
        document.addEventListener('DOMContentLoaded', function () {

            // Get all "navbar-burger" elements
            var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

            // Check if there are any navbar burgers
            if ($navbarBurgers.length > 0) {

                // Add a click event on each of them
                $navbarBurgers.forEach(function ($el) {
                    $el.addEventListener('click', function () {

                        // Get the target from the "data-target" attribute
                        var target = $el.dataset.target;
                        var $target = document.getElementById(target);

                        // Toggle the class on both the "navbar-burger" and the "navbar-menu"
                        $el.classList.toggle('is-active');
                        $target.classList.toggle('is-active');

                    });
                });
            }

        });
    }
}
</script>

<style scoped>
nav.navbar {
    margin-bottom: 1.5rem;
}
</style>
