.. _module_ext_client_plugins_syntaxchecker:

syntaxchecker
=============

This sections contains module documentation of syntaxchecker module.

Plugin
^^^^^^

Class for SyntaxChecker.

**Attributes** :

**Methods** :

* _init_plugin

Method initializes plugin.

* setup

Method sets plugin menu.

* _check_syntax

Method checks syntax of current file content.

* _check

Method checks text syntax according to file extensions.

* _check_python

Method checks syntax of Python file using compile. Error is read from traceback.

* _check_jedi

Method checks syntax of jedi file, YAML format, Yoda format, Python syntax.

* _reformat_test

Method modified test content, lowercase keys for better parsing.

* _check_scenario

Method checks syntax of test scenario, mandatory tags, test case ordering, python blocks syntax.

* _check_case

Method checks syntax of test case, mandatory tags, test condition ordering, python blocks syntax.

* _check_condition

Method checks syntax of test condition, mandatory tags, python blocks syntax.

* _check_python_block

Method checks syntax of Python block using compile. Error is read from traceback.