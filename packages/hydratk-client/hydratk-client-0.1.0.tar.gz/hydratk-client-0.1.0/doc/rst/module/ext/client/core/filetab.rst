.. _module_ext_client_core_filetab:

filetab
=======

This sections contains module documentation of filetab module.

FileTab
^^^^^^^

Class for FileTab frame.

**Attributes** :

* _nb - Notebook instance reference
* _editor - Editor instance reference
* _colorizer - Colorizer instance reference
* _formatter - Formatter instance reference
* _autocompleter - AutoCompleter instance reference
* _name - tab name
* _path - tab filepath
* _last_find_str - last string to find
* _disable_format - bool, disable automatic text formatting
* _text - Text reference
* _ln_bar - line number bar
* _info_bar - info bar
* _vbar - VerticalBar
* _hbar - HorizontalBar
* _menu - context menu

**Properties (Getters)** :

* nb - returns _nb
* editor - returns _editor
* colorizer - returns _colorizer
* formatter - returns _formatter
* autocompleter - returns _autocompleter
* text - returns _text
* name - returns _name
* path - returns _path

**Methods** :

* __init__

Constructor. Initialize references and GUI.

* _set_gui

Method initializes GUI - text area, scrollbars, line number bar, info bar, context menu.

* _set_menu

Method sets context menu.

* _context_menu

Method displays context menu.

* set_font

Method sets font (family, size, style) for text area and line number bar.

* _get_line_numbers

Method prepares content for line number bar.

* update_line_numbers

Method updates line number bar content according to events if enabled.

* update_info_bar

Method updates info bar content according to events if enabled.

* highlight_line

Method highlights requested line in text area.

* _on_key_press

Method handles key press event, line number and info bar, line highlight.

* _on_key_release

Method handles key release event, line number and info bar, line highlight, colorizing, text formatting, yoda tree refresh.

* _on_mouse_click

Method handles mouse click event, info bar, line highlight.

* _on_vsb

Method handles vertical scrolling, synchronize text area and line number.

* _on_mouse_wheel

Method handles mouse wheel event, synchronize text area and line number.
Event names are different for Windows (1 event, direction in event detail) and Linux (2 events for 2 directions).
 
* _change_font_size

Method changes text font size according to mouse wheel.

* goto

Method highlights request line, line number and info bars are synchronized with text area.

* find

Method searches text for requested string, occurrences are highlighted.

* replace

Method searches text for requested string, occurrences area replaced and highlighted.

* colorize

Method colorizes text content.

* _format_text

Method formats text content if enabled.

* _show_autocomplete

Method displays autocomplete window.

* disable_format

Method disables automatic text formatting. Used for code autocompletion.