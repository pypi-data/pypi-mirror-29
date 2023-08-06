.. _module_ext_client_core_logger:

logger
======

This sections contains module documentation of logger module.

Logger
^^^^^^

Class for Logger frame.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _config - Config instance reference
* _log - Text reference
* _menu - context menu
* _log_levels - log level translation num2str
* _level - current log level
* _msg_format - message format
* _logdir - log directory
* _logfile - log filepath

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* config - returns _config
* logfile - returns _logfile

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, directory, log level, message format.

* _set_gui

Method initializes GUI, text area, scrollbar, context menu.

* _set_menu

Method initializes context menu.

* _context_menu

Method displays context menu.

* _write_msg

Method writes requested log message  to text area and file.
Messages with lower level are ignored, errors and warnings are highlighted.

* debug

Method writes DEBUG message.

* info

Method writes INFO message.

* warn

Method writes WARN message.

* error

Method writes ERROR message.

* _clear

Method clears text area.