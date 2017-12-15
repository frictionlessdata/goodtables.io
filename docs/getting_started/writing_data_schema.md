# Describing your data schema

Without knowledge of the data structure, goodtables is only able to check if the structure of the data is valid. For example, that all rows have the same number of columns, that there are no blank headers, etc. To validate the actual contents, you need to describe the data schema.

The data schema describes what each column should have (strings, numbers, dates), their formats (this string should be an e-mail), and constraints (numbers on age column should be bigger than 18). You can think of it as a kind of data dictionary. The best way to describe the data schema is by writing a data package.

## Instructions

On the root folder of your data, create a `datapackage.json` file with the contents:

```json
{
  "name": "my-dataset",
  "title": "My dataset",
  "resources": [
    {
      "name": "my-data",
      "path": "data/data.csv"
    }
  ]
}
```

This is the simplest tabular data package we can create. Let's see how our data looks like so we can write the table schema for it.

```eval_rst
+------------+------+------+--------+
| date       | from | to   | amount |
+============+======+======+========+
| 2017-01-01 | Jane | John | 1000   |
+------------+------+------+--------+
| 2017-01-15 | Jane | Paul | 500    |
+------------+------+------+--------+
| 2017-02-03 | John | Jane | 2000   |
+------------+------+------+--------+
```

A table schema has three parts: the data type ("string", "number", "date"), the data format ("e-mail", "URI", "ISO date"), and the constraints ("number must be above 18"). Not all columns will have all three parts.

In our data, we have the following columns: 

```eval_rst
+--------+---------+------------+-----------------------+
| column | type    | format     | constraints           |
+========+=========+============+=======================+
| date   | date    | YYYY-MM-DD |                       |
+--------+---------+------------+-----------------------+
| from   | string  |            |                       |
+--------+---------+------------+-----------------------+
| to     | string  |            |                       |
+--------+---------+------------+-----------------------+
| amount | numeric |            | Greater or equal to 0 |
+--------+---------+------------+-----------------------+
```

Writing this as a table schema in our data package, we have:

```json
{
  "name": "my-dataset",
  "title": "My dataset",
  "resources": [
    {
      "name": "my-data",
      "path": "data/data.csv",
      "schema": {
        "fields": [
          {
            "name": "date",
            "type": "date",
            "description": "The transaction date"
          },
          {
            "name": "from",
            "type": "string",
            "description": "Payer"
          },
          {
            "name": "to",
            "type": "string",
            "description": "Payee"
          },
          {
            "name": "amount",
            "type": "numeric",
            "description": "Transaction value in Euros",
            "constraints": {
              "minimum": 0
            }
          }
        ]
      }
    }
  ]
}
```

Note that we didn't have to define the date format explicitly, as the default format is YYYY-MM-DD.

You can find all supported data types, formats and constraints in the [Table Schema specification][tableschema].

[tableschema]: https://frictionlessdata.io/specs/table-schema/ "Table Schema Specification"
