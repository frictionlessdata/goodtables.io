<script>
export default {
  name: 'Settings',
  props: {
    repos: Array,
    buckets: Array,
  },
}
</script>

<template>
<div class="app add-view">
  <div class="inner">

    <section class="add-source">
      <header class="main-header">
        <ul class="nav nav-tabs" role="tablist">
          <li role="presentation" class="active"><a href="#addGithub" aria-controls="addGithub" role="tab" data-toggle="tab">GitHub</a></li>
          <li role="presentation"><a href="#addAmazon" aria-controls="addAmazon" role="tab" data-toggle="tab">Amazon</a></li>
        </ul>
      </header>

      <div class="tab-content">
        <div role="tabpanel" class="github tab-pane active" id="addGithub">
          <div class="tool-bar">
            <span>
              <input type="search" class="form-control search" placeholder="Filter">
            </span>
            <span class="sync">
              <button data-toggle="tooltip" data-placement="left" title="Refresh your organizations and repositories">
                <span class="icon-spinner11"><i>Sync account</i></span>
              </button>
            </span>
          </div>

          <ul class="repos">
            <li v-for="repo of repos" v-if="!repo.active">
              <button class="activate">
                <span class="icon-plus"><i>Activate</i></span>
              </button>
              <h3 class="repo-title">{{ repo.name }}</h3>
              <span class="repo-body">
                <a :href="`https://github.com/${repo.name}`">View repository</a>
              </span>
            </li>
          </ul>

        </div>
        <div role="tabpanel" class="amazon tab-pane" id="addAmazon">
          <div class="tool-bar">
            <span>
              <input type="search" class="form-control search" placeholder="Filter">
            </span>
            <span class="sync">
              <button data-toggle="tooltip" data-placement="left" title="Add bucket">
                <span class="icon-plus"><i>Add bucket</i></span>
              </button>
            </span>
          </div>

          <ul class="repos">
            <li v-for="bucket of buckets" v-if="!bucket.active">
              <button class="activate">
                <span class="icon-plus"><i>Activate</i></span>
              </button>
              <h3 class="bucket-title">{{ bucket.name }}</h3>
              <span class="bucket-body">
                <a :href="`https://console.aws.amazon.com/s3/buckets/${bucket.name}`">View bucket</a>
              </span>
            </li>
          </ul>
        </div>
      </div>

    </section>

  </div>
</div>
</template>

<style scoped>
</style>
