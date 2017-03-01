<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'GithubSettings',
  components: {
    Messages,
  },
  data() {
    return {
      ready: false,
      error: null,
      syncing: false,
      repos: [],
    }
  },
  methods: {
    updateRepos() {
      axios.get('/github/api/repo')
        .then(res => {
          this.ready = true
          this.error = res.data.error
          this.syncing = res.data.syncing
          this.repos = res.data.repos
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    syncAccount() {
      if (this.syncing) return
      axios.get('/github/api/sync_account')
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.syncing = true
            const interval = setInterval(() => {
              this.updateRepos()
              if (!this.syncing) {
                clearInterval(interval)
              }
            }, 3000)
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    activateRepo(repo) {
      axios.get(`/github/api/repo/${repo.id}/activate`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            repo.active = true
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    deactivateRepo(repo) {
      axios.get(`/github/api/repo/${repo.id}/deactivate`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            repo.active = false
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
  },
  created() {
    this.updateRepos()
  },
}
</script>

<template>
<div>

  <Messages v-if="error" :messages="[['danger', error]]" />
  <Messages v-if="syncing" :messages="[['warning', 'Syncing account. Please wait..']]" />

  <div class="container">

    <h1>GitHub</h1>

    <p>GitHub integration description</p>

    <h2>Repos</h2>

    <div class="sync">
      <span> Refresh your organizations and repositories</span>
      <button @click="syncAccount()" :disabled="!ready || syncing" class="btn btn-primary">
        Sync account
      </button>
    </div>

    <template v-if="repos && repos.length">
      <div v-for="repo of repos" class="repo">
        <button v-if="repo.active" @click="deactivateRepo(repo)" class="btn btn-success">
          Deactivate
        </button>
        <button v-else @click="activateRepo(repo)" class="btn btn-danger">
          Activate
        </button>
        {{ repo.name }}
        (<a :href="`https://github.com/${repo.name}`">repo</a>)
        <a v-if="repo.active" :href="`/github/repo/${repo.name}`">View jobs</a>
      </div>
    </template>
    <p v-else-if="!ready" class="empty">Loading repos. Please wait..</p>
    <p v-else class="empty">There are no synced repositories</p>

  </div>

</div>
</template>

<style scoped>
.sync {
  margin-bottom: 10px;
  border-bottom: solid 1px #eee;
  padding-bottom: 10px;
  text-align: right;
}

.repo {
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
