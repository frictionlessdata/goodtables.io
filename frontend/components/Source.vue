<script>
import goodtablesUI from 'goodtables-ui'
// import JobList from './JobList.vue'
// import JobListItem from './JobListItem.vue'
import MessageGroup from './MessageGroup.vue'
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
    MessageGroup,
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
      <a class="integration icon-github"></a>
      <h1>okfn/test-data</h1>
      <div>

        <!-- Report -->
        <section class="main invalid report">
          <div class="inner">
            <div class="latest-job">
              <div class="icon">
                <span class="label label-danger">
                  <span class="icon-cross"><i>Invalid</i></span>
                </span>
              </div>
              <div class="status">
                <h2>
                  Job #16 failed
                  <small>8 days ago</small>
                </h2>
              </div>
              <div class="meta">
                <ul>
                  <li>
                    Pushed by <a>amercader</a>
                  </li>
                  <li>
                    <a>2928dd</a> on <a>master</a>
                  </li>
                </ul>
              </div>
            </div>
            <div id="report"></div>
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
                  <a v-on:click="viewClass = 'collapsed-side-view'" class="collapse-view right">Collapse sidebar</a>
                  <h3 class="aside-title"><span class="text">18 jobs</span></h3>
                  <Job view="compact" :job="job" v-for="job of source.job_history.reverse()" />
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>
