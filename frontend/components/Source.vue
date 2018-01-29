<script>
import moment from 'moment'
import goodtablesUI from 'goodtables-ui'
// import JobList from './JobList.vue'
// import JobListItem from './JobListItem.vue'
import Job from './Job.vue'

export default {
  name: 'Source',
  props: {
    source: Object,
    job: Object,
  },
  data () {
    return {
      viewClass: 'default-side-view',
    }
  },
  components: {
    Job,
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
  mounted() {
    const element = document.getElementById('report')
    const component = goodtablesUI.Report
    const props = {report: this.job.report}
    goodtablesUI.render(component, props, element)
  },
}
</script>

<template>
  <div :class="viewClass">
    <div class="primary-secondary source-view">
      <a class="integration" :class="`icon-${source.integration_name}`"></a>
      <h1>{{ source.name }}</h1>
      <div>

        <!-- Report -->
        <section class="main report" :class="`${job.status === 'valid' ? 'valid' : 'invalid'}`">
          <div class="inner">
            <Job view="latest" :job="job" />
            <div id="report"></div>
            <hr />
            <div class="badges">
              <h3>Image URL</h3>
              <pre>https://goodtables.io/badge/{{source.integration_name}}/{{source.name}}.svg</pre>
              <h3>Markdown</h3>
              <pre>[![goodtables.io](https://goodtables.io/badge/{{source.integration_name}}/{{source.name}}.svg)](https://goodtables.io/{{source.integration_name}}/{{source.name}})</pre>
              <h3>RST</h3>
              <pre>.. image:: https://goodtables.io/badge/{{source.integration_name}}/{{source.name}}.svg
:target: https://goodtables.io/{{source.integration_name}}/{{source.name}}</pre>
            </div>
            <a v-on:click="viewClass = 'default-side-view'" class="expand-view left">
              Expand sidebar
            </a>
          </div>
        </section>

        <!-- Jobs -->
        <section class="history aside">
          <div class="inner">
            <div>
              <div v-bar>
                <div>
                  <a
                    v-on:click="viewClass = 'collapsed-side-view'"
                    class="collapse-view right"
                  >
                    Collapse sidebar
                  </a>
                  <h3 class="aside-title"><span class="text">18 jobs</span></h3>
                  <Job
                    v-for="item of source.job_history.reverse()"
                    :active="item.id === job.id"
                    view="compact"
                    :job="item"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>
