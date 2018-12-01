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
        <th>School</th>
        <th colspan="2">Score</th>
      </thead>
      <tbody>
        <tr v-for="item in searchResults" :key="item.id">
          <td>{{concatName(item.firstName, item.lastName)}}</td>
          <td>{{item.email}}</td>
          <td>{{item.school}}</td>
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
export default {
  data() {
    return {
      applications: [
        {
          firstName: "John",
          lastName: "Cena",
          email: "JC@ucdavis.edu",
          school: "UC Davis",
          id: 10,
          score: 5
        }
      ],
      searchTerm: ""
    };
  },
  computed: {
    searchResults: function() {
      return this.applications.filter(app => this.searchTerm === "" || 
        this.concatName(app.firstName, app.lastName).toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        app.email.includes(this.searchTerm.toLowerCase()) ||
        app.school.toLowerCase().includes(this.searchTerm.toLowerCase()));
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
