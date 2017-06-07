<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'SettingsTokens',
  components: {
    Messages,
  },
  data() {
    return {
      error: null,
      ready: false,
      tokens: [],
      tokenDescription: null,
      showCreateToken: false,
      filter: '',
    }
  },
  computed: {
    filteredTokens() {
      if (!this.filter) return this.tokens
      return this.tokens.filter(token =>
        (token.description || '').toLowerCase().includes(this.filter.toLowerCase()))
    },
    createTokenIcon() {
      return (!this.showCreateToken) ? 'icon-plus' : 'icon-cross'
    },
  },
  methods: {
    loadTokens() {
      axios.get('/api/token')
        .then(res => {
          this.ready = true
          this.error = res.data.error
          this.tokens = res.data.tokens || []
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    createToken() {
      const payload = {description: this.tokenDescription}
      axios.post('/api/token', payload)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.tokens = [...this.tokens, res.data.token]
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    deleteToken(token) {
      axios.delete(`/api/token/${token.id}`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.tokens = this.tokens.filter(item => item !== token)
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
  },
  created() {
    this.loadTokens()
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
      <button @click="showCreateToken = !showCreateToken" class="show-add" data-toggle="tooltip" data-placement="left" title="Create token">
        <span :class="createTokenIcon"><i>Create token</i></span>
      </button>
    </span>
  </div>

  <Messages v-if="error" :messages="[['danger', error]]" />

  <div v-if="showCreateToken" style="padding: 25px 15px; width: 100%; border-bottom: solid 5px #333">
    <form @submit.prevent="createToken()">
      <div class="form-group">
        <label for="token-description">Token Description</label>
        <input v-model="tokenDescription" type="text" class="form-control" id="token-description" />
      </div>
      <button type="submit" class="btn btn-default add">Create Token</button>
    </form>
  </div>

  <ul v-if="tokens.length" class="repos">
    <li v-for="token of filteredTokens" class="repo active">
      <button @click="deleteToken(token)" class="activate">
        <span class="icon-cross"><i>Delete Token</i></span>
      </button>
      <h3 class="repo-title">
        <code>{{ token.token }}</code>
      </h3>
      <span class="repo-body">
        {{ token.description || 'no description'}}
      </span>
    </li>
  </ul>
  <p v-else-if="!ready" class="empty">Loading tokens. Please wait..</p>
  <p v-else>No tokens created</p>

</div>
</template>

<style scoped>
</style>
