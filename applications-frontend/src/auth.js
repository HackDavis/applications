export default {
  methods: {
    loggedIn() {
      return this.$cookie.get("remember_token") != undefined;
    },
    getUserInfo() {
      this.$http.get("/api/user").then(
        response => {
          this.$user.setUser(response.body);
        },
        error => {
          if (error) {
            console.error(error);
            this.$user.setUser(null);
          }
        }
      );
    }
  }
};
