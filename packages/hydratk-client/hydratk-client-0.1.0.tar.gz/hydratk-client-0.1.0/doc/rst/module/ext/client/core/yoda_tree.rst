.. _module_ext_client_core_yoda_tree:

yoda_tree
=========

This sections contains module documentation of yoda_tree module.

YodaTree
^^^^^^^^

Class for code YodaTree frame. It uses external module `pyyaml <https://pyyaml.org>`_

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _config - Config instance reference
* _editor - Editor instance reference
* _logger - Logger instance reference
* _tree - TreeView
* _vsb - VerticalBar
* _hsb - HorizontalBar
* _menu - context menu
* _tests - dict, test configuration
* _current_test - currently displayed test
* _hidden_tags - tags hidden in tree
* _indent - indent length

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* config - returns _config
* editor - returns _editor
* logger - returns _logger

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references and GUI, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, hidden tags, indent length.

* _set_gui

Method initializes GUI, tree view, scrollbars.

* _context_menu

Method displays context menu.

* _autoscroll

Method provides automatic scrolling for tree position.

* add_test

Method adds file to storage, jedi files are parsed and tree is populated.

* get_test

Method returns requested test configuration.

* delete_test

Method deletes requested test.

* refresh

Method refreshes tree content, content is reparsed.

* _populate_tree

Method populates tree, some tags and values are not displayed.

* clear_tree

Method clears tree content.

* _display_item

Method checks if requested item can be displayed. 
Some tags are hidden, values with code blocks are not displayed.

* _highlight_item

Method highlights line in text are for selected tree item.

* _set_menu

Method initializes context menu according to selected tree item.
Scenario, case and condition have different available tags. Some tags can't be duplicated.

* _add_item

Method writes text block from template and highlights the line.

* _find_item

Method finds position of requested item in text.

* _prepare_add_scenario

Method prepares test scenario content from template and calculates block position in text.

* _prepare_add_case

Method prepares test case content from template and calculates block position in text.

* _prepare_add_condition

Method prepares test condition content from template and calculates block position in text.

* _prepare_add_prereq

Method prepares pre-requirements content from template and calculates block position in text.

* _prepare_add_postreq

Method prepares post-requirements content from template and calculates block position in text.

* _prepare_add_events

Method prepares events content from template and calculates block position in text.