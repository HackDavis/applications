import Vue from "vue";
export default {
  data() {
    return {
      user: null
    };
  },
  methods: {
    loggedIn() {
      return this.$cookie.get("remember_token") != undefined;
    },
    getUserInfo() {
      this.$http.get("/api/user").then(
        response => {
          this.user = response.body;
        },
        error => {
          if (error) {
            console.error(error);
            this.user = null;
          }
        }
      );
    }
  }
};
