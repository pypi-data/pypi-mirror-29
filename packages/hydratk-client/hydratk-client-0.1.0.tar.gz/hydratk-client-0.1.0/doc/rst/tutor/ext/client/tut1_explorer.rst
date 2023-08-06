.. _tutor_client_tut1_explorer:

Tutorial 1: Explorer
====================

This section shows how to use Explorer.

Create project
^^^^^^^^^^^^^^

Use menu item File/New/Project or New/Project in context menu (right click in explorer area).

  .. image:: fig/explorer_01_new_project.png
  
In Windows create directory and select it. If directory already exists just select it.
In Linux append directory path (directory is created by client).

  .. image:: fig/explorer_02_project_dir.png
  
Project structure is automatically created - libraries, helpers, tests.

  .. image:: fig/explorer_03_project_struct.png
  
Project is added to configuration. Library and helper folders are added to PYTHONPATH.

  .. code-block:: yaml
  
     Projects:
       test:
         path: C:/private/codes/Git/Hydra/test
         pythonpath:
         - C:/private/codes/Git/Hydra/test/lib/yodalib
         - C:/private/codes/Git/Hydra/test/helpers/yodahelpers  
         
Create directory
^^^^^^^^^^^^^^^^

Use menu item File/New/Directory or New/Directory in context menu. 
In Windows create directory and select it. In Linux append directory path (directory is created by client). 

  .. image:: fig/explorer_04_new_directory.png
  
Create file
^^^^^^^^^^^

To create new empty file use menu item File/New/File, New/File in context menu or button New in toolbar.

  .. image:: fig/explorer_05_new_file.png
  
To create new library use menu item File/New/Library or New/Library in context menu.
  
  .. image:: fig/explorer_06_new_library.png
  
To create new helper use menu item File/New/Helper or New/Helper in context menu.  
  
  .. image:: fig/explorer_07_new_helper.png
  
To create new test use menu item File/New/Test or New/Test in context menu.  
  
  .. image:: fig/explorer_08_new_test.png
  
To create new draft use menu item File/New/Draft or New/Draft in context menu.  
  
  .. image:: fig/explorer_09_new_draft.png
  
To create new archive use menu item File/New/Archive or New/Archive in context menu.  
  
  .. image:: fig/explorer_10_new_archive.png    
  
Standard functions
^^^^^^^^^^^^^^^^^^

Explorer supports standard functions accessible from context menu.

* Open - file content is displayed in tab, also available by doubleclick.
* Copy - filepath is copied to clipboard. Directory copy is not supported.
* Paste - paste file from clipboard.
* Delete - delete file, directory or project.
* Refresh - refresh tree, useful when directory content is changed outside of client.