<script>
import Job from './Job.vue'

export default {
  name: 'Jobs',
  props: {
    sources: Array,
  },
  data() {
    return {
      filter: '',
    }
  },
  components: {
    Job,
  },
  computed: {
    lastJobs() {
      return this.sources
        .filter(source => source.integration_name !== 'api')
        .filter(source => source.last_job)
        // TODO: job.source to data model level
        .map(source => ({...source.last_job, source}))
    },
    filteredLastJobs() {
      if (!this.filter) return this.lastJobs
      return this.lastJobs.filter(job => {
        const sourceName = `${job.source.integration_name}/${job.source.name}`
        return sourceName.includes(this.filter)
      })
    }
  }
}
</script>

<template>
  <div class="only jobs">
    <h1>Jobs</h1>

    <!-- Filter -->
    <div class="filter form-group">
      <label class="sr-only" for="keyword">Filter by keyword</label>
      <div class="input-group">
        <input
          v-model="filter"
          type="text"
          class="form-control input-lg"
          id="keyword"
          placeholder="Filter by keyword"
        >
        <div class="input-group-addon">
          <button><span class="icon-search"><i>Search</i></span></button>
        </div>
      </div>
    </div>

    <!-- Jobs -->
    <div v-if="filteredLastJobs.length" class="source-list">
      <Job view="standard" :job="job" v-for="job of filteredLastJobs" />
    </div>
    <div v-else class="source-item" style="padding-top: 1em;">
      There are no jobs yet.
      Add a <a href="/settings">source</a> to get started.
    </div>

  </div>
</template>
