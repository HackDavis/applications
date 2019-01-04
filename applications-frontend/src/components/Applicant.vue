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
            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse">1
              <input v-model="application.score" value="1" type="radio" name="radio" checked="checked">
              <div class="control__indicator" />
            </label>
          </div>

          <div class="column">
            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse">2
              <input v-model="application.score" value="2" type="radio" name="radio" checked="checked">
              <div class="control__indicator" />
            </label>
          </div>

          <div class="column">
            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse">3
              <input v-model="application.score" value="3" type="radio" name="radio" checked="checked">
              <div class="control__indicator" />
            </label>
          </div>

          <div class="column">
            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse">4
              <input v-model="application.score" value="4" type="radio" name="radio" checked="checked">
              <div class="control__indicator" />
            </label>
          </div>

          <div class="column">
            <label class="control control--radio column  is-flex is-align-center is-flex-column-reverse">5
              <input v-model="application.score" value="5" type="radio" name="radio" checked="checked">
              <div class="control__indicator" />
            </label>
          </div>
        </div>

        <!-- Feedback textarea -->
        <div class="no-margin subtitle is-3">Feedback</div>
        <div class="columns is-mobile is-multiline is-gapless">
          <textarea class="textarea has-fixed-size" v-model="application.feedback" placeholder="Optionally justify your rating here"></textarea>
        </div>


        <!-- Submit button -->
        <a v-on:click="score" :disabled="isInvalidScore" class="button is-primary is-medium" style="margin-top: 1em;">Submit</a>

        <!-- Skip button -->
        <a v-on:click="skip" class="button is-medium" style="margin-top: 1em;">Skip</a>

      </center>
    </div>

    <!-- Information panel -->

    <div class="column" style="border-radius: 1em;">
      <div class="subtitle is-3 has-text-centered">Applicant</div>
      <div class="container is-fluid">

        <div class="subtitle is-4">Direct links</div>
        <div class="columns is-mobile is-multiline is-gapless is-centered has-background-light">
          <div class="column is-narrow">
            <div v-if="resumeAnswer" class="column">
              <a :href="resumeAnswer.answer" class="button is-primary is-medium">Resume</a>
            </div>
          </div>
          <div v-for="linkAnswer in linkAnswers" :key="linkAnswer.id">
            <div class="column is-narrow">
              <a :href="linkAnswer.answer" class="button is-primary is-medium" rel="noopener" target="_blank">{{ linkAnswer.question.question }}</a>
            </div>
          </div>
        </div>

        <br>

        <div class="subtitle is-4">Interests</div>
        <div class="columns is-mobile is-multiline is-centered has-background-light">
          <span v-for="interest in interestAnswers" :key="interest.id" class="column is-centered is-narrow">{{ interest.answer }}</span>
        </div>

        <br>

        <div class="subtitle is-4">Short answers</div>

        <div v-for="essayAnswer in essayAnswers" :key="essayAnswer.id" class="columns is-centered">
          <div class="column is-6">
            <div class="is-5">{{ essayAnswer.question.question }}</div>
          </div>
          <div class="column has-background-light is-6" style="border-radius: 1em;">
            <div class="is-5">{{ essayAnswer.answer }}</div>
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
      answers: [],
      application: {}
    };
  },
  computed: {
    essayAnswers: function() {
      return this.filterAnswersByQuestionTypes(["essay"]);
    },
    interestAnswers: function() {
      return this.filterAnswersByQuestionTypes(["checkbox"]).filter(
        interest => interest.answer != ""
      );
    },
    linkAnswers: function() {
      const linkAnswers = this.filterAnswersByQuestionTypes(["link"]);
      return linkAnswers.filter(linkAnswer =>
        this.isValidUrl(linkAnswer.answer)
      );
    },
    resumeAnswer: function() {
      const resumeAnswers = this.filterAnswersByQuestionTypes(["resumeLink"]);
      if (resumeAnswers.length == 0) {
        return null;
      }
      return resumeAnswers[0];
    },
    isInvalidScore: function() {
      return !this.isValidScore();
    }
  },
  created: function() {
    this.next();
  },
  methods: {
    filterAnswersByQuestionTypes: function(validQuestionTypes) {
      return this.answers.filter(answer =>
        validQuestionTypes.includes(answer.question.question_type)
      );
    },
    isValidUrl: function(url) {
      try {
        new URL(url);
        return true;
      } catch (err) {
        return false;
      }
    },
    isValidScore: function() {
      return this.application.score >= 1 && this.application.score <= 5;
    },
    hasNoMoreApplications: function(response) {
      return response.status == 204;
    },
    setData: function(data) {
      this.answers = data.answers;
      this.application = data.application;
    },
    handleResponseSuccess(response) {
      if (this.hasNoMoreApplications(response)) {
        alert("No more applications left!");
        return;
      }

      this.setData(response.data);
    },
    handleResponseFailure(error) {
      console.error(error);
    },
    next: function() {
      let id = this.$route.params.id ? "/" + this.$route.params.id : "";

      this.$http
        .get("/api/review" + id)
        .then(this.handleResponseSuccess, this.handleResponseFailure);
    },
    skip: function() {
      this.$http
        .get("/api/review/skip")
        .then(this.handleResponseSuccess, this.handleResponseFailure);
    },
    score: function() {
      if (!this.isValidScore()) {
        return;
      }

      this.$http
        .post("/api/review/" + this.application.id + "/score", { score: this.application.score, feedback: this.application.feedback })
        .then(() => {
          this.$router.push("/review");
          this.next();
        }, this.handleResponseFailure);
    }
  }
};
</script>
<style scoped>
#ratings-column {
  margin-top: 0;
}
.control {
    font-size: 25px;
    position: relative;
    display: block;
    margin-bottom: 10px;
    cursor: pointer;
}

.control input {
    position: relative;
    z-index: -1;
    opacity: 0;
}

.control__indicator {
    width: 30px;
    height: 30px;
    background: #e6e6e6;
    position: relative;
}

.control--radio .control__indicator {
    border-radius: 50%;
}



/* Hover and focus states */
.control:hover input ~ .control__indicator,
.control input:focus ~ .control__indicator {
    background: #ccc;
}

/* Checked state */
.control input:checked + .control__indicator {
    background: #2aa1c0;
}

/* Hover state whilst checked */
.control:hover input:not([disabled]):checked + .control__indicator {
    background: #0e647d;
}

/* Disabled state */
.control input:disabled + .control__indicator {
    pointer-events: none;
    opacity: .6;
    background: #e6e6e6;
}

/* Check mark */
.control__indicator:after {
    position: relative;
    display: none;
    content: '';
}

/* Show check mark */
.control input:checked + .control__indicator:after {
    display: block;
}

/* Checkbox tick */
.control--checkbox .control__indicator:after {
    top: 4px;
    left: 8px;
    width: 3px;
    height: 8px;
    transform: rotate(45deg);
    border: solid #fff;
    border-width: 0 2px 2px 0;
}

/* Disabled tick colour */
.control--checkbox input:disabled + .control__indicator:after {
    border-color: #7b7b7b;
}

/* Radio button inner circle */
.control--radio .control__indicator:after {
    top: 25%;
    left: 25%;
    width: 50%;
    height: 50%;
    border-radius: 50%;
    background: #fff;
}

/* Disabled circle colour */
.control--radio input:disabled + .control__indicator:after {
    background: #7b7b7b;
}

.no-margin {
  margin: 0 !important;
}

</style>
