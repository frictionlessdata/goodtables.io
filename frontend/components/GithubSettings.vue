<script>
import axios from 'axios'

export default {
  name: 'GithubSettings',
  props: {
    repos: Array,
  },
  data() {
    return {
      isSyncingAccount: false,
    }
  },
  created() {
    axios.get('/github/api/is_syncing_account')
      .then(res => {
        this.isSyncingAccount = res.data.is_syncing_account
      })
  },
}
</script>

<template>
<div class="container">

  <h1>GitHub</h1>

  <p>GitHub integration description</p>

  <h2>Repos</h2>

  <template v-if="isSyncingAccount">
    <p><button disable class="btn btn-warning">Syncing account</button></p>
    <p>Please refresh the page after some time...</p>
  </template>

  <template v-else>
    <div style="margin-bottom: 30px" class="row">
      <div style="float: right">
        <span> Refresh your organizations and repositories</span>
        <a href="/github/sync" class="btn btn-primary" style="width:120px;">Sync account</a>
      </div>
    </div>
    <template v-if="repos && repos.length">
      <div v-for="repo of repos" class="row" >
        <a v-if="repo.active" :href="`/github/deactivate/${repo.id}`" class="btn btn-success">Deactivate</a>
        <a v-else :href="`/github/activate/${repo.id}`" class="btn btn-danger">Activate</a>
        {{ repo.name }} (<a :href="`https://github.com/${repo.name}`">repo</a>)
        <a v-if="repo.active" :href="`/github/repo/${repo.name}`">View jobs</a>
      </div>
    </template>
    <p v-else class="empty">There are no synced repositories</p>
  </template>

</div>
</template>

<style scoped>
.row {
  border-bottom: solid 1px #eee;
  padding: 5px 0;
}
.empty {
  margin: 10px 0;
}
.btn {
  width: 120px;
}
</style>
