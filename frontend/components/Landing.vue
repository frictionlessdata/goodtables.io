<script>
import AppBaseLayout from './AppBaseLayout.vue'
import screenshot from '../images/screenshot.png'
import screenshotDetails1 from '../images/screenshot-details/1.png'
import screenshotDetails2 from '../images/screenshot-details/2.png'
import screenshotDetails3 from '../images/screenshot-details/3.png'
import screenshotDetails4 from '../images/screenshot-details/4.png'

export default {
  name: 'Landing',
  props: {
    baseUrl: String,
  },
  components: {
    AppBaseLayout,
  },
  data() {
    return {
      screenshot,
      screenshotDetails1,
      screenshotDetails2,
      screenshotDetails3,
      screenshotDetails4,
    }
  },
}
</script>

<template>
  <AppBaseLayout class="main-page" :baseUrl="baseUrl">
    <div slot="header">
      <h1>Publish data with confidence</h1>
      <p>Validate your data on every change, so you catch errors before your users</p>
      <a href="/user/login/github" class="cta btn">
        Validate your data for free
        <p class="sub-text">
          <span class="link-icon icon-github"></span>
          <span class="link-text">Sign in with GitHub</span>
        </p>
      </a>
    </div>

    <figure class="screenshot">
      <img :src="screenshot" alt="Goodtables report screenshot" />
    </figure>

    <h2>Continuous data validation for spreadsheets</h2>

    <div class="features">
      <figure>
        <img :src="screenshotDetails1" alt="" />
        <figcaption>
          Monitor files in multiple formats, including CSV, Excel, LibreOffice, and <a href="http://docs.goodtables.io/" rel="external">more</a>.
        </figcaption>
      </figure>
      <figure>
        <img :src="screenshotDetails2" alt="" />
        <figcaption>
          Check the structure and contents of your tables for potential issues.
        </figcaption>
      </figure>
      <figure>
        <img :src="screenshotDetails3" alt="" />
        <figcaption>
          See errors in context, so they can be easily isolated and resolved.
        </figcaption>
      </figure>
      <figure>
        <img :src="screenshotDetails4" alt="" />
        <figcaption>
          Automatically validate on every change, helping you to keep your data error free.
        </figcaption>
      </figure>
    </div>

    <div class="info">
      <div class="item">
        <div class="inner">
          <h3>How much does it cost?</h3>
          <p>
            It's free! While the basic service of goodtables.io will always remain free, there will be additional features for paid plans in the future.
          </p>
        </div>
      </div>
      <div class="item">
        <div class="inner">
          <h3>How easy is it to set up?</h3>
          <p>
            If your data is hosted on GitHub, you'll be up and running in a few clicks. We also have an <a href="https://docs.goodtables.io/getting_started/s3.html" rel="external">option for technical users</a> to monitor data from Amazon S3.
          </p>
        </div>
      </div>
      <div class="item">
        <div class="inner">
          <h3>What do you do with my data?</h3>
          <p>
            We only use your data while validating it, removing the files after we're finished. Also, <a href="https://github.com/frictionlessdata/goodtables.io" rel="external">all code is open source</a>, so you can check it yourself, or even host it in your own servers.
          </p>
        </div>
      </div>
    </div>

    <a href="/user/login/github" class="cta btn">
      Validate your data for free
      <p class="sub-text">
        <span class="link-icon icon-github"></span>
        <span class="link-text">Sign in with GitHub</span>
      </p>
    </a>
  </AppBaseLayout>
</template>
