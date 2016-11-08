# goodtables.io


**Good Tables == Good Times!**

Continuous data validation as a service.


Preliminary designs and specifications can be found in the [wiki](https://github.com/frictionlessdata/goodtables.io/wiki).

## Development installation

We currently use Redis as a broker and result storage:

    sudo apt-get install redis-server

Install the Python package:

    git clone git@github.com:frictionlessdata/goodtables.io.git
    cd goodtables.io
    pip install -r requirements.txt
    python setup.py develop

## Quickstart

Start the Celery worker:

    celery -A goodtablesio.tasks worker --loglevel=info

You can use the `goodtablesio` command line helper to send validation tasks to the queue:

    goodtablesio https://raw.githubusercontent.com/amercader/newcastle-libraries-data/master/councillors-wards.csv

or

    goodtablesio  /path/to/local/file.csv
