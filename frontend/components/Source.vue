<script>
import Report from './Report.vue'
import SourceListItem from './SourceListItem.vue'

export default {
  name: 'Source_',
  props: {
    job: Object,
  },
  components: {
    Report,
    SourceListItem,
  },
  computed: {
    statusClass: function() {
      return {
        'valid': this.job.status === 'success',
        'invalid': this.job.status === 'failure',
        'error': this.job.status === 'error'
      }
    }
  }

}
</script>

<template>
  <div v-bind:class="statusClass">
    <div class="inner banner">
      <template v-if="job.integration_name === 'github'">
      <a class="icon-github integration"><i>GitHub</i></a>
      <h2 class="source-title">
          {{ job.integration_name }}/{{ job.conf.owner }}/{{job.conf.repo }}

      </h2>
      </template>

      <template v-else-if="job.integration_name === 's3'">
      <a class="icon-amazon integration"><i>Amazon S3</i></a>
      <h2 class="source-title">
          {{ job.integration_name }}/{{job.conf.bucket }}
      </h2>
      </template>
      <SourceListItem :job="job" :inSourcePanel="true"/>
    </div>
    <section class="inner">

      <div>
        <ul class="nav nav-tabs" role="tablist">
         <li role="presentation" class="active"><a href="#report" aria-controls="home" role="tab" data-toggle="tab">Report</a></li>
         <li role="presentation"><a href="#history" aria-controls="profile" role="tab" data-toggle="tab">Job history</a></li>
        </ul>
        <div class="tab-content">
          <div role="tabpanel" class="report tab-pane active" id="report">
            <ul class="meta">
              <li>
                Report calculated on {{ job.finished }}
              </li>
              <li>
                Source added: 21 Feb 2017
              </li>
            </ul>
            <Report :report="job.report" />
         </div>
         <div role="tabpanel" class="tab-pane" id="history">
           History here
         </div>
        </div>
      </div>
    </section>
  </div>
</template>

