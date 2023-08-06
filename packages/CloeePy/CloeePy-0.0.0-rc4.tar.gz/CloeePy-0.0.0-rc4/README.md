# CloeePy
Mini Python framework for backend jobs and such. Avoids the HTTP riffraff when you're
not building a web system.

CloeePy uses YAML configuration files, which integrates better with Kubernetes'
ConfigMaps.

**This project is currently in alpha.**

## System Requirements
- Unix-based operating system
- Python 3.3+

## Installation
`pip install CloeePy`

## Configuration
Please see the [example configuration](./example-config.yml) for details of how to configure

A minimal configuration would be:

```
# config.yml

# CloeePy Framework and plugins configuration listed under CloeePy key
CloeePy:
  Logging:
    formatter: text
    level: debug
  Plugins: {}

# Your application specific configurations can go here
CustomVar: custom_value
```

## Usage
Using CloeePy is simple. Just import the framework, tell CloeePy where your config file
is located, and use the plugins that are attached to the application object.

With programs consisting of multiple modules, you can access the CloeePy instance
by re-instantiating it via `app = CloeePy()`. The CloeePy instance is a singleton,
so it will only ever be instantiated once per process.

The only plugin that comes packaged with CloeePy (at this point) is the logger.

```
# main.py

from cloeepy import CloeePy

if __name__ == "__main__":
  # Required: set config path as environment variable
  os.environ["CLOEEPY_CONFIG_PATH"] = /path/to/config.yml

  # instantiate application instance
  app = CloeePy()

  # write a log entry to stdout
  app.log.info("Hello World!")
```


## Background
This package is brought to you by the engineering team at Cloee. We build
Artificial Intelligence for DevOps and Infrastructure as a Service. Many of our
systems run as background jobs, and we weren't quite happy with existing Python
frameworks - as most are designed for building web systems (Django, Flask, Tornado, etc).

Our requirements were:

**Simple, easy-to-use framework for developing non-HTTP backend systems**

We write a lot of cron jobs and message-driven systems, so we don't need request
handling functionality, which is the focus of most existing frameworks.

**Singleton application context that can be accessed from anywhere**

We needed an application context containing configuration, database connections, other
useful stuff, that can be easily accessed from anywhere in our application.
Application context for a CloeePy app is a singleton that can be instantiated
anywhere in the application without running the risk of re-reading configuration
files or overwriting existing database connections.

**YAML driven configuration files**

Most popular python frameworks use python modules as configuration files. Although it's
convenient to do so in many situations, most of our systems run as containers on
Kubernetes. YAML has become the de-facto configuration format for many modern
applications, and Kuberenetes supports YAML-based ConfigMaps that can be added to
a container at startup time.

**Configuration object, NOT configuration dictionary**

Okay, this is a nit-picky one. But when you have deeply nested configurations,
isn't it annoying when all of your configuration data is stored as a Python dictionary?
Wouldn't dot accessors to your configuration data be a lot prettier and easy to
read/write? We think so. Therefore, any dictionaries in your configuration files
are turned into generic Python objets, so you can use the dot accessors like this:

`config.key1.key2.key3`

instead of this:

`config[key1][key2][key3]`.

Nonetheless, if you REALLY like dictionary access, you still have access to
your configuration as a dictionary.

**Extensible via plugins**

You can extend CloeePy by creating plugins. Plugins allow you to create
anything you want and attach it to the application context. This is particularly
useful for managing database connections or sharing common data/objects
throughout your application.

## Maintainers
Scott Crespo (@scottcrespo)

## Contributing
If you would like to contribute, please read the [Contributor's Guide](./CONTRIBUTING.md)
