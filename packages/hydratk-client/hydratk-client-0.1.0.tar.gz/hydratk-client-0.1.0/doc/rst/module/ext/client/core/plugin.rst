.. _module_ext_client_core_plugin:

plugin
======

This sections contains module documentation of plugin module.

Plugin
^^^^^^

Class for plugin manager.

**Attributes** :

* _plugin_id - id
* _plugin_name - name
* _plugin_version - version
* _plugin_author - author
* _plugin_year - year
* _root - Gui instance reference
* _config - Config instance reference
* _trn - Translator instance reference
* _explorer - Explorer
* _yoda_tree - YodaTree instance reference
* _editor - Editor instance reference
* _logger - Logger instance reference
* _cfg - plugin configuration

**Properties (Getters)** :

* plugin_id - returns _plugin_id
* plugin_name - returns _plugin_name
* plugin_version - returns _plugin_version
* plugin_author - returns _plugin_author
* plugin_year - returns _plugin_year
* root - returns _root
* config - returns _config
* trn - returns _trn
* explorer - returns _explorer
* yoda_tree - returns _yoda_tree
* editor - returns _editor
* logger - returns _logger
* cfg - returns _cfg

**Methods** :

* __init__

Constructor. Set references, initialize plugin, import messages and images, execute plugin setup.

* _import_messages

Method imports plugin langtexts and adds them to translator repository.

* _import_images

Methos imports plugin images and adds them to root repository.

* _set_tool

Method sets tool button in tooolbar. To be used in plugin setup.

* _set_menu

Method sets new menu in existing menu or in menubar. To be used in plugin setup.

* _set_menu_item

Methods sets new menu item and links it with command callback (and optional shortcut). To be used in plugin setup.