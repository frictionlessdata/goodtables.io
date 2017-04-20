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
      if (this.job.integration_name === 'github') {
        return `/source/github/${this.sourceName}/jobs/${this.job.number}`
      } else if (this.job.integration_name === 's3') {
        return `/source/s3/${this.sourceName}/jobs/${this.job.number}`
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
        return this.job.conf.sha.slice(0, 7)
      } else if (this.job.integration_name === 's3') {
        return this.job.conf.bucket
      }
    },
    jobTimeStamp() {
      return moment(this.job.created).fromNow()
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

