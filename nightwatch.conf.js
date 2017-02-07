require('babel-register')
const SauceLabs = require('saucelabs')
const chromedriver = require('chromedriver')

// Base

let nightwatchConfig = {
  src_folders: ['e2e'],
  output_folder: false,
}

// Local

if (!process.env.TRAVIS) {

  nightwatchConfig = Object.assign({}, nightwatchConfig, {
    selenium: {
      start_process: true,
      server_path: 'node_modules/selenium-server/lib/runner/selenium-server-standalone-3.0.1.jar',
      host: '127.0.0.1',
      port: 4444,
      cli_args: {
        'webdriver.chrome.driver': chromedriver.path
      }
    },
    test_settings: {
      default: {
        silent: true,
        launch_url: 'http://localhost:9090',
        selenium_port: 4444,
        selenium_host: 'localhost',
        desiredCapabilities: {
          javascriptEnabled: true,
          acceptSslCerts: true
        },
        globals: {
          report,
        },
      },
      chrome: {
        desiredCapabilities: {
          browserName: 'chrome',
        }
      },
    }
  })

// Remote

} else {

  nightwatchConfig = Object.assign({}, nightwatchConfig, {
    selenium: {
      start_process: false,
      server_path: '',
      host: '127.0.0.1',
      port: 4444,
      cli_args: {
        'webdriver.chrome.driver': '',
        'webdriver.ie.driver': '',
      }
    },
    test_workers: {
      enabled: true,
      workers: 'auto',
    },
    test_settings: {
      default: {
        silent: true,
        launch_url: 'http://localhost:9090',
        selenium_port: 80,
        selenium_host: 'ondemand.saucelabs.com',
        username : process.env.SAUCE_USERNAME,
        access_key : process.env.SAUCE_ACCESS_KEY,
        desiredCapabilities: {
          build: `build-${process.env.TRAVIS_JOB_NUMBER}`,
          'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
          javascriptEnabled: true,
          acceptSslCerts: true
        },
        globals: {
          report,
        },
      },
      chrome: {
        desiredCapabilities: {
          browserName: 'chrome',
          platform: 'Linux',
          version: 'latest',
        },
      },
      safari: {
        desiredCapabilities: {
          browserName: 'safari',
          platform: 'Mac 10.11',
        },
      },
      edge: {
        desiredCapabilities: {
          browserName: 'microsoftedge',
        },
      },
    }
  })

}

// Globals

function report(client, done) {
  if (!process.env.TRAVIS) {
    done()
    return
  }

  const saucelabs = new SauceLabs({
    username: process.env.SAUCE_USERNAME,
    password: process.env.SAUCE_ACCESS_KEY
  })

  const sessionid = client.capabilities['webdriver.remote.sessionid']
  const jobName = client.currentTest.name

  saucelabs.updateJob(sessionid, {
    passed: client.currentTest.results.failed === 0,
    name: jobName
  }, done)
}

// Module API

module.exports = nightwatchConfig
