import Vue from 'vue'
export default {
    data() {
        return {
            user: null
        }
    },
    methods: {
        loggedIn() {
            return this.$cookie.get("remember_token") != undefined;
        },
        getUserInfo() {
            this.$http.get("/api/user_info").then(response => {
                this.user = response.body    
            },
            error => {
                if(error) {
                    console.error(error)
                }
            });
        }
    },
    created() {
        if(this.loggedIn() && !this.user) {
            this.user = {}
            this.getUserInfo()
        }
        else if(!this.loggedIn()) {
            this.user = null
        }
    }
}