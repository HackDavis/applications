<template>
    <div>
        <div class="container">
            <div class="columns is-multiline">
                <div v-for="(stats, question) in answers" :key="stats[0][3]" class="column is-one-third">
                    <div class="card">
                    <header class="card-header">
                        <h1 class="card-header-title">{{question}}</h1>
                    </header>
                    <div class="card-content">
                        <div class="content">
                            <ul>
                                <li v-for="stat in stats" :key="stat[1]">{{stat[1]}}: {{(stat[0] * 100 / total).toFixed(2)}}%</li>
                            </ul>
                        </div>
                    </div>
                </div>
                </div>
            </div>
        </div>
        <div class="columns">
            <div class="column">
                <div class="field is-horizontal" v-for="question in question_weights" :key="question[0]">
                    <div class="field-label">
                        <label class="label">{{question[1]}}</label>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input class="input" v-model="question[2]"/>
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
                            <div class="accordion-content" @click.stop="dummy">
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
    </div>
</template>

<script>
import _ from 'lodash';
import bulmaAccordion from 'bulma-accordion/dist/js/bulma-accordion.min.js';

export default {
    data () {
        return {
            answer_weights: [],
            question_weights: [],
            total: 1,
            answers: {}
        };
    },
    created() {
        this.reloadStats();
        this.loadConfiguration().then(() => {
            bulmaAccordion.attach();
        });
    },
    methods: {
        reset() {
            this.answer_weights = _.cloneDeep(this.orig.answer_weights);
            this.question_weights = _.cloneDeep(this.orig.question_weights);
        },
        loadConfiguration() {
            return new Promise((resolve, reject) => {
                this.$http.get("/api/admin/configure").then(response => {
                    this.answer_weights = response.body.answer_weights;
                    this.question_weights = response.body.question_weights;
                    this.orig = _.cloneDeep(response.body);
                    resolve(response);
                }, error => reject(error));
            });
        },
        submit() {
            let new_question_weights = [];
            for(let i = 0; i < this.question_weights.length; i++){
                if(this.question_weights[i][2] != this.orig.question_weights[i][2]) {
                    new_question_weights.push(this.question_weights[i]);
                }
            }

            let new_answer_weights = _.reduce(_.zip(this.answer_weights, this.orig.answer_weights), (acc, n) => {
                console.log(n);
                let new_weights = _.reduce(_.zip(n[0][2], n[1][2]), (acc, m) => {
                    if(m[0].weight != m[1].weight) {
                        acc.push(m[0]);
                        return acc;
                    }
                    return acc;
                }, []);
                if(new_weights.length > 0) {
                    acc.push([n[0][0], n[0][1], new_weights]);
                    return acc;
                }
                return acc;
            }, []);
            

            let update = {
                answer_weights: new_answer_weights,
                question_weights: new_question_weights
            };

            this.$http.put("/api/admin/configure", update).then(success => {
                console.log(success);
                this.reloadStats();
                this.loadConfiguration();
            }, error => console.error(error));
        },
        dummy() {},
        reloadStats() {
            this.$http.get("/api/admin/demographics").then(response => {
                this.total = response.data.total;
                let answer_map = {};
                response.data.answers.forEach(element => {
                if(answer_map[element[2]] === undefined) {
                    answer_map[element[2]] = [];
                }
                answer_map[element[2]].push(element);
                });

                this.answers = answer_map;
            }, error => console.error(error));
        }
    }
};
</script>

<style>
    .accordion-body {
        overflow-y: scroll !important;
    }
</style>
