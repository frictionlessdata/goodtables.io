<script>

import Logo from './Logo.vue'
import SourceList from './SourceList.vue'

export default {
  name: 'Dashboard',
  props: {
    latestJobs: Array,
  },
  data: function() {
    return {
        view: 'default-view'
    }
  },
  components: {
    Logo,
    SourceList,
  },
}
</script>

<template>
  <div class="app" :class="view">
    <div class="inner">

      <section class="add-source">
        <header class="main-header">
          <a v-on:click="view = 'default-view'" class="close"><span class="icon-keyboard_arrow_left"><i>Close</i></span></a>
          <ul class="nav nav-tabs" role="tablist">
            <li role="presentation" class="active"><a href="#addGithub" aria-controls="addGithub" role="tab" data-toggle="tab">GitHub</a></li>
            <li role="presentation"><a href="#addS3" aria-controls="addS3" role="tab" data-toggle="tab">Amazon S3</a></li>
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
            <!--
            <ul class="repos">
              <li v-for="repo of repos" v-if="!repo.active">
                <button @click="activateRepo(repo)" class="activate">
                  <span class="icon-plus"><i>Activate</i></span>
                </button>
                <h3 class="repo-title">{{ repo.name }}</h3>
                <span class="repo-body">
                  <a :href="`https://github.com/${repo.name}`">View repository</a>
                </span>
              </li>
            </ul>
            -->

          </div>
          <div role="tabpanel" class="s3 tab-pane" id="addS3">
            amazon
          </div>
        </div>
      </section>

      <section class="settings">
        <header class="main-header">
          Settings
        </header>
      </section>

      <div class="default">
        <nav class="main-nav invalid">
          <header class="main-header">
            <a v-on:click="view = 'default-view'" class="show-view-default"><span>Default view</span></a>
            <a v-on:click="view = 'list-view'" class="show-view-list"><span>List view</span></a>
            <logo/>
            <ul class="nav nav-tabs" role="tablist">
              <li role="presentation" class="active"><a href="#latest-jobs" aria-controls="latest-jobs" role="tab" data-toggle="tab">Latest Jobs</a></li>
            </ul>
          </header>

          <ul class="secondary-nav">
            <li v-if="view != 'add-view'">
              <a v-on:click="view = 'add-view'"><span class="icon-plus label-success"></span> <span class="label label-success">Add source</span></a>
            </li>
            <li v-else>
              <a v-on:click="view = 'default-view'"><span class="icon-keyboard_arrow_left label-success"></span> <span class="label label-success">Close</span></a>
            </li>
            <li v-if="view != 'settings-view'">
              <a v-on:click="view = 'settings-view'"><span class="icon-equalizer label-info"></span> <span class="label label-info">Settings</span></a>
            </li>
            <li v-else>
              <a v-on:click="view = 'default-view'"><span class="icon-keyboard_arrow_left label-info"></span> <span class="label label-info">Close</span></a>
            </li>
          </ul>

          <div class="tab-content">
            <div role="tabpanel" class="tab-pane active" id="latest-jobs">
              <SourceList :jobs="latestJobs" />
            </div>
          </div>

        </nav>
        <main class="source-view">
        </main>
      </div>
    </div>
  </div>
</template>
