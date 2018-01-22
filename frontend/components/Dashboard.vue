<script>
import Job from './Job.vue'

export default {
  name: 'Dashboard',
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
    invalidLastJobs() {
      return this.lastJobs
        .filter(job => ['failure', 'error'].includes(job.status))
    },
  }
}
</script>

<template>
  <div class="dashboard">

    <!-- Actions -->
    <section class="actions">
      <h1>Action required</h1>
      <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
        <Job
          v-for="(job, index) of invalidLastJobs"
          :active="index === 0"
          view="extended"
          :job="job"
        />
      </div>
    </section>

    <!-- Jobs -->
    <section class="jobs">
      <div class="inner">
        <div>
          <div v-bar>
            <div>
              <h1>Jobs</h1>
              <div class="source-list">
                <Job view="standard" :job="job" v-for="job of lastJobs" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>
