.. _module_ext_client_core_translator:

translator
==========

This sections contains module documentation of translator module.

Translator
^^^^^^^^^^

Class for multiple language translation.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _language - language code
* _msg_mod - message module
* _messages - dict, message langtexts

**Methods** :

* __init__

Constructor, singleton pattern. Import message module.

* get_instance

Returns instance reference, singleton pattern.

* _register_messages

Method stores message langtexts.

* _set_language

Method sets used language.

* msg

Method translates langtext to message.