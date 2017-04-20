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

  <div class="tool-bar">
    <span>
      <input v-model="filter" type="search" class="form-control search" placeholder="Filter">
    </span>
    <span class="sync">
      <button @click="showAddBucket = !showAddBucket" class="show-add" data-toggle="tooltip" data-placement="left" title="Add bucket">
        <span class="icon-plus"><i>Add bucket</i></span>
      </button>
    </span>
  </div>

  <Messages v-if="error" :messages="[['danger', error]]" />

  <div v-if="showAddBucket">
    <hr>
    <form @submit.prevent="addBucket()">
      <div class="form-group">
        <label for="access-key-id">Access Key Id</label>
        <input v-model="accessKeyId" type="text" class="form-control" id="access-key-id" />
      </div>
      <div class="form-group">
        <label for="secret-access-key">Secret Access Key</label>
        <input v-model="secretAccessKey" type="text" class="form-control" id="secret-access-key" />
      </div>
      <div class="form-group">
        <label for="bucket-name">Bucket Name</label>
        <input v-model="bucketName" type="text" class="form-control" id="bucket-name" />
      </div>
      <button type="submit" class="btn btn-default add">Submit</button>
    </form>
    <hr>
  </div>

  <ul v-if="buckets.length" class="repos">
    <li v-for="bucket of filteredBuckets" class="repo" :class="{active: bucket.active}">
      <button v-if="bucket.active" @click="deactivateBucket(bucket)" class="activate">
        <span class="icon-cross"><i>Deactivate</i></span>
      </button>
      <button v-else @click="activateBucket(bucket)" class="activate">
        <span class="icon-plus"><i>Activate</i></span>
      </button>
      <h3 class="repo-title">
        <a :href="`/source/s3/${bucket.name}`">{{ bucket.name }}</a>
      </h3>
      <span class="repo-body">
        <a :href="`https://console.aws.amazon.com/s3/buckets/${bucket.name}`">View bucket</a>
        /
        <a href="#" @click.prevent="removeBucket(bucket)">Remove bucket</a>
      </span>
    </li>
  </ul>
  <p v-else-if="!ready" class="empty">Loading buckets. Please wait..</p>
  <p v-else>No buckets configured</p>

</div>
</template>

<style scoped>
.bucket {
  padding: 5px 0;
}
.bucket:not(:last-child) {
  border-bottom: solid 1px #eee;
}
</style>
