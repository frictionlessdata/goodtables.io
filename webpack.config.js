const path = require('path')
const webpack = require('webpack')
const autoprefixer = require('autoprefixer')
const ENV = process.env.NODE_ENV;

// Base

const webpackConfig = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: (ENV === 'production') ? 'goodtables-vue.min.js' : 'goodtables-vue.js',
    library: 'goodtablesVue',
    libraryTarget: 'var',
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            css: 'vue-style-loader!css-loader',
            postcss: 'vue-style-loader!css-loader',
          },
          postcss: [
            autoprefixer({
              browsers: ['last 2 versions']
            })
          ],
        },
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.json$/,
        loader: 'json-loader'
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'url-loader',
        options: {
          limit: 32768,
          name: '[name].[ext]?[hash]'
        }
      },
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.common.js'
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
}

// Production

if (ENV === 'production') {
  webpackConfig.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  webpackConfig.plugins = (webpackConfig.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}

// Module API

module.exports = webpackConfig
