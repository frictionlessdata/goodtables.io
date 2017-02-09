<script>
import JobList from './JobList.vue'

export default {
  props: {
    githubJobs: Array,
    s3Jobs: Array,
  },
  components: {
    'app-joblist': JobList,
  },
}
</script>

<template>
<div class="container">
  <h1>Dashboard</h1>

  <h2>Jobs</h2>

  <h3>GitHub</h3>

  <div style="margin-bottom: 30px" class="row">
    <div style="float: right">
      <a href="/github/settings" class="btn btn-primary" style="width:120px;">Add repository</a>
    </div>
  </div>

  <template v-if="githubJobs">
    <app-joblist :jobs="githubJobs">
    <div style="margin-top: 20px"><a href="/github">Show more</a></div>
  </template>

  <template v-else>
    <p>No active or finished jobs.</p>
  </template>

  <hr />

  <h3>Amazon S3</h3>

  <div style="margin-bottom: 30px" class="row">
    <div style="float: right">
      <a href="/s3/settings" class="btn btn-primary" style="width:120px;">Add bucket</a>
    </div>
  </div>

  <template v-if="s3Jobs">
    <app-joblist :jobs="s3Jobs">
    <div style="margin-top: 20px"><a href="/s3">Show more</a></div>
  </template>

  <template v-else>
    <p>No active or finished jobs.</p>
  </template>

</div>
</template>

<style scoped>
</style>
