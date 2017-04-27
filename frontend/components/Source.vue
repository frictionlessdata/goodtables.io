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
    sourceURL() {
      if (this.job) {
        return `/${this.job.integration_name}/${this.source.name}`
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
                <a :href="sourceURL">{{ source.name }}</a>
              </h2>
              <JobListItem v-if="job" :job="job" :inSourcePanel="true"/>
              <div v-else class="alert alert-warning">
                <p>No jobs yet!</p>
                <p v-if="source.integration_name == 'github'">The first job will be triggered the next time someone pushes to the GitHub repository.</p>
                <p v-if="source.integration_name == 's3'">The first job will be triggered the next time someone upload or updates a file on the S3 bucket.</p>
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
