.. install_ext_client:

Client
======


You have 2 options how to install DataGen extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk-client
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-client
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.     

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-client.git
     $ cd ./hydratk-client
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://python.org/pypi/hydratk-client -O hydratk-client.tar.gz
     $ tar -xf hydratk-client.tar.gz
     $ cd ./hydratk-client
     $ sudo python setup.py install
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.    
     
Requirements
^^^^^^^^^^^^     
     
Several python modules are used.
These modules will be installed automatically, if not installed yet (for Python 2.7).

  .. note::
  
     Tkinter (GUI framework) must be installed. It is already packed with Python distributions for Windows.
     Some Linux distributions don't have it packed. In that case follow instructions for your OS.
     Plugin GitClient requires git executable which is not installed automatically.
     See https://git-scm.com/download/win for Windows or Linux repositories.  

* pyyaml
* jedi
* GitPython  
     
Installation
^^^^^^^^^^^^

See installation example, Linux, Python 2.7.

  .. code-block:: bash
  
     running install
     running bdist_egg
     running egg_info
     running install_lib
     running build_py
     creating build/bdist.linux-x86_64/egg
     creating build/bdist.linux-x86_64/egg/hydratk
     ...
     
     Processing hydratk_client-0.1.0.dev0-py2.7.egg
     creating /root/.pyenv/versions/2.7.13/envs/p27/lib/python2.7/site-packages/hydratk_client-0.1.0-py2.7.egg
     Extracting hydratk_client-0.1.0.dev0-py2.7.egg to /root/.pyenv/versions/2.7.13/envs/p27/lib/python2.7/site-packages
     Adding hydratk-client 0.1.0.dev0 to easy-install.pth file
     Installing htkclient script to /root/.pyenv/versions/p27/bin

     Installed /root/.pyenv/versions/2.7.13/envs/p27/lib/python2.7/site-packages/hydratk_client-0.1.0-py2.7.egg
     Processing dependencies for hydratk-client==0.1.0
     Searching for jedi==0.10.2
     Best match: jedi 0.10.2
     Processing jedi-0.10.2-py2.7.egg
     jedi 0.10.2 is already the active version in easy-install.pth

     Using /root/.pyenv/versions/2.7.13/envs/p27/lib/python2.7/site-packages/jedi-0.10.2-py2.7.egg
     Searching for PyYAML==3.12
     Best match: PyYAML 3.12
     Processing PyYAML-3.12-py2.7-linux-x86_64.egg
     PyYAML 3.12 is already the active version in easy-install.pth

     Using /root/.pyenv/versions/2.7.13/envs/p27/lib/python2.7/site-packages/PyYAML-3.12-py2.7-linux-x86_64.egg
     Finished processing dependencies for hydratk-client==0.1.0
  
Application installs following (paths depend on your OS configuration)

* htkclient command in /usr/local/bin/htkclient (htkclient.exe in Windows)
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-client-0.1.0-py2.7.egg
* configuration file in /etc/hydratk/hydratk-client.conf
* log directory in /var/local/hydratk/client/log   
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-client module is installed.   

  .. code-block:: bash
  
     $ pip list | grep hydratk-client
     
     hydratk-client (0.1.0)
     
Type command htkclient and application is started.