# The goodtables.yml

```yaml
files:
  - source: data.csv
    schema: schema.json
    format: csv
    encoding: utf-8
    skip_rows: 3
    delimiter: ';'

  - source: data.xls
    format: xls
    sheet: 4

datapackages:
  - 'datapackage.json'

settings:
  checks:
    # You can pass check types
    - structure
    - schema
    # ...or individual checks
    - no-headers
    - blank-headers
  skip_checks:
    - duplicate-lines
  error_limit: 1
  table_limit: 1
  row_limit: 5000
  infer_schema: True
  infer_fields: True
  order_fields: True
```
