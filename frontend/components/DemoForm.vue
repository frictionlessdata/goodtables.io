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
    <h3>What is goodtables.io?</h3>
    <p>
      goodtables.io is a free online service for continuous data validation. goodtables.io checks tabular data sources for structural problems, such as blank rows and non-tabular input, and optionally checks the data against a given schema, providing robust quality assurance for your data. goodtables.io supports many formats used for tabular data storage, including CSV, Excel, JSON, and ODS. Read more about the bad data problems goodtables.io can address <a href="http://okfnlabs.org/bad-data/" target="_blank">here</a>.
    </p>
  </div>
  <div class="col-md-4">
    <h3>How does it work?</h3>
    <p>There are several ways to use goodtables.io</p>
    <ul>
      <li>Use the form on this page to try goodtables.io out by manually adding data sources you would like to validate. See <a href="http://try.goodtables.io/?source=https%3A%2F%2Fraw.githubusercontent.com%2Ffrictionlessdata%2Fgoodtables-py%2Fmaster%2Fdata%2Finvalid-on-structure.csv&apiJobId=9a84648d-2088-47c2-80a7-923fb9564a7a">invalid structure</a> and <a href="http://try.goodtables.io/?source=https%3A%2F%2Fraw.githubusercontent.com%2Ffrictionlessdata%2Fgoodtables-py%2Fmaster%2Fdata%2Finvalid-on-bis-modified-schema.csv&schema=https%3A%2F%2Fraw.githubusercontent.com%2Ffrictionlessdata%2Fgoodtables-py%2Fmaster%2Fdata%2Fbis-modified-schema.json&apiJobId=0e49fa2e-d74a-4771-a528-f0fc5c6d1a7b">invalid schema</a> examples.</li>
      <li>Create a user account to configure goodtables.io for <a href="https://goodtables.io">goodtables.io</a>continuous data validation</li> from GitHub or Amazon S3.
      <li>Developers can also look at the open source <a href="https://github.com/frictionlessdata/goodtables-py" target="_blank">python library that provides all the data validation logic</a>, or the <a href="https://github.com/frictionlessdata/goodtables-js" target="_blank">goodtables.io javascript client</a> for use in 3rd party applications.</li>
    </ul>
  </div>
  <div class="col-md-4">
    <h3>How provide a feedback?</h3>
    <p>To provide a feedback or report an issue:</p>
    <ul>
      <li>Give feedback <a href="https://discuss.okfn.org/t/launching-goodtables-io-tell-us-what-you-think" target="_blank">thread</a>on the Open Knowledge International forum.</li>
      <li>Open a bug report or a feature request on the <a href="https://github.com/frictionlessdata/goodtables.io/issues" target="_blank">goodtables.io issue tracker</a>.</li>
      <li>Join our <a href="https://gitter.im/frictionlessdata/chat" target="_blank">chat room on Gitter, and talk to the team</a>.</li>
    </ul>
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
