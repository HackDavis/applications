<template>
    <div class="container">
        <h1 class="title">Wow you hit a {{this.$route.params.id}} error.</h1>
        <h2 class="subtitle">What were you thinking?</h2>
        <!-- super XSS vuln but ok -->
        <p v-html="message"></p>
    </div>
</template>

<script>
export default {
    props: ['message']
}
</script>

<style>

</style>
