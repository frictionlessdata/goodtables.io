# Validating data on GitHub

This is a very short tutorial on using goodtables.io to continuously validate data hosted on [GitHub][github].

## Pre-requisites

* Tabular data on a [GitHub repository][gh-new-repo]

## Instructions

1. Login on [goodtables.io][gtio] using your GitHub account and accept the permissions confirmation.
1. Once we've synchronized your repository list, go to the [Manage Sources][gtio-managesources] page and enable the repository with the data you want to validate.
    * If you can't find the repository, try clicking on the Refresh button on the Manage Sources page

Goodtables will then validate all tabular data files (CSV, XLS, XLSX, ODS) and [data packages][datapackage] in the repository. These validations will be executed on every change, including pull requests.

## Next steps

* Add a badge to your README to display your data validation status. The instructions are on the "Get badge" tab in the data report page.
* [Write a table schema][gtio-dataschema] to validate the contents of your data
* [Configure which files are validated and how][gtio-configuring]

[gtio]: https://goodtables.io/ "Goodtables.io"
[github]: https://github.com/ "GitHub"
[gh-new-repo]: https://help.github.com/articles/create-a-repo/ "GitHub: Create new repository tutorial"
[gtio-managesources]: https://goodtables.io/settings "Goodtables.io: Manage sources"
[datapackage]: https://frictionlessdata.io/data-packages/ "Data Package"
[gtio-dataschema]: writing_data_schema.html "Writing a data schema"
[gtio-configuring]: configuring.html "Configuring goodtables.io"
