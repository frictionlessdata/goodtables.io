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

![googletables.io high-level design](https://docs.google.com/drawings/d/1NZUILFIZWo9w7U3dQXwB_CdU043QzuIi0rGWkeRsUq4/pub?w=960&h=720)

### Backends

- Auth server provided by Google and GitHub
- Git server, CI runner and CI server all self-hosted GitLab
- Object storage provided by S3

### goodtables.io

- `.goodtables.yml` is defined by a spec we write. This is them passed into a .gitlab.yml file via a new forced commit on our Git server
- Auth UI/API is a pretty general auth handler affair, as per many other apps we have
- Integration UI/API to handle hooking up a client, and general communication with a client once initialised
- Report UI to show GoodTables reports. Such reports can simply be static JSON files on Object storage, created as artifacts of the CI run. The API to access these files would be based on a simple naming convention we employ on S3.

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

### gitlab-ce

[gitlab-ce](https://gitlab.com/gitlab-org/gitlab-ce) is an open source software collaboration platform built around git, with a built in CI server.

At a minimum, gitlab-ce provides:

- A git server
- a CI runner
- a CI server

And we will make the following customisations:

- read the `.goodtables.yml` from an incoming payload, and mixin this data into our own `.gitlab.yml` for executing the CI
- Take the resulting `results.json` from the CI process, and write it to S3

Note that there are several possible ways to make these customisations:

- Through some custom code before and after gitlab in various code paths
- Possibly using some hooks gitlab provides around executing git
- In the CI run itself, for example, to push a results.json to S3

### Auth providers

There are many auth providers: we'll start with Google and GitHub.

We've got plenty of examples of using OAuth 2 backends in various other apps.

### goodtables.yml

`.goodtables.yml` is a file located at the root of the repository (or more generally, the directory) containing he data for validation. It is used to declare which files in the directory are to be run against **goodtables.io**.

#### How will this work?

- `.goodtables.yml` just exposes an API for goodtables config
- when we receive a repo to run data validation, we do a new commit, where we've read the `.goodtables.yml`, taken that info, and put it in a generated `.gitlab.yml`
  - So our git server has at least an extra forced commit for each run. Similar to how we'd sometimes use heroku.
- Our `.gitlab.yml` template is what has the info for running goodtables, for pushing results to S3 and so on.

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
