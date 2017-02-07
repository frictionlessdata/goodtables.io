const webpackConfig = require('./webpack.config.js')
delete webpackConfig.entry

// Base

const karmaConfig = (config) => {
  config.set({
    singleRun: true,
    browsers: ['PhantomJS'],
    frameworks: ['mocha', 'sinon-chai'],
    files: ['test/index.js'],
    reporters: ['spec', 'coverage'],
    preprocessors: {
      'test/index.js': ['webpack'],
    },
    webpack: webpackConfig,
    webpackMiddleware: {
      noInfo: true
    },
    client: {
      mocha: {
        opts: '.mocharc',
      },
    },
    coverageReporter: {
      dir: './coverage',
      includeAllSources: true,
      check: {
        global: {
          lines: 70,
        },
      },
      reporters: [
        { type: 'lcov', subdir: '.' },
        { type: 'text' },
      ]
    },
  })
}

// Module API

module.exports = karmaConfig
