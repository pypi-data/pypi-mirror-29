.. _tutor_client_tut2_editor:

Tutorial 2: Editor
==================

This section shows how to use Editor.

Standard functions
^^^^^^^^^^^^^^^^^^

Editor supports standard functions accessible from menu Edit or context menu (right click).

* Undo - go 1 change back.
* Redo - go 1 change forward.
* Cut - cut text and store it to clipboard.
* Copy - copy text to clipboard.
* Paste - paste text from clipboard.
* Delete - delete text.
* Select all - select whole text content.

* Goto - goto requested line.

  .. image:: fig/editor_01_goto.png
  .. image:: fig/editor_02_goto.png

* Find - find requested string in text.

  .. image:: fig/editor_03_find.png
  .. image:: fig/editor_04_find.png

* Replace - find string in text and replace with requested string.

  .. image:: fig/editor_05_replace.png
  .. image:: fig/editor_06_replace.png
  
Font
^^^^

Text font is configured.

  .. code-block:: yaml
  
     Core:
       font:
         family: Courier New
         size: 12
         style: normal
         
Font size can be changed in editor, use menu items View/Increase font or View/Decrease font. 

Additional bars
^^^^^^^^^^^^^^^

Editor provides line numbers bar and info bar (cursor position). 
Displaying can be enabled/disabled via menu items View/Line numbers and View/Info bar.

The values are also configured.

  .. code-block:: yaml
  
     Core:
       show_info_bar: 1
       show_line_number: 1      
  
Syntax highlighting
^^^^^^^^^^^^^^^^^^^

Editor supports syntax highlighting.
Python keywords, strings, Yoda tags. 

  .. image:: fig/editor_07_syntax_highlighter.png

The colors are configured.

  .. code-block:: yaml
  
     Core:
       color:
         keyword: '#0000FF'
         string: '#008F00'
         yoda: '#A52A2A'
         
Text formatting
^^^^^^^^^^^^^^^

Editor supports automatic text formatting.

Some Python keywords trigger indent (method, class, loop, control condition, ...) and dedent (return, break, pass, ...).
Yoda tags trigger indent. 
     
Indent lengths are configured.     
         
  .. code-block:: yaml
  
     Core:
       format:
         indent_python: 4
         indent_yoda: 2 
        
When you type opening bracket, closing bracket is automatically amended.

Code autocomplete
^^^^^^^^^^^^^^^^^

Editor supports automatic code completion for Python.
Use shortcut Ctrl+Space to show window with available completion.

  .. image:: fig/editor_08_autocomplete.png
  
When only one completion is available it is automatically amended.
Completions are searched in PYTHONPATH and current file (Python or Jedi).

Syntax check
^^^^^^^^^^^^

Editor supports syntax check. Use menu item Source/Syntax check.
The check is available for Python and Jedi files. Found errors are written to log.


  .. image:: fig/editor_09_syntax_check_ok.png
  
  .. image:: fig/editor_10_syntax_check_err.png                         