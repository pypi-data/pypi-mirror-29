.. _tutor_client_tut3_yoda_tree:

Tutorial 3: YodaTree
====================

This section shows how to use YodaTree.

Test tree
^^^^^^^^^

Current test content is parsed and displayed in tree form.
Each item is highlighted in text after click.

  .. image:: fig/yoda_tree_01_tree.png

Some Yoda tags are hidden to display shorter tree.
Tags are configured. 

  .. code-block:: yaml
  
     Core:
       yoda:
         hidden_tags: Author,Id,Path,Desc,Version,Pre-Req,Post-Req,Events,Test,Validate
         
Test design
^^^^^^^^^^^

Client supports test design. It is not necessary to deal with Yoda format.
Available actions are offered in context menu (right click on requested tag).

* Test-Scenario - add test scenario, test case, pre-requirement, post-requirements, events

  .. image:: fig/yoda_tree_02_add_case.png

* Test-Case - add test condition, events

  .. image:: fig/yoda_tree_03_add_condition.png
  
* Test-Condition - add events          

  .. image:: fig/yoda_tree_04_add_events.png
  
Use menu item Plugin/Syntax check to check test content.
Found errors are written to log.

  .. image:: fig/yoda_tree_05_syntax_check_ok.png
  
  .. image:: fig/yoda_tree_06_syntax_check_err.png  