<template>
  <div class="container">
    <div class="columns is-multiline">
      <div v-for="(stats, question) in answers" :key="stats[0][3]" class="column is-one-third">
        <div class="card">
          <header class="card-header">
            <h1 class="card-header-title">{{question}}</h1>
          </header>
          <div class="card-content">
            <div class="content">
              <ul>
                <li v-for="stat in stats" :key="stat[1]">{{stat[1]}}: {{stat[0] * 100 / total}}%</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      total: 1,
      answers: {}
    };
  },
  created() {
    this.$http.get("/api/admin/demographics").then(response => {
      this.total = response.data.total;
      let answer_map = {};
      response.data.answers.forEach(element => {
        if(answer_map[element[2]] === undefined) {
          answer_map[element[2]] = [];
        }
        answer_map[element[2]].push(element)
      })

      this.answers = answer_map;
    }, error => console.error(error));
  }
}
</script>

<style>

</style>
