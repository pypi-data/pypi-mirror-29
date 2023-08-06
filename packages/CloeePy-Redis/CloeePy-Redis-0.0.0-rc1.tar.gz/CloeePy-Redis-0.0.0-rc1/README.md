# CloeePy-Redis
Redis Plugin for the CloeePy Framework

Attaches a Redis connection to CloeePy application context.

## Installation

`pip install CloeePy-Redis`

## Configuration

### Configuration Basics
CloeePy-Redis configuration must be placed under `CloeePy.Plugins.cloeepy_redis` in your config file.
The parameters are simply the available `Redis-Py.StrictRedis` connection parameters. For more
information on possible configurations please see [Redis-Py's Documentation](http://redis-py.readthedocs.io/en/latest/)

```
CloeePy:
  ...
  Plugins:
    cloeepy_redis:
      host: localhost
      port: "6379"
      password: "secret"
```

### Customize Plugin Namespace

By default, your Redis connection is available on the CloeePy application context as
`app.redis`. Optionally you can specify a different namespace by which you access
the redis connection via `pluginNamespace`.

```
...
Plugins:
  cloeepy_redis:
    pluginNamespace: customRedisNS
    host: localhost
    port: "6379"
    password: "secret"

```

Then, you would access your Redis connection on the application context like so:

```
app = CloeePy()
result = app.customRedisNS.ping()
app.log.info(result)
```

### Optional Environment Variables

It's best practice NOT to store sensitive data, such as database usernames and passwords,
in plain-text configuration files. Thus, CloeePy-Redis supports configuring your
password via environment variable.

You need to set the following:

- Password: `CLOEEPY_REDIS_PASSWORD`

By doing so, you can omit `password` in your configuration file.


## Usage
```
import os
from cloeepy import CloeePy

if __name__ == "__main__":
  # Required: set config path as environment variable
  os.environ["CLOEEPY_CONFIG_PATH"] = "./example-config.yml"

  # instantiate application instance
  app = CloeePy()

  # Make Redis call and log to stdout
  app.log.info(app.redis.ping())
```
