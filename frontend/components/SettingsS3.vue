<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'SettingsS3',
  components: {
    Messages,
  },
  data() {
    return {
      ready: false,
      error: null,
      buckets: [],
      accessKeyId: null,
      secretAccessKey: null,
      bucketName: null,
      showAddBucket: false,
      filter: '',
    }
  },
  computed: {
    filteredBuckets() {
      if (!this.filter) return this.buckets
      return this.buckets.filter(bucket => bucket.name.includes(this.filter))
    },
    addBucketIcon() {
      return (!this.showAddBucket) ? 'icon-plus' : 'icon-cross'
    },
  },
  methods: {
    updateBuckets() {
      axios.get('/s3/api/bucket')
        .then(res => {
          this.ready = true
          this.error = res.data.error
          this.buckets = res.data.buckets || []
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    addBucket() {
      const payload = {
        'access-key-id': this.accessKeyId,
        'secret-access-key': this.secretAccessKey,
        'bucket-name': this.bucketName,
      }
      axios.post('/s3/api/bucket', payload)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.buckets = [...this.buckets, res.data.bucket]
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    activateBucket(bucket) {
      axios.get(`/s3/api/bucket/${bucket.id}/activate`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            bucket.active = true
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    deactivateBucket(bucket) {
      axios.get(`/s3/api/bucket/${bucket.id}/deactivate`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            bucket.active = false
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
    removeBucket(bucket) {
      axios.delete(`/s3/api/bucket/${bucket.id}`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.buckets = this.buckets.filter(item => item !== bucket)
          }
        })
        .catch(() => {
          this.error = 'Unknown Error'
        })
    },
  },
  created() {
    this.updateBuckets()
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
      <h3 class="list-heading">Add a bucket</h3>
      <form @submit.prevent="addBucket()" class="add form">
        <div class="form-group">
          <label for="access-key-id">Access Key Id</label>
          <input
            v-model="accessKeyId"
            id="access-key-id"
            class="form-control"
            type="text"
          >
        </div>
        <div class="form-group">
          <label for="secret-access-key">Secret Access Key</label>
          <input
            v-model="secretAccessKey"
            id="secret-access-key"
            class="form-control"
            type="text"
          >
        </div>
        <div class="form-group">
          <label for="bucket-name">Bucket Name</label>
          <input
            v-model="bucketName"
            id="bucket-name"
            class="form-control"
            type="text"
          >
        </div>
        <button type="submit" class="btn btn-default add">Add</button>
      </form>
    </div>

    <!-- Controls -->
    <div class="controls">
      <a class="moveto selected"><span class="icon"></span><span class="text">Add</span></a>
    </div>

    <!-- Active -->
    <div class="selected list">
      <h3 class="list-heading">Active buckets</h3>
      <ul v-if="filteredBuckets.length">
        <li v-for="bucket of filteredBuckets" title="Remove bucket">
          <a @click.prevent="removeBucket(bucket)" class="remove item-button">
            <span class="source name">{{ bucket.name }}</span>
            <span class="icon"></span><span class="text">Remove</span>
          </a>
        </li>
      </ul>
      <div v-else class="empty">
        <p>There are no active buckets.</p>
      </div>
    </div>

  </div>

</div>
</template>

<style scoped>
</style>
