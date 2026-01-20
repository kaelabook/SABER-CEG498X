# CircleRecognition
## Description
Database class to handle database interactions and configuration storage.
## External Dependencies
- pyyaml
- sqlite3
```
pip install pyyaml pysqlite
```
imported with:
```
import yaml
import sqlite3
```
## File structure (MAKE A REAL TREE THIS LOOKS AWFUL)
```
Database
|
| conf/
  \
  | keys/
  | | AES256_urandKey.key
  |  saber_config.yaml
| images/
 \
  | received/
  | <images>
| Database_SABER.py
```

## Parameters
init parameters
Hough Circle transform modifiable parameters.
| name            | dataType | Description                                                               | defaultValue | 
|---|---|---|---|
| ```self.mode```         | string   |   |           |

## Methods
Publicly callable methods:

## Database interactions


Internal methods that perform database interactions:



