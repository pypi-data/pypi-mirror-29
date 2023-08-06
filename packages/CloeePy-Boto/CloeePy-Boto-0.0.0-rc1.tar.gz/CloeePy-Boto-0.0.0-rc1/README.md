# CloeePy-RabbitMQ
Boto Plugin for the CloeePy Framework

Attaches a Boto Session to CloeePy application context.

## Installation

`pip install CloeePy-Boto`

## Configuration

### Configuration Basics
CloeePy-Boto configuration is by environment variables, and text-based
configuration is note supported. All you need to do is ensure
`cloeepy_boto` is listed under `CloeePy.Plugins`

To learn what environment variables to configure, read the
[Boto3 Docs](https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration)


```
CloeePy
  ...
  Plugins:
    cloeepy_boto: {}
```

### Customize Plugin Namespace

By default, your connection is available on the CloeePy application context as
`app.boto`. Optionally you can specify a different namespace by which you access
the rabbitmq connection via `pluginNamespace`.

```
...
Plugins:
  cloeepy_boto:
    pluginNamespace: customBotoNS
```

Then, you would access your Boto connection on the application context like so:

```
app = CloeePy()
result = app.customBotoNS.ping()
app.log.info(result)
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

  # create s3 resource and print bucket names
  s3 = app.boto.resource('s3')
  for bucket in s3.buckets.all():
    print(bucket.name)
```
