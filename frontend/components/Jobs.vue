<script>
import Job from './Job.vue'

export default {
  name: 'Jobs',
  props: {
    sources: Array,
  },
  components: {
    Job,
  },
  computed: {
    lastJobs() {
      return this.sources
        .filter(source => source.last_job)
        .map(source => source.last_job)
    },
  }
}
</script>

<template>
  <div class="only jobs">
    <h1>Jobs</h1>

    <div class="filter form-group">
      <label class="sr-only" for="keyword">Filter by keyword</label>
      <div class="input-group">
        <input type="text" class="form-control input-lg" id="keyword" placeholder="Filter by keyword">
        <div class="input-group-addon">
          <button><span class="icon-search"><i>Search</i></span></button>
        </div>
      </div>
    </div>

    <div class="source-list">
      <Job view="standard" :job="job" v-for="job of lastJobs" />
    </div>

  </div>
</template>
