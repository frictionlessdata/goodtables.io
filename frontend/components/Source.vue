<script>
import Report from './Report.vue'
import SourceListItem from './SourceListItem.vue'

export default {
  name: 'Source',
  props: {
    source: Object,
    job: Object,
  },
  components: {
    Report,
    SourceListItem,
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
              <SourceListItem :source="source" :job="job" :inSourcePanel="true"/>
            </div>

            <section v-if="job" class="inner">

              <div>
                <ul class="nav nav-tabs" role="tablist">
                 <li role="presentation" class="active"><a href="#report" aria-controls="home" role="tab" data-toggle="tab">Report</a></li>
                 <li role="presentation"><a href="#history" aria-controls="profile" role="tab" data-toggle="tab">Job history</a></li>
                </ul>
                <div class="tab-content">
                  <div role="tabpanel" class="report tab-pane active" id="report">

                    <template v-if="job">
                      <div v-if="job.error" class="alert alert-warning">
                        {{ job.error.message }}
                      </div>
                      <Report v-if="job.report" :report="job.report" />
                      <ul class="meta">
                        <li>Report calculated on {{ job.finished }}</li>
                      </ul>
                    </template>

                    <template v-if="!job">
                      <p>No jobs yet</p>
                    </template>

                 </div>
                 <div role="tabpanel" class="tab-pane" id="history">

                   <div class="main-nav">
                     <SourceListItem v-for="job of source.job_history.reverse()" :source="source" :job="job" />
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
