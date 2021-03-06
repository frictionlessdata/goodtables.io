<script>
import moment from 'moment'
import {removeBaseUrl} from '../helpers'

export default {
  name: 'Job',
  props: {
    job: Object,
    view: String,
    active: Boolean,
    githubId: Number,
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
        'icon-cross': (this.job && (this.job.status === 'failure' || this.job.status === 'error')),
      }
    },
    integrationIconClass() {
      return {
        'icon-github': this.job.integration_name === 'github',
        'icon-amazon': this.job.integration_name === 's3',

      }
    },
    sourceName() {
      return this.job.source.name
    },
    internalURL() {
      return `/${this.job.integration_name}/${this.sourceName}/jobs/${this.job.number}`
    },
    externalURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.sourceName}/tree/${this.job.conf.sha}`
      } else if (this.job.integration_name === 's3') {
        return `https://console.aws.amazon.com/s3/buckets/${this.sourceName}`
      }
    },
    jobTimeStamp() {
      return moment(this.job.created).fromNow()
    },
    jobMessage() {
      let message = ''
      if (this.job.integration_name === 'github') {
        message = this.job.conf.is_pr
          ? this.job.conf.pr_title
          : this.job.conf.commit_message
      } else if (this.job.integration_name === 's3') {
        message = this.job.conf.bucket
      }
      message = message.split('\n')[0]
      return message
    },
    jobHash() {
      if (this.job.integration_name === 'github') {
        return this.job.conf.sha ? this.job.conf.sha.slice(0, 6) : ''
      }
    },
    jobAuthor() {
      if (this.job.integration_name === 'github') {
        return this.job.conf.author_name
      }
    },
    jobBranch() {
      if (this.job.integration_name === 'github') {
        return this.job.conf.branch_name
      }
    },
    githubUserURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.job.conf.author_name}`
      }
    },
    githubBranchURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.sourceName}/tree/${this.job.conf.branch_name}`
      }
    },
    githubCommitURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.sourceName}/commit/${this.job.conf.sha}`
      }
    },
    githubPullRequestURL() {
      if (this.job.integration_name === 'github') {
        return `https://github.com/${this.sourceName}/pull/${this.job.conf.pr_number}`
      }
    },
    invalidFiles() {
      const files = []
      if (this.job.report) {
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
      }
      return files
    },
  },
}
</script>

<template>

  <!-- Compact -->
  <div v-if="view === 'compact'" class="source-item" :class="{active}">
    <div class="panel" :class="statusPanelClass">
      <div :class="job.integration_name">

        <!-- User/message -->
        <span class="source">
          <a class="avatar" :href="internalURL">
            <img v-if="jobAuthor" :src="`https://github.com/${jobAuthor}.png?s=48`" />
            <img v-else-if="githubId" :src="`https://avatars1.githubusercontent.com/u/${githubId}?s=52&v=4`" />
          </a>
          <h3 class="panel-title">{{ jobMessage }}</h3>
        </span>

        <!-- Statistics -->
        <a class="job" :href="internalURL">
          <span class="jobcount">
            <span class="jobnumber">#{{ job.number }}</span>
            <span v-if="jobHash" class="jobid">
              <a :href="githubCommitURL"> ({{ jobHash }})</a>
            </span>
          </span>
          <span class="label" :class="statusLabelClass">
            <span :class="statusIconClass"><i>{{ job.status }}</i></span>
          </span>
          <span class="time">{{ jobTimeStamp }}</span>
        </a>

      </div>
    </div>
  </div>

  <!-- Standard -->
  <div v-else-if="view === 'standard'" class="source-item">
    <div class="panel" :class="statusPanelClass">
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
            <span v-if="jobHash" class="jobid">
              <a :href="githubCommitURL"> ({{ jobHash }})</a>
            </span>
          </span>
          <span class="icon-clock"></span>
          <span class="time">{{ jobTimeStamp }}</span>
        </a>

        <!-- Integration -->
        <a :href="internalURL" class="integration" :class="integrationIconClass"></a>

      </div>
    </div>
  </div>

  <!-- Report -->
  <div v-else-if="view === 'report'" class="latest-job">
    <div class="icon">
      <span class="label" :class="statusLabelClass">
        <span :class="statusIconClass"><i>{{ job.status }}</i></span>
      </span>
    </div>
    <div class="status">
      <h2>
        Job #{{ job.number }} {{ job.status }}
        <small>{{ jobTimeStamp }}</small>
      </h2>
    </div>
    <div v-if="job.integration_name === 'github'" class="meta">
      <ul v-if="job.conf.is_pr">
        <li>Pull request <a :href="githubPullRequestURL">#{{ job.conf.pr_number }}</a></li>
        <li>
          opened by
          <a :href="githubUserURL">{{ jobAuthor }}</a>
        </li>
      </ul>
      <ul v-else>
        <li>Pushed by <a :href="githubUserURL">{{ jobAuthor }}</a></li>
        <li>
          <a :href="githubCommitURL">{{ jobHash }}</a> on
          <a :href="githubBranchURL">{{ jobBranch }}</a>
        </li>
      </ul>
    </div>
  </div>

  <!-- Extended -->
  <div v-else-if="view === 'extended'" class="panel panel-default">

    <!-- Heading -->
    <div class="panel-heading" role="tab" id="headingOne">
      <span class="label" :class="statusLabelClass">
        <span class="icon-cross"><i>{{ job.status }}</i></span>
      </span>
      <h3 class="panel-title">
        <a :href="internalURL">
          {{ sourceName }}
        </a>
        <small>
          {{ jobTimeStamp }} -
          <span class="jobnumber"> #{{ job.number }}</span>
          <span v-if="jobHash">
            <a :href="githubCommitURL">({{ jobHash }})</a>
          </span>
          <span v-if="job.status === 'error'">- ERROR</span>
        </small>
      </h3>
    </div>

    <!-- Files -->
    <div
      :id="`job-${job.id}`"
    >
      <div class="panel-body">
        <a :href="internalURL">
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
        </a>
      </div>
    </div>

  </div>

</template>
