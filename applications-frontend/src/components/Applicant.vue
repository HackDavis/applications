<template>
    <div class="container">
        <div class="columns is-multiline">

            <!-- Control panel -->
            <div id="ratings-column" class="column section-column has-background-white is-4">
                <center>

                    <!-- Rating control -->
                    <div class="subtitle is-3">Rating</div>

                    <div class="columns is-mobile is-multiline has-background-light is-gapless">
                        <div class="column">
                            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >1
                                <input v-on:click="current_rating = 1" type="radio" name="radio" checked="checked"/>
                                <div class="control__indicator"></div>
                            </label>
                        </div>

                        <div class="column">
                            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >2
                                <input v-on:click="current_rating = 2" type="radio" name="radio" checked="checked"/>
                                <div class="control__indicator"></div>
                            </label>
                        </div>

                        <div class="column">
                            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >3
                                <input v-on:click="current_rating = 3" type="radio" name="radio" checked="checked"/>
                                <div class="control__indicator"></div>
                            </label>
                        </div>

                        <div class="column">
                            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >4
                                <input v-on:click="current_rating = 4" type="radio" name="radio" checked="checked"/>
                                <div class="control__indicator"></div>
                            </label>
                        </div>

                        <div class="column">
                            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >5
                                <input  v-on:click="current_rating = 5" type="radio" name="radio" checked="checked"/>
                                <div class="control__indicator"></div>
                            </label>
                        </div>
                    </div>

                    <!-- Next applicant button -->
                    <a v-on:click="next_applicant" class="button is-primary is-medium" style="margin-top: 1em;">Next applicant</a>
                </center>
            </div>

            <!-- Information panel -->
            <div class="column has-background-light" style="border-radius: 1em;">
                <div class="subtitle is-3 has-text-centered">Applicant Information</div>
                <div class="container is-fluid has-background-light">
                    <div class="subtitle is-4">{{name}}:</div>
                    <div class="columns is-centered is-multiline">
                        <div class="column">
                            <div class="is-4">{{year}}</div>
                        </div>
                        <div class="column">
                            <div class="is-4">{{major}}</div>
                        </div>
                    </div>

                    <center>
                        <div class="subtitle is-4">Direct links</div>
                    </center>

                    <div class="columns is-mobile is-centered is-multiline">
                        <div class="column is-narrow">
                            <a  v-on:click="greet" class="button is-primary is-medium">Resume</a>
                        </div>

                        <div class="column is-narrow">
                            <a  v-on:click="greet" onclick="github" class="button is-primary is-medium">Github</a>
                        </div>

                        <div class="column is-narrow">
                            <a v-on:click="greet" class="button is-primary is-medium">LinkedIn</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  data: function() {
    return {
      name: "John Smith",
      year: "Freshman",
      major: "Computer Science",
      current_rating: 5
    };
  },

  methods: {
    next_applicant: function() {
      alert(
        "Next applicant! You rated this applicant " +
          this.current_rating +
          " out of 5."
      );
    },

    greet: function() {
      alert("Hello " + this.name + "!");
    }
  }
};
</script>
<style scoped>
#ratings-column {
  margin-top: 0;
}
</style>
