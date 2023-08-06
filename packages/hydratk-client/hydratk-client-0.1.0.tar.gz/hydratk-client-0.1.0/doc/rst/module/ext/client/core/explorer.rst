.. _module_ext_client_core_explorer:

explorer
========

This sections contains module documentation of explorer module.

Explorer
^^^^^^^^

Class for Explorer frame.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _config - Config instance reference
* _editor - Editor instance reference
* _logger - Logger instance reference
* _yoda_tree - YodaTree instance reference
* _autocompleter - AutoCompleter instance reference
* _projects - projects configuration
* _tree - TreeView with project tree
* _vsb - VerticalBar
* _hsb - HorizontalBar
* _menu - context menu
* _menu_new - context submenu

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* config - returns _config
* editor - returns _editor
* logger - returns _logger
* yoda_tree - returns _yoda_tree
* autocompleter - returns _autocompleter

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references and GUI, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, gets projects and populates tree.

* _set_gui

Method initializes GUI, tree, scrollbars, context menu.

* _set_menu

Method initializes context menu.

* _autoscroll

Method provides automatic scrolling for tree position.

* _context_menu

Method displays context menu.

* _populate_project

Method populates requested project.

* _populate_tree

Method populates tree, project is root, directories are nodes, files are leafs.

* _update_tree

Method updates tree content.

* new_file

Method creates new file vie editor method.

* new_project

Method asks for directory and creates project. If project doesn't exist method prepares initial structure.
Windows: root directory is created via dialog, Linux: directory is created via method (dialog provides path).
Otherwise the project is only added to explorer and configuration. Project modules are added to PYTHONPATH.

* new_directory

Method asks for directory and refreshes project tree.
Windows: directory is created via dialog, Linux: directory is created via method (dialog provides path).

* _new_template_file

Method creates new file from template and opens tab. Filepath is provided via dialog.

* new_helper

Method creates helper file from template.

* new_library

Method creates library file from template.

* new_test

Method creates test file from template.

* new_archive

Method creates archive file from template.

* new_draft

Method creates draft file from template.

* _open

Method opens tab with tab content, filepath gets from tree.
If file is already open it selects tab only.

* _copy

Method copies file from tree, path is stored to clipboard.

* _paste

Method pastes to tree, path is read from clipboard.

* _delete

Method deletes file or directory from tree and refreshes tree. Method asks for confirmation.
If file is open it closes appropriate tab.

* refresh

Method refreshes requested part of tree.