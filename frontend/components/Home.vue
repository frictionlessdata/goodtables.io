<script>
import Logo from './Logo.vue'

const Vue = require('vue')
const VueScrollTo = require('vue-scrollto')

Vue.use(VueScrollTo)

export default {
  name: 'Home',
  props: {},
  components: {
    Logo,
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
              <div class="container">
                <logo/>
                <nav>
                  <a href="/user/login/github"><span class="link-icon icon-login"></span> <span class="link-text">Sign in with GitHub</span></a>
                </nav>
              </div>
            </div>
            <div class="content">
              <div class="source-item panel panel-success">
                <div>
                  <span class="source">
                    <span class="label label-success">
                      <span class="icon-checkmark">
                        <i>Valid</i>
                      </span>
                    </span>
                    <p class="panel-title">
                      repository/my-data
                    </p>
                  </span>
                  <span class="job">
                    <span class="icon-clock"></span>
                    <span class="time"> a minute ago</span>
                  </span>
                </div>
              </div>

              <a class="next" href="#features" v-scroll-to="'#features'">
                <h1>Continuous data validation for everybody</h1>
                <span class="icon-keyboard_arrow_down">
                  <i>Learn more</i>
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </header>
    <section class="features" id="features">
      <div class="container">
        <div class="content">
          <div class="inner">
            <ul class="feature-list">
              <li class="check">
                <span class="wrapper">
                  <span class="icon-goodtables"></span>
                </span>
                <p>Automatically check data is good on every update</p>
              </li>
              <li class="validate">
                <span class="wrapper">
                  <span class="icon-mouse-pointer"></span>
                </span>
                <p>Validate data with a minimum of clicks</p>
              </li>
              <li class="trust">
                <span class="wrapper">
                  <span class="icon-shield"></span>
                </span>
                <p>Trust in the validity and usefulness of your data</p>
              </li>
              <li class="connect">
                <span class="icon-github"></span>
                <p>Connect directly to your data repository</p>
              </li>
              <li class="quality">
                <span class="wrapper">
                  <span class="icon-checkmark"></span>
                  <span class="icon-checkmark"></span>
                </span>
                <p>Prove that your data is of consistent good quality</p>
              </li>
              <li class="errors">
                <span class="icon-clock"></span>
                <p>Catch and identify errors early</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <a class="next" href="#about" v-scroll-to="'#about'">
        <span class="icon-keyboard_arrow_down">
          <i>More</i>
        </span>
      </a>
    </section>
    <section class="text" id="about">
      <div class="container">
        <div class="content">
		  <div class="inner">
			<h2>Ensure, in a detailed and automated fashion, that data sources meet the quality requirements for further analysis and integration</h2>
			<p>
			  GoodTables is part of the <a href="https://frictionlessdata.io/">Frictionless Data</a> project from Open Knowledge International, which supports a wider discussion around Open Data quality. We believe that GoodTables can reduce the processing time of your data publication workflow, whatever it may be. For us it answers one the most consistent questions we have encountered in our work with data over the last 10 years: How can one ensure, in a detailed and automated fashion, that data sources meet the quality requirements for further analysis and integration?
			</p>
		  </div>
        </div>
        <div class="cta">
          <div class="inner">
            <a class="btn btn-primary" href="/user/login/github">Sign in with GitHub</a>
            <h2>Try it yourself. It's Free!*</h2>
            <small>* While the basic service of goodtables.io will always remain free, there will be additional features for paid plans in the future. Watch this space!</small>
          </div>
        </div>
      </div>
    </section>
    <section class="footer">
      <div class="container">
        <div class="footer-primary">
          <a class="footer-logo" href="https://okfn.org/">
            <img src="https://a.okfn.org/img/oki/landscape-white-468x122.png" alt="Open Knowledge International">
          </a>
          <ul class="footer-links">
            <li><a href="https://twitter.com/OKFNLabs">@OKFNLabs</a></li>
          </ul>
        </div>
        <div class="footer-secondary">
          <p>
            &copy; <a href="https://okfn.org">Open Knowledge International</a> 2017
          </p>
        </div>
      </div>
    </section>
  </div>
</template>
