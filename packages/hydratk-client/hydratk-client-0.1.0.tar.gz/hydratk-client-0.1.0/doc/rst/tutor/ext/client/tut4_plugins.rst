.. _tutor_client_tut4_plugins:

Tutorial 4: Plugins
====================

This section shows how to use Plugins.

Plugin manager
^^^^^^^^^^^^^^

Installed plugins must be properly configured. 
See minimum configuration. Each plugin also can have specific items.

  .. code-block:: yaml
  
     Plugins:
       SyntaxChecker:
         package: hydratk.extensions.client.plugins.syntaxchecker
         module: syntaxchecker
         enabled: 1
         
Enabled plugins are loaded within application start.
Use menu item Plugin/Plugin manager to enable/disable plugins.
The application must be restarted to reload plugins.

  .. image:: fig/plugin_01_manager.png