<template>
  <div class="container">
    <h1 class="title">{{ this.$route.params.id }} error</h1>
    <h2 class="subtitle">Use the navbar to head back!</h2>
    <!-- super XSS vuln but ok -->
    <p v-html="message"/>

    <img :src="'https://http.cat/' + this.$route.params.id" onerror="this.style.display='none'"/>
  </div>
</template>

<script>
export default {
  props: ["message"]
};
</script>

<style>
</style>
