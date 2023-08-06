.. _module_ext_client_core_colorizer:

colorizer
=========

This sections contains module documentation of colorizer module.

Colorizer
^^^^^^^^^

Class for code syntax highlighting.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _config - Config instance reference

**Properties (Getters)** :

* config - returns _config

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, pattern colors.

* _make_patterns

Method sets regular expression for patterns - keyword, string, yoda tag.

* colorize

Method searches patterns in text. Text is colorized according to found pattern.