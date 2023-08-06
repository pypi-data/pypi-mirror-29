.. _module_ext_client_core_autocompleter:

autocompleter
=============

This sections contains module documentation of autocompleter module.

AutoCompleter
^^^^^^^^^^^^^

Class for code automatic completion. It uses external module `jedi <https://github.com/davidhalter/jedi>`_

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _config - Config instance reference
* _tab - current FileTab instance reference
* _win - Top window
* _tree - TreeView with code completion
* _vbar - VerticalBar

**Properties (Getters)** :

* root - returns _root
* config - returns _config
* tab - returns _tab

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, add modules to PYTHONPATH.

* update_pythonpath

Method add project specific modules to PYTHONPATH.

* _set_gui

Method initializes GUI - window, tree with code autocompletion.

* show_completion

Method shows available code completion for current python or jedi file.
When only completion is available, it is completed.

* _complete

Method writes requested code completion to text.
Functions and classes are completed also with parameters.