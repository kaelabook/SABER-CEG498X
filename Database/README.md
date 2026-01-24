# CircleRecognition
## Description
Database class to handle database interactions and configuration storage.
## External Dependencies
- pyyaml

```
pip install pyyaml
```
imported with:
```
import yaml
```
## File structure
```
/ (This Directory)
/conf/
/conf/keys/
/images/
/images/received/<received images>
/images/<images to be transmitted>
/Database_SABER.py
```

## Parameters
init parameters
| name | dataType | Description | defaultValue | 
|---|---|---|---|
| ```self.mode``` | string   | Mode, 'origin', 'server', or 'dbTest'.dbTest currently does nothing but is a placeholder for future capability. Modes choose the schema for the primary database for each raspberry Pi each. The receive database or "server" has a slightly different structure and load process than the source or origin side. | Init parameter, must be included on instanciation, the default is 'origin'. |
| ```self.configPath``` | string  | Path to the configuration file | 'conf/saber_config.yaml'  |


## Methods
Publicly callable methods:
### Constructors:
```loadVal(table, col, val)``` and ```load<N>Vals(table, cols: tuple, vals: tuple)```

Both methods take in a column and value to load values into new rows to a specified ```table```, up to 4 at a time if ```loadFourVals(...)``` is called. This is used for database initialization and isn't typically used externally but can be. Loaded via a parameterized INSERT OR IGNORE INTO statement.

### Mutators:
```setValue(table, destCol, destVal, checkCol, checkVal)```

Changes the value of cells in the ```table``` conditionally where certain values in certain columns align, this is placed in the selected table via ```destVal``` and ```destCol```, the specific row is selected with ```checkCol``` and ```checkVal``` which will place data where the selected check Columns and Values align.

### Accessors:
```getValue(table, checkCol, checkVal, reqCol)```

Retrieves data in a specified ```reqCol``` that aligns with a specified ```checkCol``` and ```checkVal``` in a specified ```table```.

```bulkRetrieval(table, col)```

Retrieves and returns every value in a specified column of a specified ```table```. Returns the retrieved values and associated ids.

```conditionalBulkRetrieval(table, col, checkCol, checkVal)```

Retrieves all data that aligns with specified ```checkVal``` in a specified ```checkCol``` used for non-unique columns to grab all data, it returns values from a specied ```col``` in a specified ```table```.



## Database Schema
1. Origin
     - id, Integer, primary key, generated automatically.
   - path, Text, must be unique, this is the abslute path to each image.
   - imageName, Text, must be unique, this is the name of each image, used for debug/testing purposes, irrelevant for final function.
   - hasRed, Integer, (either 1 or 0), is used to determine if an image is to be ignored entirely even for red-circle validation.
   - hasCircle, Integer (either 1 or 0), is the authoratative answer on the presence of a red circle, used to determine what images will be transmitted.
   - serializedImage, Text (BLOB) , Unique , Base64 encoded image.
   - encryptedImage, Text (BLOB) , Unique , AES-256 encrypted version of serializedImage.
   - nonce, Text, Unique, crypto Nonce for the encrypted image.
   - tag, Text, Unique, hash used to validate encryption prior to decryption
   - generatedHash, Text, Unique, hash that is generated to validate transmission integrity. 
2. Server
     - id, Integer, primary key, generated automatically.
   - path, Text, must be unique, this is the abslute path to each image.
   - imageName, Text, must be unique, this is the name of each image, used for debug/testing purposes, irrelevant for final function
   - serializedImage, Text (BLOB) , Unique , Base64 encoded image.
   - encryptedImage, Text (BLOB) , Unique , AES-256 encrypted version of serializedImage.
   - nonce, Text, Unique, crypto Nonce for the encrypted image.
   - tag, Text, Unique, hash used to validate encryption prior to decryption
   - receivedHash, Text, Unique, hash that was received used to validate against a generated hash prior to decryption
3. config
   - id, Integer, unique, generated automatically.
   - type, Text, unique, describes the type of cofiguration value the row is
   - path, Text, unique, path key that links a path to the type of configuration major key.


## Configuration Schema
YAML formatted configuration file in the general form of MajorKey.MinorKey.Value. Current major minor KeyPairs:
```images_origin.path.<value>```

```images_origin.type.<value>```

```images_server.path.<value>```

```images_server.type.<value>```

```aes_key.path.<value>```

```aes_key.path.<value>```


