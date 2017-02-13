# goodtables.io

[![Travis](https://img.shields.io/travis/frictionlessdata/goodtables.io/master.svg)](https://travis-ci.org/frictionlessdata/goodtables.io)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/goodtables.io.svg?branch=master)](https://coveralls.io/r/frictionlessdata/goodtables.io?branch=master)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

[![Saucelabs](https://saucelabs.com/browser-matrix/goodtables.io.svg)](https://saucelabs.com/u/goodtables.io)


**Good Tables == Good Times!**

Continuous data validation as a service.

Preliminary designs and specifications can be found in the [wiki](https://github.com/frictionlessdata/goodtables.io/wiki).

## Development

### Installation

We currently use Redis as a broker:

```bash
sudo apt-get install redis-server
```

Prepare Python and Node virtual environments:

```bash
git clone git@github.com:frictionlessdata/goodtables.io.git
cd goodtables.io
virtualenv .python -p python3.5
source .python/bin/activate
nvm install 6
nvm use 6
npm run init
```

Create `.env` file with environment variables:

```bash
$ cp .env.example .env
$ editor .env # edit your vars

```

### Migrations

```bash
npm run migrate # migrate
alembic downgrade -1 # downgrade
alembic revision -m '<name>' # add a migration
```

### Running the app

Start the Celery worker and dev server:

```bash
bash1$ npm run celery:dev
bash2$ npm run server:dev
```

Now developmet server runs on `localhost:5000`. We could send github repo for validation getting job identifiers as a response:

> POST localhost:5000/github/hook/

```json
{
  "repository": {
      "clone_url": "https://github.com/roll/goodtables-example.git"
    }
}
---
693f40f0-fcad-416e-b2c7-a5beebff4f44
```

> GET localhost:5000/api/job/693f40f0-fcad-416e-b2c7-a5beebff4f44

```json
{
  "report": {
    "created": "Mon, 14 Nov 2016 12:42:41 GMT",
    "finished": "Mon, 14 Nov 2016 12:42:43 GMT",
    "report": {
      "error-count": 1,
      "errors": [],
      "table-count": 2,
      "tables": [
        {
          "error-count": 1,
          "errors": [
            {
              "code": "blank-header",
              "column-number": 3,
              "message": "Header in column 3 is blank",
              "row": null,
              "row-number": null
            }
          ],
          "headers": [
            "id",
            "name",
            "",
            "name"
          ],
          "row-count": 2,
          "time": 0.964,
          "valid": false
        },
        {
          "error-count": 0,
          "errors": [],
          "headers": [
            "id",
            "name"
          ],
          "row-count": 3,
          "time": 0.945,
          "valid": true
        }
      ],
      "time": 0.981,
      "valid": false
    },
    "id": "693f40f0-fcad-416e-b2c7-a5beebff4f44"
  },
  "status": "SUCCESS"
}
```

### Frontend building

To build frontend files to `public` directory:

```bash
npm run build:dev
# npm run build:prod

```

### Dependencies locking

To lock the dependencies:

```bash
npm run deps
# npm run deps:back
# npm run deps:front
```

### Unit testing

To run unit tests for the whole application with linting and coverage:

```bash
npm run test
# npm run test:back
# npm run test:front
```

### E2E testing

To run user acceptance end-to-end tests for the whole application:

```bash
npm run spec
```

## Alpha version

**Note**: the current site is in an early alpha version and things are bound to break and change.

The current alpha version supports adding two data sources, GitHub repositories and Amazon S3 buckets.

To try it out, go to http://goodtables.oklabs.org and log in with your GitHub account

To add a Github Repo:

* Click on the "Add Repository" button from the dashboard.
* If you don't see a list of your repositories, click on the "Sync account" button. This might take a while.
* Once the list of repositories appears, click "Activate" on the repository that you want to validate.
* From now on, every time you push to that repository a validation job will be run on goodtables.io.
* You also should see the validation status next to the commit messages and pull requests (note that this only works on repositories in the `frictionlessdata` organization due to #132):

![dealwithit 1](https://cloud.githubusercontent.com/assets/200230/20802449/001ee8c4-b7e4-11e6-9e8b-b88390a659c7.png)

The statuses link to the full report on the prototype app.


To add an S3 Bucket:

* Click on the "Add Bucket" button from the dashboard.
* Enter an AWS Access Key Id and a Secret Access Key pair, and the name of the bucket. Your keys should allow reading the contents of the bucket, as well as creating notification events on it. Click on "Add bucket"
* From now on, every time you update a file on the S3 bucket (upload or delete) a validation job will be run on goodtables.io.
