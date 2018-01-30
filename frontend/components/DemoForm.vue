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
  <div>
    <div class="primary-secondary">
      <h1>One-time validation</h1>
      <div>
        <section class="main">
          <div id="form"></div>
        </section>
        <section class="aside">
          <div>
            <h3 class="aside-title">How to use this page</h3>
            <p>There are several ways to use goodtables.io. On this page you can try goodtables.io out by manually adding data sources you would like to validate.</p>

            <h4>Other ways to use goodtables.io</h4>
            <p>
              Create a user account to configure goodtables.io for <a href="https://goodtables.io">goodtables.io</a> continuous data validation from GitHub or Amazon S3.
            </p>

            <p>
              Developers can also look at the open source <a href="https://github.com/frictionlessdata/goodtables-py" target="_blank">python library that provides all the data validation logic</a>, or the <a href="https://github.com/frictionlessdata/goodtables-js" target="_blank">goodtables.io javascript client</a> for use in 3rd party applications.
            </p>

          </div>
        </section>
      </div>

    </div>

  </div>
</template>

<style scoped>
</style>
