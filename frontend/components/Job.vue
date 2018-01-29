<script>
import moment from 'moment'
import {removeBaseUrl} from '../helpers'

export default {
  name: 'Job',
  props: {
    job: Object,
    view: String,
    active: Boolean,
  },
  computed: {
    statusPanelClass() {
      return {
        'panel-success': (this.job && this.job.status === 'success'),
        'panel-danger': (this.job && this.job.status === 'failure'),
        'panel-warning': (this.job && this.job.status === 'error'),
        'panel-info': !this.job,
      }
    },
    statusLabelClass() {
      return {
        'label-success': (this.job && this.job.status === 'success'),
        'label-danger': (this.job && this.job.status === 'failure'),
        'label-warning': (this.job && this.job.status === 'error'),
        'label-info': !this.job,
      }
    },
    statusIconClass() {
      return {
        'icon-checkmark': (this.job && this.job.status === 'success'),
        'icon-cross': (this.job && this.job.status === 'failure'),
      }
    },
    integrationIconClass() {
      return {
        'icon-github': this.job.integration_name === 'github',
        'icon-amazon': this.job.integration_name === 's3',

      }
    },
    sourceName() {
      if (this.job.integration_name === 'github') {
        return `${this.job.conf.owner}/${this.job.conf.repo}`
      } else if (this.job.integration_name === 's3') {
        return this.job.conf.bucket
      }
    },
    internalURL() {
      if (!this.inSourcePanel) {
        return `/${this.job.integration_name}/${this.sourceName}/jobs/${this.job.number}`
      }
    },
    externalURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.sourceName}/tree/${this.job.conf.sha}`
      } else if (this.job.integration_name === 's3') {
        return `https://console.aws.amazon.com/s3/buckets/${this.sourceName}`
      }
    },
    jobTitle() {
      if (this.job.integration_name === 'github') {
        if (this.job.conf.is_pr) {
          return this.job.conf.pr_title
        }
        return this.job.conf.commit_message
      } else if (this.job.integration_name === 's3') {
        return this.job.conf.bucket
      }
    },
    jobTimeStamp() {
      return moment(this.job.created).fromNow()
    },
    githubUserURL() {
      return `https://github.com/${this.job.conf.author_name}`
    },
    githubBranchURL() {
      return `https://github.com/${this.sourceName}/tree/${this.job.conf.branch_name}`
    },
    githubCommitURL() {
      return `https://github.com/${this.sourceName}/commit/${this.job.conf.sha}`
    },
    githubPullRequestURL() {
      return `https://github.com/${this.sourceName}/pull/${this.job.conf.pr_number}`
    },
    invalidFiles() {
      const files = []
      for (const table of this.job.report.tables) {
        if (table.valid) continue
        const rows = {}
        rows[1] = table.headers
        for (const error of table.errors) {
          if (error.row) rows[error['row-number']] = error.row
        }
        // TODO: add other rows
        files.push({
          name: removeBaseUrl(table.source),
          errorCount: table['error-count'],
          rows,
        })
      }
      return files
    },
    errorCount() {
      return this.job.report['error-count']
    },
    fileName() {
      // TODO: implement
      return 'test'
    },
    commitHash() {
      return this.job.conf.sha ? this.job.conf.sha.slice(0, 6) : ''
    },
    commitBranch() {
      return this.job.conf.branch_name
    },
    commitAuthor() {
      return this.job.conf.author_name
    },
    commitMessage() {
      return this.job.conf.commit_message.split('\n')[0]
    },
  },
}
</script>

