<script>
import goodtablesUI from 'goodtables-ui'
import Messages from './Messages.vue'
import Job from './Job.vue'

export default {
  name: 'Source',
  props: {
    baseUrl: String,
    source: Object,
    job: Object,
    githubId: Number,
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
    sourceUrl() {
      if (this.job) {
        return `${this.baseUrl}/${this.job.integration_name}/${this.source.name}`
      }
    },
    jobUrl() {
      if (this.sourceUrl) {
        return `${this.sourceUrl}/jobs/${this.job.number}`
      }
    },
    jobHistory() {
      return this.source.job_history
        // TODO: job.source to data model level
        .map(job => ({...job, source: this.source}))
        .reverse()
    },
    badgeImageUrl() {
      // TODO: Add branch
      return `${this.baseUrl}/badge/${this.source.integration_name}/${this.source.name}.svg`
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
  <div>
    <section class="primary-secondary source-view">
      <header>
        <a class="integration" :class="`icon-${source.integration_name}`"></a>
        <h1>
          <a :href="sourceUrl">{{ source.name }}</a>
          <a :href="jobUrl"><img :src="badgeImageUrl" :alt="job.status"></a>
        </h1>
      </header>
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
              <h3>Badge image URL</h3>
              <pre>{{badgeImageUrl}}</pre>
              <h3>Markdown</h3>
              <pre>[![goodtables.io]({{badgeImageUrl}})]({{sourceUrl}})</pre>
              <h3>RST</h3>
              <pre>.. image:: {{badgeImageUrl}}
:target: {{sourceUrl}}</pre>
            </div>
          </div>
        </section>

        <!-- Jobs -->
        <section class="history aside">
          <div class="inner">
            <div>
              <div v-bar>
                <div>
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
    </section>
  </div>
</template>
