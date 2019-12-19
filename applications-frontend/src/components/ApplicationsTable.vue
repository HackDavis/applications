<template>
  <div>
    <div class="is-flex is-justify-between summary">
      <div class="summary-left">
        <h1 class="subtitle is-4">Your Progress</h1>
        <progress class="progress is-primary" :value="progress.self.done" :max="progress.self.total"></progress>
        <p class="progress-numbers">{{progress.self.done}} completed of {{progress.self.total}}</p>
        <h2 class="subtitle is-4">Team Progress</h2>
        <progress class="progress is-primary" :value="progress.team.done" :max="progress.team.total"></progress>
        <p class="progress-numbers">{{progress.team.done}} completed of {{progress.team.total}}</p>
      </div>
      <div class="summary-right">
        <h1 v-if="isAdmin" class="title has-text-centered">Applications By User</h1>
        <table v-if="isAdmin" class="table" @scroll.passive="scroll">
          <thead>
            <th>User</th>
            <th>Apps scored</th>
            <th>Apps rescored by admin</th>
            <th>Apps rescored as admin</th>
          </thead>
          <tbody>
            <tr v-for="item in applicationsByUser" :key="item[0]">
              <td>{{item[0]}}</td>
              <td>{{item[1].totalScored}}</td>
              <td>{{item[1].scoredLockedByAdmin}}</td>
              <td>{{item[1].scoredLockedAsAdmin}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <h1 class="title has-text-centered">Applications</h1>
    <div class="field">
      <div class="control has-icons-left">
        <input v-model.lazy="searchTerm" class="input is-primary is-rounded" type="text" placeholder="Search" />
        <span class="icon is-small is-left">
          <font-awesome-icon :icon="['fa', 'search']" />
        </span>
      </div>
    </div>
    <table id="applications-table" class="table" @scroll.passive="scroll">
      <thead>
        <th>Name</th>
        <th>Email</th>
        <th>University</th>
        <th colspan="2">Score</th>
        <th v-if="isAdmin">Assigned to</th>
        <th>Locked by</th>
      </thead>
      <progress class="progress loading is-primary" v-if="loading" max="100"></progress>
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
          <td v-if="isAdmin">{{item.assignedToEmail}}</td>
          <td>{{item.lockedByEmail}}</td>
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
      maxViewIndex: 0,
      progress: {
        team: {
          done: 0,
          total: 1
        },
        self: {
          done: 0,
          total: 1
        }
      }
    };
  },
  components: {
    'progress-bar': ProgressWrapper
  },
  methods: {
    isUserAdmin: function() {
      const user = this.$user.getUser();
      return user && user.role == 'admin';
    },
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
    this.$http.get("/api/user/progress").then(response => this.progress = response.data, error => console.error(error));
    this.$http
        .get("/api/user/scores")
        .then(response => {
          this.maxViewIndex = 20;

          if(response.data.length > 0) {
            this.applications = response.data.map(element => {
              if(element.lockedByEmail) element.lockedByEmail = element.lockedByEmail.split("@")[0];
              if(element.assignedToEmail) element.assignedToEmail = element.assignedToEmail.split("@")[0];
              return element;
            });
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
    isAdmin: function() {
      return this.isUserAdmin();
    },
    searchResults: function() {
      if(this.searchTerm === "") {
        return this.applications;
      }

      const searchTerm = this.searchTerm.toLowerCase();
      const isAdmin = this.isUserAdmin();

      return this.applications.filter(app => {
        const concatedName = this.concatName(app.firstName, app.lastName);
        
        return (concatedName.toLowerCase().includes(searchTerm) ||
        (app.email && app.email.includes(searchTerm)) ||
        (app.university && app.university.toLowerCase().includes(searchTerm)) ||
        (app.score && app.score.toString().includes(searchTerm)) ||
        (isAdmin && app.assignedToEmail && app.assignedToEmail.toLowerCase().includes(searchTerm)) ||
        (app.lockedByEmail && app.lockedByEmail.toLowerCase().includes(searchTerm)));
      })
    },
    paginatedItems: function() {
      return this.searchResults.slice(0, this.maxViewIndex);
    },
    loading: function() {
      return this.applications.length == 0;
    },
    applicationsByUser: function() {
      const user = this.$user.getUser();
      const initialState = {
        totalScored: 0,
        scoredLockedByAdmin: 0,
        scoredLockedAsAdmin: 0
      }

      const applicationsByUser = this.applications.reduce((applicationsByUser, application) => {
        const assignedToEmail = application.assignedToEmail;
        if(!assignedToEmail) return applicationsByUser;
        if (!applicationsByUser[assignedToEmail]) {
          applicationsByUser[assignedToEmail] = Object.assign({}, initialState);
        }

        const lockedByEmail = application.lockedByEmail;
        if (lockedByEmail && !applicationsByUser[lockedByEmail]) {
          applicationsByUser[lockedByEmail] = Object.assign({}, initialState);
        }

        if (application.score != 0) {
          applicationsByUser[assignedToEmail].totalScored += 1;
          if (lockedByEmail) {
            applicationsByUser[assignedToEmail].scoredLockedByAdmin += 1;
            applicationsByUser[lockedByEmail].scoredLockedAsAdmin += 1;
          }
        }

        return applicationsByUser;
        }, {});
      
      return Object.entries(applicationsByUser);
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
table#applications-table {
  height: 600px;
  overflow-y: scroll;
  display: block;
  margin-bottom: 50px !important;
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

progress.progress {
  max-width: 300px;
  width: 100%;
  margin-bottom: 0.5rem;
}

.progress-numbers {
  margin-bottom: 1.5rem
}

.summary {
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.summary .summary-left {
  flex-grow: 1;
  padding: 15px;
  min-width: 150px;
}
.summary .summary-right {
  flex-shrink: 0;
  padding: 15px;
}
</style>