<template>

  <!-- Compact -->
  <div v-if="view === 'compact'">
    <div class="source-item" :class="{active}">
      <div class="panel panel-success">
        <div :class="job.integration_time">

          <!-- User/message -->
          <span class="source">
            <a class="avatar" :href="internalURL">
              <img src="https://avatars1.githubusercontent.com/u/200230?s=48" alt="" />
            </a>
            <h3 class="panel-title">{{ commitMessage }}</h3>
          </span>

          <!-- Statistics -->
          <a class="job" :href="internalURL">
            <span class="jobcount" v-if="commitHash">
              <span class="jobnumber">{{ commitHash }}</span>
            </span>
            <span class="label label-success">
              <span class="icon-checkmark"><i>{{ job.status }}</i></span>
            </span>
            <span class="time">{{ jobTimeStamp }}</span>
          </a>

        </div>
      </div>
    </div>
  </div>

  <!-- Standard -->
  <div v-else-if="view === 'standard'">
    <div class="source-item">
      <div class="panel panel-success">
        <div :class="job.integration_name">

          <!-- Status/name -->
          <a :href="internalURL" class="source">
            <span class="status">{{ job.status }} </span>
            <span class="label" :class="statusLabelClass">
              <span :class="statusIconClass"><i>{{ job.status }}</i></span>
            </span>
            <h3 class="panel-title">
              {{ job.integration_name }}/{{ sourceName }}
              <span class="jobnumber">#{{ job.number }}</span>
            </h3>
          </a>

          <!-- Statistics -->
          <a :href="internalURL" class="job">
            <span class="jobcount">
              <span class="jobnumber"> #{{ job.number }}</span>
              <span class="jobid"> ({{ commitHash }})</span>
            </span>
            <span class="icon-clock"></span>
            <span class="time">{{ jobTimeStamp }}</span>
          </a>

          <!-- Integration -->
          <a :href="internalURL" class="integration" :class="integrationIconClass"></a>

        </div>
      </div>
    </div>
  </div>

  <!-- Latest -->
  <div v-else-if="view === 'latest'" class="latest-job">
      <div class="icon">
        <span class="label label-danger">
          <span class="icon-cross"><i>{{ job.status }}</i></span>
        </span>
      </div>
      <div class="status">
        <h2>
          Job #{{ job.number }} {{ job.status }}
          <small>{{ jobTimeStamp }}</small>
        </h2>
      </div>
      <div class="meta">
        <ul>
          <li>
            Pushed by
            <a :href="`https://github.com/${commitAuthor}`">
              {{ commitAuthor }}
            </a>
          </li>
          <li>
            <a>{{ commitHash }}</a> on <a>{{ commitBranch }}</a>
          </li>
        </ul>
      </div>
    </div>

  <!-- Extended -->
  <div v-else-if="view === 'extended'">
    <div class="panel panel-default">

      <!-- Heading -->
      <div class="panel-heading" role="tab" id="headingOne">
        <span class="label label-danger">
          <span class="icon-cross"><i>Invalid</i></span>
        </span>
        <h3 class="panel-title">
          {{ sourceName }}
          <small>{{ jobTimeStamp }} ({{ commitHash }})</small>
        </h3>
        <a
          role="button"
          data-toggle="collapse"
          data-parent="#accordion"
          :href="`#job-${job.id}`"
          aria-expanded="true"
          aria-controls="collapseOne"
          :class="{collapsed: !active}"
        >
          <span class="icon-keyboard_arrow_down"><i>Toggle details</i></span>
        </a>
        <span class="count label label-danger">{{ errorCount }}</span>
      </div>

      <!-- Files -->
      <div
        :id="`job-${job.id}`"
        class="panel-collapse collapse"
        :class="{in: active}"
        role="tabpanel"
        aria-labelledby="headingOne"
      >
        <div class="panel-body">
          <ul class="dash-files">
            <li v-for="file of invalidFiles">
              <span class="label label-danger">
                {{ file.errorCount }} {{ file.errorCount > 1 ? 'errors' : 'error' }}
              </span>
              <div class="report-thumb">
                <table class="table">
                  <tbody>
                    <tr v-for="(row, rowNumber) of file.rows">
                      <td class="result-row-index">{{ rowNumber }}</td>
                      <td v-for="value of row">{{ value }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              {{ file.name }}
            </li>
          </ul>
          <a :href="`/${job.integration_name}/${sourceName}`" class="btn btn-default">
            See full report
          </a>
        </div>
      </div>

    </div>
  </div>

</template>
