<script>
import axios from 'axios'
import Messages from './Messages.vue'

export default {
  name: 'S3Settings',
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
            this.buckets = [...this.buckets, {
              name: payload['bucket-name'],
            }]
          }
        })
    },
    removeBucket(bucket) {
      axios.get(`/s3/api/bucket/${bucket.name}/remove`)
        .then(res => {
          this.error = res.data.error
          if (!this.error) {
            this.buckets = this.buckets.filter(item => item !== bucket)
          }
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
        <button @click="removeBucket(bucket)" class="btn btn-success">Remove</button>
        {{ bucket.name }}
      </div>
    </div>
    <p v-else-if="!ready" class="empty">Loading buckets. Please wait..</p>
    <p v-else>No buckets configured</p>

    <hr>

    <h2>Add Bucket</h2>

    <form>
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
      <button @click.prevent="addBucket()" class="btn btn-default">Submit</button>
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
