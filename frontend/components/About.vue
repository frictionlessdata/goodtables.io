<script>
import AppBaseLayout from './AppBaseLayout.vue'

export default {
  name: 'About',
  props: {
    baseUrl: String,
  },
  components: {
    AppBaseLayout,
  },
}
</script>

<template>
  <AppBaseLayout>
    <p>
      Goodtables.io is a continuous validation service for tabular data by
      the <a href="https://okfn.org" rel="external">Open Knowledge
      Foundation</a>. It allows for the checking of common errors and problems
      in tabular data files, such as:
    </p>
    <ul>
      <li>Can a CSV be loaded?</li>
      <li>Are there any blank rows?</li>
      <li>Are all values in the column "e-mail" actually e-mails?</li>
      <li>Do all rows have the same number of columns?</li>
    </ul>
    <p>
      This frees up data publishers' time to focus on checking if the data
      is correct in the first place, increasing the quality and their
      confidence in the dataset.
    </p>

    <h2>Why?</h2>
    <p>
      We want to increase the usage of data. We believe that it can help
      people be more productive and achieve their goals.
    </p>
    <p>
      Although there is a lot of data published by governments and other
      institutions, its quality tends to be low on average. This is caused
      in part by the lack of resources and training, but also by the lack
      of good tools. This is where goodtables fits.
    </p>
    <p>
      By using goodtables, data publishers can do more with less,
      increasing the quality of their data, which in turn will increase its
      usage by making it easier to work with it.
    </p>

    <h2>Who?</h2>
    <p>
      This service is provided by the <a href="https://okfn.org"
      rel="external">Open Knowledge Foundation</a>, a global non-profit
      organisation that focuses on helping civil society groups access and
      use data to achieve their goals. Since we started in 2004, we have been
      pushing governments and organisations to release data, building tools and
      materials to help them do so, and to help others make use of this data.
      Some of our projects include:
    </p>
    <ul>
      <li>
        <a href="https://ckan.org">CKAN</a>, the most used open source data
        publishing platform;
      </li>
      <li>
        The <a href="https://opendefinition.org/" rel="external">Open
        Definition</a> that defines "openness" in relation to data and content;
      </li>
      <li>
        Data literacy materials as
        the <a href="https://opendatahandbook.org" rel="external">Open
        Data Handbook</a> and <a href="https://schoolofdata.org"
        rel="external">School of Data</a>;
      </li>
      <li>
        <a href="https://openspending.org"
        rel="external">OpenSpending</a>, a fiscal data publishing
        platform, and;
      </li>
      <li>
        <a href="https://frictionlessdata.io" rel="external">Frictionless Data</a>, a
        set of specifications and tools to work with data (of which
        Goodtables is part of).
      </li>
    </ul>
    <p>
      You can read more about us and our work on <a href="https://okfn.org">our
      website</a>.
    </p>
  </AppBaseLayout>
</template>

<style scoped>
  .main-header .inner {
    padding-bottom: 0;
  }

  .main-content {
    text-align: left;
  }
</style>
