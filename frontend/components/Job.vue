<script>
import moment from 'moment'

export default {
  name: 'Job',
  props: {
    job: Object,
    view: String,
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
    errorCount() {
      // TODO: implement
      return 50
    },
    fileName() {
      // TODO: implement
      return 'test'
    },
    commitHash() {
      return this.job.conf.sha ? this.job.conf.sha.slice(0, 6) : ''
    }
  },
}
</script>

<template>

  <!-- Compact -->
  <div v-if="view === 'compact'">
    <div class="source-item">
      <div class="panel panel-success">
        <div :class="job.integration_time">

          <!-- User/message -->
          <span class="source">
            <a class="avatar">
              <img src="https://avatars1.githubusercontent.com/u/200230?s=48" alt="" />
            </a>
            <h3 class="panel-title">{{ job.conf.commit_message }}</h3>
          </span>

          <!-- Statistics -->
          <a class="job">
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
        >
          <span class="icon-keyboard_arrow_down"><i>Toggle details</i></span>
        </a>
        <span class="count label label-danger">{{ errorCount }}</span>
      </div>

      <!-- Files -->
      <div
        :id="`job-${job.id}`"
        class="panel-collapse collapse in"
        role="tabpanel"
        aria-labelledby="headingOne"
      >
        <div class="panel-body">
          <ul class="dash-files">
            <li>
              <span v-if="errorCount === '1'" class="label label-danger">{{ errorCount }} error</span>
              <span v-else class="label label-danger">{{ errorCount }} errors</span>
              <div class="report-thumb">
                <table class="table">
                  <tbody>
                    <tr class="row-pass">
                      <td class="result-row-index">1</td>
                      <td>file</td>
                      <td>year</td>
                      <td>manufacturer</td>
                      <td>model</td>
                      <td>description</td>
                      <td>euro_standard</td>
                      <td>tax_band</td>
                      <td>transmission</td>
                      <td>transmission_type</td>
                      <td>engine_capacity</td>
                      <td>fuel_type</td>
                      <td>urban_metric</td>
                      <td>extra_urban_metric</td>
                      <td>combined_metric</td>
                      <td>urban_imperial</td>
                      <td>extra_urban_imperial</td>
                      <td>combined_imperial</td>
                      <td>noise_level</td>
                      <td>co2</td>
                      <td>thc_emissions</td>
                      <td>co_emissions</td>
                      <td>nox_emissions</td>
                      <td>thc_nox_emissions</td>
                      <td>particulates_emissions</td>
                      <td>fuel_cost_12000_miles</td>
                      <td>fuel_cost_6000_miles</td>
                      <td>standard_12_months</td>
                      <td>standard_6_months</td>
                      <td>first_year_12_months</td>
                      <td>first_year_6_months</td>
                      <td>date_of_change</td>
                    </tr>
                    <tr class="row-before-fail">
                      <td class="result-row-index">2</td>
                      <td>DatapartC_july2000.csv</td>
                      <td>2000</td>
                      <td>Alfa Romeo</td>
                      <td>145</td>
                      <td>Range</td>
                      <td>1.6</td>
                      <td>Twin Spark</td>
                      <td>16v</td>
                      <td>2</td>
                      <td></td>
                      <td>M5</td>
                      <td>Manual</td>
                      <td>1598</td>
                      <td>Petrol</td>
                      <td>11.1</td>
                      <td>6.5</td>
                      <td>8.2</td>
                      <td>25.4</td>
                      <td>43.5</td>
                      <td>34.4</td>
                      <td>74</td>
                      <td>195</td>
                      <td></td>
                      <td>980</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td>618</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr class="fail">
                      <td class="result-row-index">3</td>
                      <td>DatapartC_july2000.csv</td>
                      <td>2000</td>
                      <td>Alfa Romeo</td>
                      <td>145</td>
                      <td>Range</td>
                      <td>1.6</td>
                      <td>Twin Spark</td>
                      <td>16v</td>
                      <td>2</td>
                      <td></td>
                      <td>M5</td>
                      <td>Manual</td>
                      <td>1598</td>
                      <td>Petrol</td>
                      <td>11.1</td>
                      <td>6.5</td>
                      <td>8.2</td>
                      <td>25.4</td>
                      <td>43.5</td>
                      <td>34.4</td>
                      <td>74</td>
                      <td>195</td>
                      <td></td>
                      <td>980</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td>618</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr class="row-after-fail">
                      <td class="result-row-index">4</td>
                      <td>DatapartC_july2000.csv</td>
                      <td>2000</td>
                      <td>Alfa Romeo</td>
                      <td>145</td>
                      <td>Range</td>
                      <td>1.6</td>
                      <td>Twin Spark</td>
                      <td>16v</td>
                      <td>2</td>
                      <td></td>
                      <td>M5</td>
                      <td>Manual</td>
                      <td>1598</td>
                      <td>Petrol</td>
                      <td>11.1</td>
                      <td>6.5</td>
                      <td>8.2</td>
                      <td>25.4</td>
                      <td>43.5</td>
                      <td>34.4</td>
                      <td>74</td>
                      <td>195</td>
                      <td></td>
                      <td>980</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td>618</td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                    </tr>
                  </tbody>
                </table>
              </div>
              {{ fileName }}
            </li>
          </ul>
          <a v-bind:href="`/${job.integration_name}/${sourceName}`" class="btn btn-default">
            See full report
          </a>
        </div>
      </div>

    </div>
  </div>

</template>
