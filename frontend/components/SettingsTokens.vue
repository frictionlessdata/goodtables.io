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

  <!-- Filter -->
  <div class="filter form-group">
    <label class="sr-only" for="keyword">Filter by keyword</label>
    <div class="input-group">
      <input
        v-model="filter"
        type="text"
        class="form-control input-lg"
        id="keyword"
        placeholder="Filter by keyword"
      >
      <div class="input-group-addon">
        <button><span class="icon-search"><i>Search</i></span></button>
      </div>
    </div>
  </div>

  <!-- Messages -->
  <Messages v-if="error" :messages="[['danger', error]]" />

  <!-- Sources -->
  <div class="parts-selector">

    <!-- Available -->
    <div class="parts list">
      <h3 class="list-heading">Add a token</h3>
      <form @submit.prevent="createToken()" class="add form">
        <div class="form-group">
          <label for="access-key-id">Token description</label>
          <input
            v-model="tokenDescription"
            id="token-description"
            class="form-control"
            type="text"
          >
        </div>
        <button type="submit" class="btn btn-default add">Create Token</button>
      </form>
    </div>

    <!-- Controls -->
    <div class="controls">
      <a class="moveto selected"><span class="icon"></span><span class="text">Add</span></a>
    </div>

    <!-- Active -->
    <div class="selected list">
      <h3 class="list-heading">Active sources</h3>
      <ul v-if="filteredTokens.length">
        <li v-for="token of filteredTokens">
          <span class="source name">{{ token.token }}</span>
          <small v-if="token.description">{{ token.description }}</small>
          <a @click.prevent="deleteToken(token)" class="remove item-button">
            <span class="icon"></span><span class="text">Remove</span>
          </a>
        </li>
      </ul>
      <div v-else class="empty">
        <p>No active tokens found.</p>
      </div>
    </div>

  </div>

</div>
</template>

<style scoped>
</style>
