<script>
import moment from 'moment'

export default {
  name: 'JobListItem',
  props: {
    job: Object,
    inSourcePanel: Boolean,
  },
  computed: {
    panelStatusClass() {
      return {
        'panel-success': (this.job && this.job.status === 'success'),
        'panel-danger': (this.job && this.job.status === 'failure'),
        'panel-warning': (this.job && this.job.status === 'error'),
        'panel-info': !this.job,
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
  },
}
</script>

<template>
  <div class="source-item panel" v-bind:class="panelStatusClass">
    <div v-bind:class="job.integration_name">

      <a class="source" :href="internalURL" :class="{active: inSourcePanel}">
        <span class="status">{{ job.status }} </span>
        <span v-if="job.status === 'success'" class="label label-success">
          <span class="icon-checkmark"><i>Valid</i></span>
        </span>
        <span v-else-if="job.status === 'failure'" class="label label-danger">
          <span class="icon-cross"><i>Invalid</i></span>
        </span>
        <span v-else-if="job.status === 'error'" class="label label-warning">
          <span class="icon-warning"><i>Error</i></span>
        </span>
        <h3 class="panel-title">
          {{ jobTitle }}
        </h3>
        <div class="panel-details" v-if="job.integration_name === 'github'">
          <span v-if="!job.conf.is_pr">
            Pushed by <a :href="githubUserURL">{{ job.conf.author_name}}</a> 
            on branch <a :href="githubBranchURL">{{ job.conf.branch_name }}</a> 
            (<a :href="githubCommitURL">{{ job.conf.sha.slice(0,6) }}</a>)
          </span>
          <span v-if="job.conf.is_pr">
            Pull Request <a :href="githubPullRequestURL">#{{ job.conf.pr_number }}</a> 
            opened by <a :href="githubUserURL">{{ job.conf.author_name}}</a> 
          </span>
        </div>
      </a>

      <a class="job" :href="internalURL" :class="{active: inSourcePanel}">
        <span class="jobcount">
          <span class="jobnumber"> #{{ job.number }}</span>
        </span>
        <span class="icon-clock"></span>
        <span class="time" v-bind:title="job.created"> {{ jobTimeStamp }}</span>
      </a>

      <a v-if="!inSourcePanel" :href="externalURL" :class="integrationIconClass" class="integration" style="display:block"></a>
    </div>
  </div>

  </div>

</template>

