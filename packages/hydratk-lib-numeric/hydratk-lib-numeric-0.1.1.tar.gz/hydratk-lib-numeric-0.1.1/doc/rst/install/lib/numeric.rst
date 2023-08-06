.. install_lib_numeric:

Numeric
=======

You have 2 options how to install Numeric library.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk-lib-numeric
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-lib-numeric
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.
     
  .. Use PIP option --install-option="--profile=p1,p2" to install only Python dependent modules included
     in requested profiles. Offered profiles are basic, math. Full profile is installed by default.   
     Not supported for easy_install because it doesn't provide custom options.   

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-lib-numeric.git
     $ cd ./hydratk-lib-numeric
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://pypi.python.org/pypi/hydratk-lib-numeric -O hydratk-lib-numeric.tar.gz
     $ tar -xf hydratk-lib-numeric.tar.gz
     $ cd ./hydratk-lib-numeric
     $ sudo python setup.py install
     
  .. Use option --profile=p1,p2 to install only Python dependent modules included
     in requested profiles. Offered profiles are basic, math. Full profile is installed by default.        
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.     
     
Requirements
^^^^^^^^^^^^

Several python modules are used.
These modules will be installed automatically, if not installed yet.

* hydratk
* matplotlib
* numpy
* scipy
* sympy

Module matplotlib requires library which will be installed via Linux package managers, if not installed yet.

  .. note ::
     
     Installation for Python2.6 and 3.3 is not supported due to key module numpy.
     
  .. note ::
  
     Installation for PyPy has some differences.
     Modules matplotlib, scipy are not supported and installed.      

Library offers following profiles.

* basic - hydratk, numpy
* math - basic profile, matplotlib, scipy, sympy
* full - everything
    
Installation
^^^^^^^^^^^^

See installation example for Linux based on Debian distribution, Python 2.7. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************
     
     *** Running task: version_update ***
     
     *** Running task: install_modules ***
     Module hydratk already installed with version 0.5.0rc1
     Installing module numpy>=1.12.1
     pip install "numpy>=1.12.1"
     Installing module sympy>=1.0
     pip install "sympy>=1.0"
     Installing module matplotlib>=2.0.0
     pip install "matplotlib>=2.0.0"
     Installing module scipy>=0.19.0
     pip install "scipy>=0.19.0"
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_lib_numeric.egg-info
     writing src/hydratk_lib_numeric.egg-info/PKG-INFO
     writing top-level names to src/hydratk_lib_numeric.egg-info/top_level.txt
     writing dependency_links to src/hydratk_lib_numeric.egg-info/dependency_links.txt
     writing manifest file 'src/hydratk_lib_numeric.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_lib_numeric.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_lib_numeric.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     ...
     creating dist
     creating 'dist/hydratk_lib_numeric-0.1.0rc1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_lib_numeric-0.1.0rc1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_lib_numeric-0.1.0rc1-py2.7.egg
     Extracting hydratk_lib_numeric-0.1.0rc1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-lib-numeric 0.1.0rc1 to easy-install.pth file
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_lib_numeric-0.1.0rc1-py2.7.egg
     Processing dependencies for hydratk-lib-numeric==0.1.0rc1
     Finished processing dependencies for hydratk-lib-numeric==0.1.0rc1
                
        
Run
^^^

When installation is finished you can run the application.

Check hydratk-lib-numeric module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk-lib-numeric

     hydratk-lib-numeric (0.1.0)    
     
Upgrade
^^^^^^^

Use same procedure as for installation. Use command option --upgrade for pip, easy_install, --force for setup.py.

Uninstall
^^^^^^^^^

Run command htkuninstall. Use option -y if you want to uninstall also dependent Python modules (for advanced user).             