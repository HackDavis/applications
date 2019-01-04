<script>
export default {
    render() {
        if(this.loggedIn()) {
            return (
                <div class="navbar-item">
                    <img class="profile-pic" src={this.$user.getUser().picture} />
                    <a class="is-size-5" href="/logout">Logout</a>
                </div>
            );
        }
        else {
            return (
                <a class="navbar-item is-size-5" href="/login">Login</a>
            );
        }
    },
    created() {
        if (this.loggedIn() && !this.$user.getUser()) {
            this.$user.setUser({});
            this.getUserInfo();
        } else if (!this.loggedIn()) {
            this.$user.setUser(null);
        }
    }
};
</script>

<style>
.profile-pic {
  margin-right: 0.5em;
  border-radius: 50%;
}
</style>
