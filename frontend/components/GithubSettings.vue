<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'GithubSettings',
  props: {
    repos: Array,
  },
  components: {
    'app-messages': Messages,
  },
  data() {
    return {
      error: null,
      isSyncingAccount: false,
    }
  },
  methods: {
    updateIsSyncingAccount() {
      axios.get('/github/api/is_syncing_account')
        .then(res => {
          this.isSyncingAccount = res.data.is_syncing_account
        })
    },
    syncAccount() {
      if (this.isSyncingAccount) return
      axios.get('/github/api/sync_account')
        .then(res => {
          if (!res.data.is_syncing_account) {
            this.error = 'Sync account error'
            return
          }
          this.isSyncingAccount = true
          const interval = setInterval(() => {
            this.updateIsSyncingAccount()
            if (!this.isSyncingAccount) {
              clearInterval(interval)
            }
          }, 1000)
        })
    },
  },
  created() {
    this.updateIsSyncingAccount()
  },
}
</script>

<template>
<div>

  <app-messages v-if="error" :messages="[['danger', error]]" />
  <app-messages v-if="isSyncingAccount" :messages="[['warning', 'Syncing account. Please wait..']]" />

  <div class="container">

    <h1>GitHub</h1>

    <p>GitHub integration description</p>

    <h2>Repos</h2>

    <div style="margin-bottom: 30px" class="row">
      <div style="float: right">
        <span> Refresh your organizations and repositories</span>
        <a @click="syncAccount()" class="btn btn-primary">Sync account</a>
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

  </div>

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
