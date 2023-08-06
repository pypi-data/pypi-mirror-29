# CloeePy-Mongo
MongoDB Plugin for CloeePy

Attaches a PyMongo DB connection to CloeePy application context

## Installation

`pip install CloeePy-Mongo`

## Configuration

```
CloeePy:
  ...
  Plugins:
    cloeepy_mongo:
      host: localhost
      port: 27017
      username: admin
      password: password
      authSource: admin
      authMechanism: SCRAM-SHA-1
      maxPoolSize: 100
```

## Usage

```
import os
from cloeepy import CloeePy

if __name__ == "__main__":
  # Required: set config path as environment variable
  os.environ["CLOEEPY_CONFIG_PATH"] = "./example-config.yml"

  # instantiate application instance
  app = CloeePy()

  # write a log entry to stdout
  app.log.info("Hello World!")

  # Make PyMongo call and log to stdout
  app.log.info(app.mongo.admin.command("isMaster"))
```
