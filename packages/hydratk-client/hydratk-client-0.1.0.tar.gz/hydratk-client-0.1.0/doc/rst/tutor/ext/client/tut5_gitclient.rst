.. _tutor_client_tut5_gitclient:

Tutorial 5: GitClient
=====================

This section shows how to use plugin GitClient.
Executive git must be manually installed otherwise the plugin won't be available.
See https://git-scm.com/download/win for Windows or Linux repositories.  

Clone repository
^^^^^^^^^^^^^^^^

Use menu item Plugin/Git client/Clone repository.
Fill repository URL (only HTTP is supported), credentials and target directory path. 
The directory will be created automatically.

  .. image:: fig/gitclient_01_clone_repository.png
  
New project is added to explorer.

  .. image:: fig/gitclient_02_project.png  

Configuration
^^^^^^^^^^^^^

To display Git repositories use menu item Plugin/Git client/Repository manager.

Project has special section with Git repository configuration.
Use button Save to update configuration. Name and email must be configured before first commit.

  .. image:: fig/gitclient_03_configuration.png

  .. code-block:: yaml
  
     Projects:
       test-camp:
         git:
           email: ''
           name: ''
           password: lynus1234
           url: https://git-retail.hydratk.org/test-camp.git
           username: bowman
       path: c:/private/codes/Git/Hydra/test-camp
       pythonpath:
       - c:/private/codes/Git/Hydra/test-camp/lib/yodalib
       - c:/private/codes/Git/Hydra/test-camp/helpers/yodahelpers  

Commit
^^^^^^

Use repository manager to commit your changes. Added, modified and deleted files are displayed in table.
At least one file must be chosen, message and author are also mandatory. Author is pre-filled from configured name and email.
Commit is automatically pushed to remote repository by default (checkbox Push).

  .. image:: fig/gitclient_04_commit.png

Remote repository
^^^^^^^^^^^^^^^^^

Use context menu if repository manager to manipulate with remote repository.
Currently only push and pull commands with one branch are available.
Push uploads local changes. Pull downloads remote changes and tries to merge them.
Merge can fail because of conflicts. In that case you must resolve conflicts manually (use git executive, this is not part of plugin).

  .. image:: fig/gitclient_05_remote.png