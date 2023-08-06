.. _module_ext_client_core_editor:

editor
======

This sections contains module documentation of editor module.

Editor
^^^^^^

Class for Editor frame.

**Attributes** :

* _instance - instance reference
* _instance_created - bool, True if created
* _root - Gui instance reference
* _trn - Translator instance reference
* _config - Config instance reference
* _logger - Logger instance reference
* _explorer - Explorer instance reference
* _yoda_tree - YodaTree instance reference
* _nb - Notebook instance reference
* _var_show_line_number - bool, show line numbers in text
* _var_show_info_bar - bool, show info bar in text
* _font - font settings

**Properties (Getters)** :

* root - returns _root
* trn - returns _trn
* config - returns _config
* logger - returns _logger
* explorer - retunrs _explorer
* yoda_tree - returns _yoda_tree
* nb - returns _nb
* var_show_line_number - returns _var_show_line_number
* var_show_info_bar - returns _var_show_info_bar
* font - returns _font

**Methods** :

* __init__

Constructor, singleton pattern. Initialize references and GUI, parse configuration.

* get_instance

Returns instance reference, singleton pattern.

* _parse_config

Method parses configuration, show line numbers, show info bar, font.

* _set_gui

Method initializes GUI, notebook.

* new_file

Method open new empty tab.

* open_file

Methods read file chosen in dialog, opens new tab with file content and registers file in yoda tree.
If file is already open, the tab is only selected.

* save_as_file

Methods asks for file name via dialog and stores current tab content to file.

* save_file

Methods stores current tab content to file. If file is new, Save as dialog is displayed.

* undo

Method updates current tab content 1 step back.

* redo

Method updates current tab content 1 step forward.

* cut

Method deletes selected text and stores it to clipboard.

* copy

Method stores selected text to clipboard.

* paste

Method writes text from clipboard.

* delete

Method deletes selected text.

* select_all

Method selects whole text content.

* save_tabs

Method asks for saving tabs which have not saved changes.

* show_line_number

Method shows or hides line numbers for all tabs according to setting. Configuration is updated.

* show_info_bar

Method shows or hides info bar for all tabs according to setting. Configuration is updated.

* win_goto

Method displays Goto window, textfield.

* _goto

Method highlights requested line from goto window.

* win_find

Method displays Find window, textfield, checkboxes.

* _find

Method searches for requested string from find window and highlights the occurrences.

* win_replace

Method displays Replace window, textfields, checkboxes.

* _replace

Method searches for requested string from replace window. Found occurrences are replaced and highlighted.

* increase_font

Method sets higher font size for all tabs.

* decrease_font

Method sets lower font size for all tabs.

* on_tab_changed

Method updates yoda tree when tab is changed. If current tab contains jedi file, tree is displayed. Otherwise tree is empty.

* refresh_yoda_tree

Method refreshes yoda tree structure.