import os
import subprocess
import flask_testing


class TestE2E(flask_testing.LiveServerTestCase):
    def create_app(self):
        from goodtablesio.app import app

        app.config['LIVESERVER_PORT'] = 9999
        app.config['SERVER_NAME'] = 'localhost:9999'

        return app

    def test_e2e(self):
        browsers = 'chrome'
        if os.environ.get('TRAVIS'):
            browsers = 'chrome,safari,edge'

        test_runner = subprocess.run(
            ['./node_modules/.bin/nightwatch', '-e', browsers]
        )
        assert test_runner.returncode == 0
