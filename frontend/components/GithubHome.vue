<script>
import JobList from './JobList.vue'

export default {
  name: 'GithubHome',
  props: {
    org: String,
    repo: String,
    jobs: Array,
  },
  components: {
    JobList,
  },
}
</script>

<template>
<div class="container">

  <h1>GitHub Jobs</h1>

  <h2 v-if="org">{{ org }}<span v-if="repo">/{{ repo }}</span></h2>

  <div v-if="!repo" style="margin-bottom: 30px" class="row">
    <div style="float: right">
      <a href="/github/settings" class="btn btn-primary" style="width:120px;">Add repository</a>
    </div>
  </div>

  <template v-if="jobs">
    <JobList :jobs="jobs" />
  </template>

  <template v-else>
    <p>No active or finished jobs.</p>
  </template>

</div>
</template>

<style scoped>
</style>
