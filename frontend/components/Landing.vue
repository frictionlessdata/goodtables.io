<script>
import Logo from './Logo.vue'
import fdLogo from '../images/logo_fd.svg'
import okiLogo from '../images/logo_oki.svg'
import screenshot from '../images/screenshot.png'
import screenshotDetails1 from '../images/screenshot-details/1.png'
import screenshotDetails2 from '../images/screenshot-details/2.png'
import screenshotDetails3 from '../images/screenshot-details/3.png'
import screenshotDetails4 from '../images/screenshot-details/4.png'

export default {
  name: 'Landing',
  props: {},
  components: {
    Logo,
  },
  data() {
    return {
      screenshot,
      screenshotDetails1,
      screenshotDetails2,
      screenshotDetails3,
      screenshotDetails4,
      okiLogo,
      fdLogo,
    }
  },
}
</script>

<template>
  <div class="landing">
    <header class="main-header">
      <div class="pattern">
        <div class="inner">
          <div class="container">
            <div class="main-nav">
              <Logo />
            </div>

            <div class="content">
              <h1>Have confidence in your data</h1>
              <p>With continuous data validation, you’ll be the first to know if there’s a problem</p>
              <a href="/user/login/github" class="cta btn">
                See how your data is doing
                <p class="sub-text">
                  <span class="link-icon icon-github"></span>
                  <span class="link-text">Sign in with GitHub</span>
                </p>
              </a>
            </div>
          </div>
        </div>
      </div>
    </header>
    <section class="main-content">
      <main class="container">
        <div class="inner">
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
                Checks the data structure and contents of your tables for potential issues.
              </figcaption>
            </figure>
            <figure>
              <img :src="screenshotDetails3" alt="" />
              <figcaption>
                See errors in familiar context, so they can be easily isolated and resolved.
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
                <h3>What does it cost?</h3>
                <p>
                  It's free! While the basic service of goodtables.io will always remain free, there will be additional features for paid plans in the future.
                </p>
              </div>
            </div>
            <div class="item">
              <div class="inner">
                <h3>How easy is it to set up?</h3>
                <p>
                  If your data is hosted on GitHub, you'll be up and running in a few clicks. We also have an <a href="http://docs.goodtables.io/" rel="external">option for technical users</a> to monitor data from Amazon S3.
                </p>
              </div>
            </div>
            <div class="item">
              <div class="inner">
                <h3>Is it private and secure?</h3>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sagittis ut ante id fermentum. Mauris sagittis, tellus quis condimentum finibus.
                </p>
              </div>
            </div>
          </div>

        </div>
      </main>
      <a href="/user/login/github" class="cta btn">
        See how your data is doing
        <p class="sub-text">
          <span class="link-icon icon-github"></span>
          <span class="link-text">Sign in with GitHub</span>
        </p>
      </a>
    </section>
    <section class="orgs">
      <div class="container">
        <ul class="logos">
          <li>
            <a v-html="okiLogo" href="https://okfn.org" rel="external" ></a>
          </li>
          <li class="fd">
            <a v-html="fdLogo" href="https://frictionlessdata.org" rel="external" ></a>
          </li>
        </ul>
        <p>
          GoodTables is part of the Frictionless Data project from Open Knowledge International, which supports a wider discussion around Open Data quality. We believe that GoodTables can reduce the processing time of your data publication workflow, whatever it may be.
        </p>
      </div>
    </section>
  </div>
</template>
