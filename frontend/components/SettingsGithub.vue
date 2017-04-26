<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'SettingsGithub',
  components: {
    Messages,
  },
  data() {
    return {
      ready: false,
      error: null,
      syncing: false,
      repos: [],
      filter: '',
    }
  },
  computed: {
    filteredRepos() {
      if (!this.filter) return this.repos
      return this.repos.filter(repo => repo.name.includes(this.filter))
    },
  },
  methods: {
    updateRepos() {
      axios.get('/github/api/repo')
        .then(res => {
          this.ready = true
          this.error = res.data.error
          this.syncing = res.data.syncing
          this.repos = res.data.repos || []
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

  <div class="tool-bar">
    <span>
      <input v-model="filter" type="search" class="form-control search" placeholder="Filter">
    </span>
    <span class="sync">
      <button @click="syncAccount()" class="refresh" :disabled="!ready || syncing"  data-toggle="tooltip" data-placement="left" title="Refresh your organizations and repositories">
        <span class="icon-spinner11"><i>Sync account</i></span>
      </button>
    </span>
  </div>

  <Messages v-if="error" :messages="[['danger', error]]" />
  <Messages v-if="syncing" :messages="[['warning', 'Syncing account. Please wait..']]" />

  <ul v-if="repos.length" class="repos">
    <li v-for="repo of filteredRepos" class="repo" :class="{active: repo.active}">
      <button v-if="repo.active" @click="deactivateRepo(repo)" class="activate">
        <span class="icon-cross"><i>Deactivate</i></span>
      </button>
      <button v-else @click="activateRepo(repo)" class="activate">
        <span class="icon-plus"><i>Activate</i></span>
      </button>
      <h3 class="repo-title">
        <a :href="`/github/${repo.name}`">{{ repo.name }}</a>
      </h3>
      <span class="repo-body">
        <a :href="`https://github.com/${repo.name}`">View repository</a>
      </span>
    </li>
  </ul>
  <p v-else-if="!ready" class="empty">Loading repos. Please wait..</p>
  <p v-else class="empty">There are no synced repositories</p>

</div>
</template>

<style scoped>
.sync {
  margin-bottom: 10px;
  border-bottom: solid 1px #eee;
  padding-bottom: 10px;
  text-align: right;
}
.empty {
  margin: 10px 0;
}
.btn {
  width: 120px;
}
</style>
