<script>
import moment from 'moment'
import goodtablesUI from 'goodtables-ui'
import Messages from './Messages.vue'
import Job from './Job.vue'

export default {
  name: 'Source',
  props: {
    source: Object,
    job: Object,
    githubId: Number,
  },
  data () {
    return {
      viewClass: 'default-side-view',
    }
  },
  components: {
    Job,
    Messages,
  },
  computed: {
    statusClass() {
      return {
        error: this.job && this.job.status === 'error',
        failure: this.job && this.job.status === 'failure',
        success: this.job && this.job.status === 'success',
      }
    },
    sourceURL() {
      if (this.job) {
        return `/${this.job.integration_name}/${this.source.name}`
      }
    },
    jobHistory() {
      return this.source.job_history
        // TODO: job.source to data model level
        .map(job => ({...job, source: this.source}))
        .reverse()
    },
  },
  created() {
    // TODO: job.source to data model level
    this.job.source = this.source
  },
  mounted() {
    if (this.job.status !== 'error') {
      const element = document.getElementById('report')
      const component = goodtablesUI.Report
      const props = {report: this.job.report}
      goodtablesUI.render(component, props, element)
    }
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
        <section class="main report" :class="statusClass">
          <div class="inner">
            <Job view="report" :job="job" />
            <Messages
              v-if="job.status === 'error'"
              :messages="[['warning', job.error.message]]"
            />
            <div id="report"></div>
            <hr />
            <div>
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
                    <h3 class="aside-title">
                      <span class="text">
                        {{ source.job_history.length }}
                        {{ source.job_history.length > 1 ? 'jobs' : 'job' }}
                      </span>
                    </h3>
                  <Job
                    v-for="item of jobHistory"
                    :active="item.id === job.id"
                    :githubId="githubId"
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
