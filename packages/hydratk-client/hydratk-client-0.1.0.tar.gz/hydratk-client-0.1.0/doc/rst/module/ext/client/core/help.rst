.. _module_ext_client_core_help:

help
====

This sections contains module documentation of help module.

Help
^^^^

Class for help menu.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references.

* get_instance

Returns instance reference, singleton pattern.

* win_about

Method displays About window, text area, buttons with hyperlinks opened in browser or mail client.

* web_tutor

Method opens tutorial in browser.

* web_doc

Method opens documentation in browser.