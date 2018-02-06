export default {
  home: (client) => {
    client
      .url(client.launch_url)
      .waitForElementVisible('h1', 5000)
      .assert.containsText('h1', 'Publish data with confidence')
      .end();
  },
  afterEach: (client, done) => {
     client.globals.report(client, done);
  },
};
