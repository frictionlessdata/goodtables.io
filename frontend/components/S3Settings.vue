<script>
export default {
  props: {
    buckets: Array,
  },
}
</script>

<template>
<div class="container">

  <h1>Amazon S3</h1>

  <p>Amazon S3 integration description</p>

  <h2>Buckets</h2>
  <ul v-if="buckets.length">
    <li v-for="bucket of buckets">{{ bucket.name }}
      (<a :href="`/s3/settings/remove_bucket/${bucket.name}`">remove</a>)
    </li>
  </ul>
  <p v-else>No buckets configured</p>

  <hr>

  <h2>Add Bucket</h2>

  <form action="/s3/settings/add_bucket" method="POST" >
    <div class="form-group">
      <label for="access-key-id">Access Key Id</label>
      <input type="text" class="form-control" id="access-key-id" name="access-key-id"/>
    </div>
    <div class="form-group">
      <label for="secret-access-key">Secret Access Key</label>
      <input type="text" class="form-control" id="secret-access-key" name="secret-access-key" />
    </div>
    <div class="form-group">
      <label for="secret-access-key">Bucket Name</label>
      <input type="text" class="form-control" id="bucket-name" name="bucket-name" />
    </div>
	<button type="submit" class="btn btn-default">Submit</button>
  </form>

</div>
</template>

<style scoped>
</style>
