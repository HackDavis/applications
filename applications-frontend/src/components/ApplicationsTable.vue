<template>
  <div>
    <div class="field">
      <div class="control has-icons-left">
        <input v-model.lazy="searchTerm" class="input is-primary is-rounded" type="text" placeholder="Search" />
        <span class="icon is-small is-left">
          <font-awesome-icon :icon="['fa', 'search']" />
        </span>
      </div>
    </div>
    <table class="table">
      <thead>
        <th>Name</th>
        <th>Email</th>
        <th>University</th>
        <th colspan="2">Score</th>
      </thead>
      <progress class="loading is-primary" v-if="loading" max="100"></progress>
      <tbody v-else>
        <tr v-for="item in searchResults" :key="item.id">
          <td>{{concatName(item.firstName, item.lastName)}}</td>
          <td>{{item.email}}</td>
          <td>{{item.university}}</td>
          <td>{{item.score}}</td>
          <td>
            <router-link class="button" :to="'/review/' + item.id">
              <span class="icon">
                <font-awesome-icon icon="edit" />
              </span>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import ProgressWrapper from './ProgressWrapper';

export default {
  data() {
    return {
      applications: [],
      searchTerm: ""
    };
  },
  components: {
    'progress-bar': ProgressWrapper
  },
  created: function() {
    this.$http
        .get("/api/user/scores")
        .then(response => this.applications = response.data, error => console.error(error));
  },
  computed: {
    searchResults: function() {
      if(this.searchTerm === "") {
        return this.applications;
      }
      return this.applications.filter(app =>
        this.concatName(app.firstName, app.lastName).toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        app.email.includes(this.searchTerm.toLowerCase()) ||
        app.university.toLowerCase().includes(this.searchTerm.toLowerCase()));
    },
    loading: function() {
      return this.applications.length == 0;
    }
  },
  methods: {
    concatName: function(first, last) {
      return first + " " + last;
    }
  }
};
</script>

<style scoped>
td a.button {
  display: inline-block;
}
table tbody td {
  vertical-align: middle;
}
table tbody td:last-child {
  padding-left: 0;
}
</style>
