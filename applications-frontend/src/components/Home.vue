<template>
  <section>
    <div v-if="!loggedIn()" class="container is-flex is-flex-column is-justify-center is-med">
      <div>
        <img 
          class="image 3by4" 
          src="@/assets/Pinguino-Linux.svg">
        <h1 class="title">{{ quote }}</h1>
      </div>
      
    </div>
    <div v-else class="container is-flex is-flex-column is-align-center">
      <h1 class="title">List of Applicants</h1>
      <applications-table></applications-table>
    </div>
  </section>
</template>

<script>
import ApplicationsTable from './ApplicationsTable';

/**
 * picks a random element from an array
 *
 * @param {array} array - the array to select an element from
 * @returns {object} an element from the array or null if the array is empty
 */
function randomSelect(array) {
  if (!array || array.length == 0) return null;
  return array[Math.floor(Math.random() * array.length)];
}
export default {
  data() {
    return {
      quotes: ["Papers, Please.", "This is boring.", "World cub"],
      quote: ""
    };
  },
  mounted() {
    // demonstrate how to use lifecycle mounting, this will trigger whenever the page is relaoded
    this.quote = randomSelect(this.quotes);
  },
  components: {
    'applications-table': ApplicationsTable
  }
};
</script>

<style scoped>
.is-med {
  width: 20rem;
}
</style>
