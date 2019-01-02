<template>
    <div class="columns">
        <div class="column is-half">
            <div class="field is-horizontal" v-for="setting in settings" :key="setting[0]">
                <div class="field-label">
                    <label class="label">{{setting[0]}}</label>
                </div>
                <div class="field">
                    <div class="control">
                        <input class="input" v-model="setting[1]"/>
                    </div>
                </div>
            </div>
            <button class="button" @click="submit">Submit</button>
            <button class="button" @click="reset">Reset</button>
        </div>
   </div>
</template>

<script>
export default {
    data () {
        return {
            settings: []
        };
    },
    created() {
        this.$http.get("/api/admin/settings").then(response => {
            delete response.body.id;
            delete response.body.last_modified;
            this.settings = Object.entries(response.body);
            this.originalSettings = _.cloneDeep(response.body);
        }, error => console.error(error));
    },
    methods: {
        reset() {
            this.settings = Object.entries(_.cloneDeep(this.originalSettings));
        },
        submit() {
            const body = this.settings.reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {});

            this.$http.put("/api/admin/settings", body).then(success => console.log(success), error => console.error(error));
        }
    }
};
</script>
