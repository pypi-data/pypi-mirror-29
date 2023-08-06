.. _module_ext_client_core_formatter:

formatter
=========

This sections contains module documentation of formatter module.

Formatter
^^^^^^^^^

Class for code automatic text formatting.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _config - Config instance reference
* _patterns - text patterns
* _amend_keys - automatically amended keys

**Properties (Getters)** :

* config - returns _config

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, indent length for patterns.

* _make_patterns

Method sets regular expression for patterns - python keywords, yoda tags, amended keys.

* format_text

Method automatically formats text according to rule (pressed key).

* _amend_key

Method writes key when triggered by configured key, used for brackets.

* _indent

Method indents text for configured patterns - yoda tags, python keywords.