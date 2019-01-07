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
    <table class="table" @scroll.passive="scroll">
      <thead>
        <th>Name</th>
        <th>Email</th>
        <th>University</th>
        <th colspan="2">Score</th>
      </thead>
      <progress class="loading is-primary" v-if="loading" max="100"></progress>
      <tbody v-else>
        <tr v-for="item in paginatedItems" :key="item.id">
          <td>{{concatName(item.firstName, item.lastName)}}</td>
          <td>{{item.email}}</td>
          <td>{{item.university}}</td>
          <td>{{item.score > 0 ? item.score : "-"}}</td>
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
      searchTerm: "",
      maxViewIndex: 0
    };
  },
  components: {
    'progress-bar': ProgressWrapper
  },
  methods: {
    scroll(e) {
      if(e.target.scrollTop == e.target.scrollTopMax) {
        this.maxViewIndex += 10;
      }
    },
    concatName(first, last) {
      return first + " " + last;
    }
  },
  created: function() {
    this.$http
        .get("/api/user/scores")
        .then(response => {
          this.maxViewIndex = 20;

          if(response.data.length > 0) {
            this.applications = response.data;
            return;
          }

          this.applications.push({
            firstName: "You have not reviewed any applications.",
            lastName: "",
            email: "",
            score: 0,
            id: ""
          });
          
        }, error => console.error(error));
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
    paginatedItems: function() {
      return this.searchResults.slice(0, this.maxViewIndex);
    },
    loading: function() {
      return this.applications.length == 0;
    }
  },
  watch: {
    searchTerm: function() {
      this.maxViewIndex = 20;
    }
  }
};
</script>

<style scoped>
table {
  height: 600px;
  overflow-y: scroll;
  display: block
}
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
