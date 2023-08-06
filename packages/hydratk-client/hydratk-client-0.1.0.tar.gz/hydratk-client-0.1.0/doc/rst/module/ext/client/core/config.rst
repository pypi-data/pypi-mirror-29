.. _module_ext_client_core_config:

config
======

This sections contains module documentation of config module.
It uses external module `pyyaml <https://pyyaml.org>`_

Config
^^^^^^

Class for configuration storage.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _path - configuration filepath
* _data - dict, parsed content

**Properties (Getters)** :

* data - returns _data

**Methods** :

* __init__

Constructor, singleton pattern. Load configuration from file.

* get_instance

Returns instance reference, singleton pattern.

* _load

Method opens configuration file and parses YAML format to dict.

* save

Method saves current (in memory) configuration data to file in YAML format.