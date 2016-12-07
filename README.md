# goodtables.io

[![Travis](https://img.shields.io/travis/frictionlessdata/goodtables.io/master.svg)](https://travis-ci.org/frictionlessdata/goodtables.io)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/goodtables.io.svg?branch=master)](https://coveralls.io/r/frictionlessdata/goodtables.io?branch=master)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

**Good Tables == Good Times!**

Continuous data validation as a service.


Preliminary designs and specifications can be found in the [wiki](https://github.com/frictionlessdata/goodtables.io/wiki).

## Development installation

We currently use Redis as a broker:

    sudo apt-get install redis-server

Install the Python package:

    git clone git@github.com:frictionlessdata/goodtables.io.git
    cd goodtables.io
    pip install -r requirements.txt
    python setup.py develop

Create `.env` file with environment variables:

```bash
$ cp .env.example .env
$ editor .env # edit your vars

```

Migrations:
- migrate - `make migrate`
- downgrade - `alembic downgrade -1`
- add migration - `alembic revision -m '<name>'`

## Quickstart

Start the Celery worker and dev server:

```bash
bash1$ make celery-dev
bash2$ make server-dev
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
    "job_id": "693f40f0-fcad-416e-b2c7-a5beebff4f44"
  },
  "status": "SUCCESS"
}
```
