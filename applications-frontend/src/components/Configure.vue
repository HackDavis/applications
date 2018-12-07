<template>
    <div class="columns">
        <div class="column">
            <div class="field is-horizontal" v-for="question in question_weights" :key="question[0]">
                <div class="field-label">
                    <label class="label">{{question[0]}}</label>
                </div>
                <div class="field">
                    <div class="control">
                        <input class="input" v-model="question[1]"/>
                    </div>
                </div>
            </div>
            <button class="button" @click="submit">Done</button>
            <button class="button" @click="reset">Reset</button>
        </div>
        <div class="column">
            <div class="accordions">
                <div class="accordion" v-for="weight in answer_weights" :key="weight[0]">
                    <div class="accordion-header toggle">{{weight[1]}}</div>
                    <div class="accordion-body">
                        <div class="accordion-content">
                            <div class="control" v-for="w in weight[2]" :key="w.name">
                                <label class="label">{{w.name}}</label>
                                <input class="input" v-model="w.weight" />
                            </div>
                        </div>
                    </div>
                    
                </div>
            </div>            
        </div>
    </div>
</template>

<script>
import _ from 'lodash';
import bulmaAccordion from 'bulma-accordion/dist/js/bulma-accordion.min.js';

document.addEventListener("DOMContentLoaded", function(event) {
    bulmaAccordion.attach();
});

export default {
    data () {
        return {
            answer_weights: [],
            question_weights: []
        };
    },
    created() {
        this.$http.get("/api/admin/configure").then(response => {
            this.answer_weights = response.body.answer_weights;
            this.question_weights = response.body.question_weights;
            this.orig = _.cloneDeep(response.body);
        }, error => console.error(error));
    },
    methods: {
        reset() {
            this.answer_weights = _.cloneDeep(this.orig.answer_weights);
            this.question_weights = _.cloneDeep(this.orig.question_weights);
        },
        submit() {
            
        }
    }
};
</script>

<style>
    .accordion-body {
        overflow-y: scroll !important;
    }
</style>
