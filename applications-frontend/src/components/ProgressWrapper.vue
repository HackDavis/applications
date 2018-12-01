<template>
    <progress class="progress is-primary" max="100" :value="value"></progress>
</template>

<script>
export default {
    props: ['value']
};
</script>
