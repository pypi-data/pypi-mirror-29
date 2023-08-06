# CloeePy
Mini Python framework for backend jobs and such. Avoids the HTTP riffraff when you're
not building a web system.

CloeePy uses YAML configuration files, which integrates better with Kubernetes'
ConfigMaps.

## System Requirements
- Unix-based operating system
- Python 3.x

## Installation
`pip install CloeePy`

## Configuration
Please see the [sample configuration] for details of how to configure Cloee

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

**Configuration Object, NOT a Configuration Dictionary**

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
