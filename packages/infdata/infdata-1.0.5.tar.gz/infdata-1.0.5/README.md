# infinity-data

This is a simple package that helps read Infinity data format and get data in such format.

## Quick start

### Get data

Just `pip install infdata`, and start getting data.

For example,
```
$ inf install example.com/posts==crawler-1.0.0
```

installs records that are posts from `example.com`.

### Publish data
```
$ int init                     # initiates folder .inf/
$ inf login                    # saves token to .inf/config
$ inf search example.com/posts # searches for dataset versions
$ inf upload file.json         # uploads Infinity JSON or JSON-L data to specified infinity server
```

**Note:** the tokens `['example.com/posts', 'crawler-1.0.0']` together define a unique `[source-specific, crawler-specific]` schema.

# Infinity JSON

Infinity JSON format includes a header line, which specifies schemas (`[S]`) and types (`[T]`) for its records. 

Example:

```
[
  {'': [[S],[T], 'x': [[S],[T]], 'y': [{'': [[S],[T]], 'z': [[S],[T]]}]},
  {'x': '1,330.98', 'y': [{'z': 1}, {'u': 2}]},
  {'x': '2,011.19', 'y': [{'z': 4}, {'u': 3}]},
]
```

The schemas, types specification for the empty string key `''` specifies the schema and type for the records themselves (required in every level separated by curly braces), whereas the rest of keys specify schemas and types for the data accessible via the keys.

This way, if we want to specify, that the `x` must be casted to a `float`, and means the [elevation](https://www.wikidata.org/wiki/Q2633778), we can do:

```
[
  {'': [], 'x': {'': [['str'],['https://www.wikidata.org/wiki/Q2633778']]}},
  {'x': '1,330.98', 'y': [{'z': 1}, {'u': 2}]},
  {'x': '2,011.19', 'y': [{'z': 4}, {'u': 3}]},
]
```

If you want to additionally, add conversion rules, you can include lambda expression after the final type:

```
[
  {'': [], 'x': {'': [['float', "lambda x: x.replace(',','')"],['https://www.wikidata.org/wiki/Q2633778']]}},
  {'x': '1,330.98', 'y': [{'z': 1}, {'u': 2}]},
  {'x': '2,011.19', 'y': [{'z': 4}, {'u': 3}]},
]
```

This way, the final data becomes:

```
from inf import normalize

normalize(
    [
      {'x': [['float', "lambda x: x.replace(',','')"],['https://www.wikidata.org/wiki/Q2633778']]},
      {'x': '1,330.98', 'y': [{'z': 1}, {'u': 2}]},
      {'x': '2,011.19', 'y': [{'z': 4}, {'u': 3}]},
    ]
)
```

Result is:

```
[
  {'Q2633778': 1330.98, 'y': [{'z': 1}, {'u': 2}]},
  {'Q2633778': 2011.19, 'y': [{'z': 4}, {'u': 3}]},
]
```
