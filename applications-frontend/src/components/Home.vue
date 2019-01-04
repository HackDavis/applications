<template>
  <section>
    <div v-if="!loggedIn() || !$user.getUser()" class="container is-flex is-flex-column is-justify-center is-med">
      <div>
        <img 
          class="image 3by4" 
          src="@/assets/Pinguino-Linux.svg">
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

export default {
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
