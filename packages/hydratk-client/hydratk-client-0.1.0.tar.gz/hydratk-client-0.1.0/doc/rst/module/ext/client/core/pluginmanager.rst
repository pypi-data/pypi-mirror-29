.. _module_ext_client_core_pluginmanager:

pluginmanager
=============

This sections contains module documentation of pluginmanager module.

PluginManager
^^^^^^^^^^^^^

Class for plugin manager.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _config - Config instance reference

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* config - returns _config

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references.

* get_instance

Returns instance reference, singleton pattern.

* show_manager

Method shows plugin manager window with list of configured plugins and their state.

* _update_state

Method updates plugins state configuration according to requested state (restart is needed to reload plugins). 