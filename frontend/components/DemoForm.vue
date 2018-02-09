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
      <h1>Validate tabular file</h1>
      <div>
        <section class="main">
          <div id="form"></div>
        </section>
      </div>

    </div>

  </div>
</template>

<style scoped>
  .main {
    width: 100%;
  }
</style>
