<script>

import moment from 'moment'

export default {
  name: 'SourceListItem',
  props: {
    source: Object,
    job: Object,
    active: Boolean,
    inSourcePanel: Boolean,
  },
  data() {
    return {
      isActive: this.active,
    }
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
        'icon-github': this.source.integration_name === 'github',
        'icon-amazon': this.source.integration_name === 's3',

      }
    },
    sourceURL() {
      let url
      if (this.source.integration_name === 'github') {
        url = `/source/github/${this.source.name}`
      } else if (this.source.integration_name === 's3') {
        url = `/source/s3/${this.source.name}`
      }
      if (this.job && this.source.last_job.number !== this.job.number) {
        url = `${url}/jobs/${this.job.number}`
      }
      return url
    },
    jobTimeStamp() {
      return moment(this.job.created).fromNow()
    },
  },
}

</script>


<template>
  <div class="source-item panel" v-bind:class="panelStatusClass">
    <div v-bind:class="source.integration_name">
      <a class="source" v-bind:class="{active: inSourcePanel}" v-bind:href="sourceURL">

        <template v-if="job">
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

        </template>

        <template v-if="!job">
        <span class="label label-info">
          <span class="icon-info"><i>No jobs yet</i></span>
        </span>
        </template>

          <h3 class="panel-title">
            {{ source.name }}

            <span v-if="job" class="jobnumber">#{{ job.number }}</span>
          </h3>
        </a>

        <a class="job"  v-bind:class="{active: inSourcePanel}">

          <template v-if="job">
          <span class="jobcount">
            <span class="jobnumber"> #{{ job.number }}</span>
          </span>
          <span class="icon-clock"></span><span class="time" v-bind:title="job.created"> {{ jobTimeStamp }}</span>
          </template>

          <template v-if="!job">
          <span class="time">No jobs yet</span>
          </template>

        </a>

        <a class="integration" v-bind:class="integrationIconClass"></a>
      </div>
  </div>

  </div>

</template>

