# Configuration

Goodtables.io is configured via a `goodtables.yml` file in the root directory. For example, you can define:

* Which files goodtables should validate
* Which spreadsheet page should be validated
* What delimiter your CSV file uses (e.g. `;`)
* Which validation checks should be executed

The rest of this page is divided in sections on common things you want to change. For the full reference, check the [goodtables.yml file reference][gtyml-reference].

## Defining the files to validate

By default goodtables validates all files with extension CSV, ODS, XLS, or XLSX, and all files named `datapackage.json`.

You can overwrite the default files in `goodtables.yml`:

```yaml
files:
  - source: data1.csv
    schema: schema1.json
  - source: data2.xls
    schema: schema2.json
```

Alternatively, you can define a pattern like:

```yaml
files: '*.csv'
```

You can also configure how the file is loaded using the options:

```eval_rst
+-----------------------------------+-----------------------------------+
| Option                            | Description                       |
+===================================+===================================+
| format                            | The file format (csv, xls, ...)   |
+-----------------------------------+-----------------------------------+
| encoding                          | The file encoding (utf-8, ...)    |
+-----------------------------------+-----------------------------------+
| skip_rows                         | Either the number of rows to      |
|                                   | skip, or an array of strings      |
|                                   | (e.g. ``#``, ``//``, ...). Rows   |
|                                   | that begin with any of the        |
|                                   | strings will be ignored.          |
+-----------------------------------+-----------------------------------+
```

## Validating data packages

By default goodtables validates all files named `datapackage.json`.

You can overwrite this default in `goodtables.yml`:

```yaml
datapackages:
  - report1/datapackage.json
  - report2/datapackage.json
```

## Validating CSV files with custom dialects

You can configure how the CSV file is loaded by adding one of the following options on `goodtables.yml`:

```yaml
files:
  - source: data.csv
    delimiter: ;
    doublequote: True
    escapechar: \
    lineterminator: \r\n
    quotechar: "
```

The entire list of options can be found on the [Python CSV formatting reference][python-csv-docs].

## Defining the spreadsheet page to validate

By default goodtables validates the first sheet of a spreadsheet.

You can overwrite the default sheet in `goodtables.yml`:

```yaml
files:
  - source: data.xlsx
    sheet: 3
```

## Changing the limit of rows to validate

By default goodtables validates at most 1,000 rows. You can change it in `goodtables.yml`:

```yaml
settings:
  row_limit: 2000
```

## Defining which validation checks are executed

By default goodtables runs all validation checks. You can customize which checks are executed in `goodtables.yml`:

```yaml
settings:
  checks:
    # You can pass check types
    - structure
    - schema
    # ... or individual checks
    - blank-header
    - duplicate-row
    - missing-value
  skip_checks:
    # You can also skip individual checks
    - minimum-constraint
```

Note that if you use the `checks` setting, you have to define all checks you want to be used. Because of this, we recommend using `skip_checks` instead.

The list of validation checks can be found on the [goodtables-py documentation][gtpy-docs].

## Automatically inferring the schema

By default goodtables does not infer the data schema. You can enable inferring in `goodtables.yml`:

```yaml
settings:
  infer_schema: True
  infer_fields: True
```

Goodtables will infer the schema of all files and columns that don't have an explicit schema.

[gtyml-reference]: goodtables_yml.html "goodtables.yml file reference"
[python-csv-docs]: https://docs.python.org/3.6/library/csv.html#csv-fmt-params "Python CSV Formatting docs"
[gtpy-docs]: https://github.com/frictionlessdata/goodtables-py "Goodtables.py documentation"
