# CloeePy-RabbitMQ
RabbitMQ Plugin for the CloeePy Framework

Attaches a RabbitMQ connection to CloeePy application context.

## Installation

`pip install CloeePy-RabbitMQ`

## Configuration

### Configuration Basics
CloeePy-RabbitMQ configuration must be placed under `CloeePy.Plugins.cloeepy_rabbitmq` in your config file.
The parameters are simply the available `Pika.ConnectionParameters` and `Pika.Credentials`.
For more information on possible configurations please see
[Pika's Documentation](https://pika.readthedocs.io/en/0.10.0/intro.html)

```
CloeePy:
  ...
  Plugins:
    cloeepy_rabbitmq:
      connectionClass: BlockingConnection
      connection:
        host: localhost
        port: 5672
      credentials:
        username: guest
        password: guest
```

### Connection Class

You must specify which of [Pika's Connection Adapters](https://pika.readthedocs.io/en/0.10.0/modules/adapters/index.html#adapters)
you wish to connect with via the `connectionClass` setting. Options are `BlockingConnection` and `SelectConnection`.

### Customize Plugin Namespace

By default, your connection is available on the CloeePy application context as
`app.rabbitmq`. Optionally you can specify a different namespace by which you access
the rabbitmq connection via `pluginNamespace`.

```
...
Plugins:
cloeepy_rabbitmq:
  pluginNamespace: customRabbitMQNS
  connectionClass: BlockingConnection
  connection:
    host: localhost
    port: 5672
  credentials:
    username: guest
    password: guest

```

Then, you would access your Redis connection on the application context like so:

```
app = CloeePy()
result = app.customRabbitMQNS.ping()
app.log.info(result)
```

### Optional Environment Variables

It's best practice NOT to store sensitive data, such as database usernames and passwords,
in plain-text configuration files. Thus, CloeePy-RabbitMQ supports configuring your
password via environment variable.

You need to set the following:

- Username: `CLOEEPY_RABBITMQ_USERNAME`
- Password: `CLOEEPY_RABBITMQ_PASSWORD`

By doing so, you can omit `username` and `password` in your configuration file.


## Usage
```
import os
from cloeepy import CloeePy

if __name__ == "__main__":
  # Required: set config path as environment variable
  os.environ["CLOEEPY_CONFIG_PATH"] = "./example-config.yml"

  # instantiate application instance
  app = CloeePy()

  # Check if RabbitMQ Connection is alive
  if app.rabbitmq.is_open:
    app.log.info("RabbitMQ conection is open")
  else:
    app.log.error("RabbitMQ connection is not open")
```
