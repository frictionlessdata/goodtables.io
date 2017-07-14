<script>
import qs from 'qs'
import goodtables from 'goodtables'
import goodtablesUI from 'goodtables-ui'


export default {
  name: 'DemoForm',
  props: {
    apiUrl: String,
    apiToken: String,
    apiSourceId: String,
  },
  mounted() {
    const client = new goodtables.ApiClient({
      apiUrl: this.apiUrl,
      apiToken: this.apiToken,
      apiSourceId: this.apiSourceId,
    })
    const validate = (source, options) => {
      const queryData = Object.assign({source}, options)
      return new Promise((resolve, reject) => {
        client.addReport(source, options).then(apiJobId => {
          queryData.apiJobId = apiJobId
          return client.getReport(apiJobId)
        }).then(report => {
          const queryString = `${location.pathname}?${qs.stringify(queryData)}`
          history.pushState(null, null, queryString)
          resolve(report)
        }).catch(error => {
          reject(error)
        })
      })
    }
    const options = qs.parse(location.search.slice(1))
    const source = options.source; delete options.source
    const apiJobId = options.apiJobId; delete options.apiJobId
    if ((options.checks || {})['blank-row']) {
      options.checks['blank-row'] = JSON.parse(options.checks['blank-row'])
    }
    if ((options.checks || {})['duplicate-row']) {
      options.checks['duplicate-row'] = JSON.parse(options.checks['duplicate-row'])
    }
    const element = document.getElementById('form')
    const component = goodtablesUI.Form
    const props = {source, options, validate}
    if (apiJobId) props.reportPromise = client.getReport(apiJobId)
    goodtablesUI.render(component, props, element)
  },
}
</script>

<template>
<div class="app">
  <div class="inner">
    <div class="default">
      <main class="source-view">
        <div class="report">
          <div id="form"></div>
          <div class="description">

<div class="row">
  <div class="col-md-4">
    <h3>What is goodtables?</h3>
    <p> Goodtables is a free online service that helps you find out if your tabular data is actually good to use - it can check for structural problems (blank rows and columns) as well as ensure that data fits a specific schema.</p>
    <p><strong>Tabular data</strong> in CSV and Excel formats is one the most common forms of data available on the web - especially if looking at <a href="http://okfn.org/opendata/" target="_blank">open data</a>. Unfortunately, much of that data is messy with blank and incorrect rows, and unexpected values for some fields. (For example, date columns that do not feature well-formed dates. See here for more examples of <a href="http://okfnlabs.org/bad-data/" target="_blank">bad data</a>.</p>
    <p>That’s where goodtables comes in: it checks your data for you, giving you quick and simple feedback on where your tabular data may not yet be quite perfect.</p>
  </div>
  <div class="col-md-4">
    <h3>How to use goodtables?</h3>
    <p>Goodtables provides different ways to use it:</p>
    <ul>
      <li>use the form above to do one-time validation</li>
      <li>register on the <a href="https://goodtables.io">goodtables.io</a> service for continuous validation</li>
      <li>take a look on <a href="https://github.com/frictionlessdata/goodtables-py" target="_blank">python</a> or <a href="https://github.com/frictionlessdata/goodtables-js" target="_blank">javascript</a> libraries for programming use</li>
    </ul>
    <p>To use a one-time validation form above you just need to provide a link to tabular file or upload it. Then click on the <strong>validate</strong> button. There is a few additional options in the form which is described in-place.</p>
  </div>
  <div class="col-md-4">
    <h3>How provide a feedback?</h3>
    <p>To provide a feedback or report an issue:</p>
    <ul>
      <li>use a feedback <a href="https://discuss.okfn.org/t/launching-goodtables-io-tell-us-what-you-think" target="_blank">thread</a> on the Open Knowledge forum</li>
      <li>file an issue on the GitHub <a href="https://github.com/frictionlessdata/goodtables.io/issues" target="_blank">issue tracker</a></li>
      <li>join the Frictionless Data Gitter <a href="https://gitter.im/frictionlessdata/chat" target="_blank">channel</a></li>
    </ul>
    <p>Reporting an error please attach a validation <strong>permalink</strong> if it's available. After submitting the form above it should be shown on top of a validation report.</p>
  </div>
</div>

          </div>
        </div>
      </main>
    </div>
  </div>
</div>
</template>

<style scoped>
.description {
  border-top: 1px solid #eee;
}
</style>

<style>
.goodtables-ui-form .btn {
  background-color: #01b471 !important;
}

.goodtables-ui-form .row-source {
  padding-bottom: 1em;
  border-bottom: solid 1px #eee;
  margin-bottom: 1em;
}

.goodtables-ui-form .row-schema {
  border-bottom: solid 1px #eee;
}

.goodtables-ui-form .row-message {
  margin-top: 1em;
  border-top: solid 1px #eee;
  padding-top: 1em;
}

.goodtables-ui-form .row-report {
  margin-top: 1em;
  border-top: solid 1px #eee;
  padding-top: 1em;
}

.goodtables-ui-form small {
  color: #777;
}
</style>
