<script>
import Report from './Report.vue'
import JobList from './JobList.vue'
import JobListItem from './JobListItem.vue'

export default {
  name: 'Source',
  props: {
    source: Object,
    job: Object,
  },
  components: {
    Report,
    JobList,
    JobListItem,
  },
  computed: {
    statusClass() {
      return {
        valid: this.job && this.job.status === 'success',
        invalid: this.job && this.job.status === 'failure',
        error: this.job && this.job.status === 'error',
        info: !this.job,
      }
    },
  },

}
</script>

<template>
  <div class="app">
    <div class="inner">
      <div class="default">

        <main class="source-view">
          <div v-bind:class="statusClass">

            <div class="inner banner">
              <template v-if="source.integration_name === 'github'">
              <a :href="`https://github.com/${source.name}`" class="icon-github integration"><i>GitHub</i></a>
              </template>
              <template v-else-if="source.integration_name === 's3'">
              <a :href="`https://console.aws.amazon.com/s3/buckets/${source.name}`" class="icon-amazon integration"><i>Amazon S3</i></a>
              </template>
              <h2 class="source-title">
                {{ source.name }}
              </h2>
              <JobListItem v-if="job" :job="job" :inSourcePanel="true"/>
              <div v-else class="alert alert-warning">
                No jobs yet
              </div>
            </div>

            <section v-if="job" class="inner">

              <div>

                <ul class="nav nav-tabs" role="tablist">
                 <li role="presentation" class="active"><a href="#report" aria-controls="home" role="tab" data-toggle="tab">Report</a></li>
                 <li role="presentation"><a href="#history" aria-controls="profile" role="tab" data-toggle="tab">Job history</a></li>
                </ul>

                <div class="tab-content">
                  <div role="tabpanel" class="report tab-pane active" id="report">
                    <div v-if="job.error" class="alert alert-warning">
                      {{ job.error.message }}
                    </div>
                    <Report v-if="job.report" :report="job.report" />
                    <ul class="meta">
                      <li>Report calculated on {{ job.finished }}</li>
                    </ul>
                  </div>

                 <div role="tabpanel" class="tab-pane" id="history">
                   <div class="main-nav">
                     <JobList :jobs="source.job_history.reverse()" />
                   </div>
                 </div>

                </div>
              </div>
            </section>

          </div>
        </main>

      </div>
    </div>
  </div>
</template>
