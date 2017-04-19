<script>
import Report from './Report.vue'
import SourceListItem from './SourceListItem.vue'

export default {
  name: 'Source_',
  props: {
    source: Object,
  },
  components: {
    Report,
    SourceListItem,
  },
  computed: {
    statusClass() {
      return {
        valid: this.source.last_job && this.source.last_job.status === 'success',
        invalid: this.source.last_job && this.source.last_job.status === 'failure',
        error: this.source.last_job && this.source.last_job.status === 'error',
        info: !this.source.last_job,
      }
    },
  },

}
</script>

<template>
  <div v-bind:class="statusClass">
    <div class="inner banner">
      <template v-if="source.integration_name === 'github'">
      <a class="icon-github integration"><i>GitHub</i></a>
      </template>

      <template v-else-if="source.integration_name === 's3'">
      <a class="icon-amazon integration"><i>Amazon S3</i></a>
      </template>
      <h2 class="source-title">
          {{ source.name }}
      </h2>

      <SourceListItem :source="source" :inSourcePanel="true"/>
    </div>
    <section class="inner">

      <div>
        <ul class="nav nav-tabs" role="tablist">
         <li role="presentation" class="active"><a href="#report" aria-controls="home" role="tab" data-toggle="tab">Report</a></li>
         <li role="presentation"><a href="#history" aria-controls="profile" role="tab" data-toggle="tab">Job history</a></li>
        </ul>
        <div class="tab-content">
          <div role="tabpanel" class="report tab-pane active" id="report">

            <template v-if="source.last_job">
            <ul class="meta">
                Report calculated on {{ source.last_job.finished }}
              </li>
              <li>
                Source added: 21 Feb 2017
              </li>
            </ul>
            <Report :report="source.last_job.report" />
            </template>

            <template v-if="!source.last_job">
            <p>No jobs yet</p>
            </template>
         </div>
         <div role="tabpanel" class="tab-pane" id="history">
           History here
         </div>
        </div>
      </div>
    </section>
  </div>
</template>
