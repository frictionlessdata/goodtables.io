# goodtables.io

## Overview

**Good Tables == Good Times!**

Continuous data validation as a service.


## User stories

GoodTables is part of the [Frictionless Data](http://frictionlessdata.io) project, which has a Trello board for user stories [here](https://trello.com/b/MGC4RpTZ). All these user stories are validated not only by our own use cases at Open Knowledge International, but also by a number of potential users we've been talking to around pilots for Frictionless Data specs and tooling.

A number of user stories related to data validation can be found there. Some of the most important are noted here:

- As a {Publisher} I want to be able to check that every time I update my data it is still good (conforms to schema) so that I can catch errors early and publish reliable data.
- As a {Researcher/Publisher} I want validate my data with a minimum of clicks, so that I can feel trust in the validity and usefulness of the data.
- As a {Developer} I want an online service that is connected to my data repository (e.g. git repo) that validates data on update so that I can delegate data validation to a third party.
- As a {Government Publisher} I want to make it easy to prove that our published data is valid so that I can claim that we are living up to our transparency commitments.
- As a {Civic Tech Activist} I want to make it easy to assess the quality of data published by the government so that I can make sure that government is living up to its transparency commitments.


## High-level design

![googletables.io high-level design](https://docs.google.com/drawings/d/1emknr4Qy74lx9uQ-YSoJB_v9bLAwq6msUBmxhhnxwig/pub?w=960&h=720)

### Backends

- Auth server provided by Google and GitHub
- Job runner powered by Celery
- Object storage provided by S3

### goodtables.io

- `.goodtables.yml` is defined by a spec we write. This is passed to the runner with the files (or linsk to the the files) to configure the validation.
- Auth UI/API is a pretty general auth handler affair, as per many other apps we have
- Integration UI/API to handle hooking up a client, and general communication with a client once initialised
- Report UI to show GoodTables reports. For a MVP such reports can simply be static JSON files on Object storage, uploaded by the job runner. The API to access these files would be based on a simple naming convention we employ on S3. Future versions could have more elaborate UIs with lists of previous jobs, etc.

### Clients

- GitHub integration modeled almost exactly as travis
- Other integrations can come later


## Components

### goodtables.io UI

The user interface at [goodtables.io](https://goodtables.io).

At a minimum, the user can:

- Authenticate
- Connect to a client, and then choose her repositories and/or directories from that client
- For each repository, see a history (list) of reports, and view a detail page for each report
- For each repository, re-run a report

### Client UIs

The integration with client interfaces where applicable. The main use case is GitHub.

At a minimum, a user can:

- Authorize or deauthorize the connection to goodtables.io
- See goodtables.io results on each pull requests
- integrate a badge (or badges) in some html, such as integrating in a README.

### goodtables lib

[goodtables](https://github.com/frictionlessdata/goodtables) is a Python package that performs all data validation.

At a minimum, the package provides:

- The ability to validate CSV, Excel and ODS files
- The ability to validate structural issues, and schema issues
- The ability to infer (and validate with) a schema, if a schema is not present
- Validation against the [data-quality-spec](https://github.com/frictionlessdata/data-quality-spec)
- An output report on the validation run, available in a number of formats, including as JSON

### goodtables.yml

`.goodtables.yml` is a file located at the root of the repository (or more generally, the directory) containing the data for validation. It is used to declare which files in the directory are to be run against **goodtables.io**.

### Celery validation jobs

[Celery](http://www.celeryproject.org/) is a asynchronous task queue that will be used to schedule and run the validation jobs.

Validation jobs

- read the `.goodtables.yml` from an incoming payload to extract the files to be validated and other configuration options.
- run the validation on all required files
- Take the resulting `results.json` report and write it to S3

### Auth providers

There are many auth providers: we'll start with Google and GitHub.

We've got plenty of examples of using OAuth 2 backends in various other apps.


#### A proposed config

```
# .goodtables.yml

# everything that is tabular
files: '*'

# everything that is csv
files: '*.csv'

# everything that is tabular in a certain directory
files: 'data/*'

# specifics
files:
  -
    path: 'budget.csv'
    schema: 'schemas/budget.json'
  -
    path: 'budget2.csv'
    schema: 'schemas/budget.json'
  -
    path: 'companies.csv'
    schema: 'schemas/companies.json'
```
