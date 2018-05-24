<script>
import Logo from './Logo.vue'
import fdLogo from '../images/logo_fd.svg'
import okiLogo from '../images/logo_oki.svg'

export default {
  name: 'AppBaseLayout',
  props: {
    baseUrl: String,
  },
  components: {
    Logo,
  },
  data() {
    return {
      fdLogo,
      okiLogo,
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
              <Logo :baseUrl="baseUrl" />

              <nav>
                <ul>
                  <li><a href="/user/login/github">Log in</a></li>
                  <li><a href="https://docs.goodtables.io">Help</a></li>
                  <li><a href="/about">About</a></li>
                </ul>
              </nav>
            </div>

            <div class="content">
              <slot name="header"></slot>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="main-content">
      <main class="container">
        <div class="inner">
          <slot></slot>
        </div>
      </main>
    </section>

    <section class="orgs">
      <div class="container">
        <ul class="logos">
          <li>
            <a v-html="okiLogo" href="https://okfn.org" rel="external" ></a>
          </li>
          <li class="fd">
            <a v-html="fdLogo" href="https://frictionlessdata.io" rel="external" ></a>
          </li>
        </ul>
        <p>
          GoodTables is part of the <a href="https://frictionlessdata.io" rel="external">Frictionless Data</a> project from <a href="https://okfn.org" rel="external">Open Knowledge International</a>, which supports a wider discussion around Open Data quality. We believe that GoodTables can reduce the processing time of your data publication workflow, whatever it may be. <a href="https://okfn.org/privacy-policy/">Privacy policy</a>.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
header nav {
  margin-left: auto;
}

header nav ul {
  list-style-type: none;
}

header nav li {
  float: left;
}

header nav li a {
  display: block;
  padding: 14px;
}

header nav li a:hover {
  background-color: #eeeeee44;
}
</style>
