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
    }
  },
  methods: {
    updateBuckets() {
      axios.get('/s3/api/bucket')
        .then(res => {
          this.ready = true
          this.error = res.data.error
          this.buckets = res.data.buckets
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

  <Messages v-if="error" :messages="[['danger', error]]" />

  <div class="container">

    <h1>Amazon S3</h1>

    <p>Amazon S3 integration description</p>

    <h2>Buckets</h2>
    <div v-if="buckets && buckets.length">
      <div v-for="bucket of buckets" class="bucket">
        <button v-if="bucket.active" @click="deactivateBucket(bucket)" class="btn btn-success">
          Deactivate
        </button>
        <button v-else @click="activateBucket(bucket)" class="btn btn-danger">
          Activate
        </button>
        {{ bucket.name }}
        (<a @click.prevent="removeBucket(bucket)" href="">remove</a>)
      </div>
    </div>
    <p v-else-if="!ready" class="empty">Loading buckets. Please wait..</p>
    <p v-else>No buckets configured</p>

    <hr>

    <h2>Add Bucket</h2>

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
      <button type="submit" class="btn btn-default">Submit</button>
    </form>

  </div>

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
