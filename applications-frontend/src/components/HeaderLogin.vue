<script>
export default {
    render() {
        if(this.loggedIn()) {
            return (
                <div class="navbar-item">
                    <img src={this.user.picture} />
                    <a class="is-size-5" href="/logout">Logout</a>
                </div>
            );
        }
        else {
            return (
                <a class="navbar-item is-size-5" href="/login">Login</a>
            );
        }
    }
}
</script>

<style>

</style>
