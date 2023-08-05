# autoalchemy
[![Build Status](https://travis-ci.org/ericchang00/autoalchemy.svg?branch=master)](https://travis-ci.org/ericchang00/autoalchemy)

Automatically generate a schema from raw data files and push it to a database. Uses [pandas](https://pandas.pydata.org/) to perform type inference and [SQLAlchemy](https://www.sqlalchemy.org/) for database connections. Works with all databases supported by SQLAlchemy (MySQL, PostgreSQL, Microsoft SQL Server, SQLite, and more).

### Installation

```sh
pip install autoalchemy
```

### Usage

To use `autoalchemy`, provide paths to the data directory and a configuration file. The quickest way to do is is through the cli:

```sh
autoalchemy /path/to/data_directory /path/to/config.json
```

Or, import and call the python module.

```python
import autoalchemy

directory = '/path/to/data_directory'
config = '/path/to/config.json'

autoalchemy.build_database(directory=directory, config=config, drop_existing=False)
```

### Tests

```sh
pytest tests.py
```
