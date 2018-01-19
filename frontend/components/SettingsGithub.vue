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

  <!-- Filter -->
  <div class="filter form-group">
    <label class="sr-only" for="keyword">Filter by keyword</label>
    <div class="input-group">
      <input
        v-model="filter"
        type="text"
        class="form-control input-lg"
        id="keyword" placeholder="Filter by keyword"
      >
      <div class="input-group-addon">
        <button><span class="icon-search"><i>Search</i></span></button>
      </div>
    </div>
  </div>

  <!-- Messages -->
  <Messages v-if="error" :messages="[['danger', error]]" />
  <Messages v-if="syncing" :messages="[['warning', 'Syncing account. Please wait..']]" />

  <!-- Sources -->
  <div class="parts-selector" id="github-sources">

    <!-- Available -->
    <div class="parts list">
      <h3 class="list-heading">
        <a @click="syncAccount()" :disabled="!ready || syncing" class="refresh">
          <span class="icon-refresh"><i>Refresh</i></span>
        </a>
        Available sources
      </h3>
      <ul v-if="filteredRepos.filter(repo => !repo.active).length">
        <li v-for="repo of filteredRepos" v-if="!repo.active">
          <span class="source name">{{ repo.name }}</span>
          <a :href="`https://github.com/${repo.name}`" class="repo link">View repository</a>
          <a @click="activateRepo(repo)" class="add item-button">
            <span class="icon"></span>
            <span class="text">Add</span>
          </a>
        </li>
      </ul>
      <div v-else class="empty action">
        <p>No sources found.</p>
        <p>Use the <span class="icon-refresh"><i>Refresh</i></span> button to refresh your list of repositories and organisations.</p>
      </div>
    </div>

    <!-- Controls -->
    <div class="controls">
      <a class="moveto selected"><span class="icon"></span><span class="text">Add</span></a>
      <a class="moveto parts"><span class="icon"></span><span class="text">Remove</span></a>
    </div>

    <!-- Active -->
    <div class="selected list">
      <h3 class="list-heading">Active sources</h3>
      <ul v-if="filteredRepos.filter(repo => repo.active).length">
        <li v-for="repo of filteredRepos" v-if="repo.active">
          <span class="source name">{{ repo.name }}</span>
          <a :href="`https://github.com/${repo.name}`" class="repo link">View repository</a>
          <a @click="deactivateRepo(repo)" class="remove item-button">
            <span class="icon"></span>
            <span class="text">Remove</span>
          </a>
        </li>
      </ul>
      <div v-else class="empty">
        <p>No active sources found.</p>
      </div>
    </div>

  </div>

</div>
</template>

<style scoped>
</style>
