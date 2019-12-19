<template>
  <div class="container">
    <progress class="progress loading is-primary" v-if="waiting" max="100"></progress>
    <form v-else class="form" enctype="multipart/form-data" method="POST">
      <div class="field">
        <label class="label">Applicants: </label>
        <div class="file has-name">
          <label class="file-label">
            <input id="file" class="file-input" type="file" @change="fileChanged" required />
            <span class="file-cta">
              <span class="file-icon">
                <font-awesome-icon :icon="['fa', 'file-csv']" />
              </span>
              <span class="file-label">
                Choose a file…
              </span>
            </span>
            <span class="file-name">{{this.fileName}}</span>
          </label>
        </div>
      </div>
      <div class="field">
        <label class="label">Mode: </label>
        <div class="control">
          <label class="checkbox">
            <input type="checkbox" v-model="isJoin">
            Join
          </label>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <button type="button" class='button is-primary' @click="submit">Submit</button>
        </div>
      </div>
    </form>
    <a id="export-button" href="/api/admin/export" class="button">Export Scores</a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isJoin: true,
      fileName: "",
      waiting: false
    };
  },
  methods: {
    submit() {
      let formdata = new FormData();
      let theFile = document.getElementById("file");
      formdata.append("applicants", theFile.files[0]);

      let route = "";
      if(this.isJoin) {
        route = '/api/admin/load';
      }
      else {
        route = '/api/admin/reload';
      }

      this.waiting = true;
      this.$http.post(route, formdata, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.waiting = false;
        console.log(response);
      }, error => {
        this.waiting = false;
        console.error(error);
      });
    },
    fileChanged(e) {
      this.fileName = e.target.files[0].name;
    }
  }
};
</script>

<style>

#export-button {
  margin-top: 20px;
}

</style>
