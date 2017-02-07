// Require babel polyfill
require('babel-polyfill')

// Require tests for karma
const testsContext = require.context('.', true, /\.js$/)
testsContext.keys().forEach(testsContext)

// Require src for coverage
const srcContext = require.context('../components', true, /\.(js|vue)$/)
srcContext.keys().forEach(srcContext)
