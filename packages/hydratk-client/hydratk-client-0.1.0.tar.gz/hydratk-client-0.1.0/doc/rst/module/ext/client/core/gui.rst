.. _module_ext_client_core_gui:

gui
===

This sections contains module documentation of gui module.

Gui
^^^

Main class which implements tk GUI application.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _config - Config instance reference
* _trn - Translator instance reference
* _explorer - Explorer instance reference
* _yoda_tree - YodaTree instance reference
* _editor - Editor instance reference
* _logger - Logger instance reference
* _pluginmanager - PluginManager instance reference
* _plugins - plugin repository
* _help - Help instance reference
* _frame_main - main Frame
* _pane_main - main PanedWindow
* _pane_left - PanedWindow on left side
* _pane_right - PanedWindow on right side
* _menu_bar - Menu bar
* _menus - menu repository
* _toolbar - toolbar Frame
* _tools - dict, tool references
* _tooltips dict, ToolTip references
* _images - dict, PhotoImage references
* _imgdir - directory with images

**Properties (Getters)** :

* cfg - returns _config
* trn - returns _trn
* explorer - returns _explorer
* yoda_tree - returns _yoda_tree
* editor - returns _editor
* logger - returns _logger
* pluginmanager - returns _pluginmanager
* plugins - returns _plugins
* help - returns _help
* tools - returns _tools
* menu_bar - returns _menu_bar
* menus - returns _menus
* tools - returns _tools
* imgdir - returns _imgdir
* images - retutns _images
* pane_left - returns _pane_left
* pane_right - returns _pane_right

**Methods** :

* __init__

Constructor, singleton pattern. Initializes main GUI, exception handler, config, translator.

* get_instance

Returns instance reference, singleton pattern.

* _set_gui

Method calls set of supplement methods to initialize all GUI parts.

* _set_window

Method sets main window parameters - title, logo, initial size, paned window.

* _set_menu

Methods calls set of supplement methods to initialize menu.

* _set_menu_file

Method initializes File menu.

* _set_menu_edit

Method initializes Edit menu.

* _set_menu_view

Method initializes View menu.

* _set_menu_plugin

Method initializes Plugin menu.

* _set_menu_help

Method initializes Help menu.

* _set_toolbar

Method initializes toolbar items.

* set_tool

Method initializes request tool item - button with image, tooltip.

* _set_pane_left

Method calls set of supplement methods to initialize left paned window.

* _set_pane_right

Method calls set of supplement methods to initialize right paned window.

* _set_explorer

Method initializes Explorer frame.

* _set_yoda_tree

Method initializes YodaTree frame.

* _set_editor

Method initializes Editor frame.

* _set_logger

Method initializes Logger frame.

* _load_plugins

Method loads all plugins which are enabled in configuration.

* _exit

Method stops application, dialog confirmation, save tabs, close log.  

ExceptionHandler
^^^^^^^^^^^^^^^^

Class to handle all exceptions which are not properly excepted.

**Attributes** :

* _logger - Logger instance reference

**Methods** :

* __init__

Constructor.

* __call__

Method writes exception to log.