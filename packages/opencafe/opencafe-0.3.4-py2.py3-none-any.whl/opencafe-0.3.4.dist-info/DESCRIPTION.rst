#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Description: OpenCafe
        ========
        
        .. image:: https://img.shields.io/pypi/v/opencafe.svg
            :target: https://pypi.python.org/pypi/opencafe
        
        .. image:: https://travis-ci.org/CafeHub/opencafe.svg?branch=master
            :target: https://travis-ci.org/CafeHub/opencafe
        
        When writing automated test sutes, there are some things that should
        "just work". Problems like managing test data, logging, and results are
        things that shouldn't have to be re-invented for every test project you work
        on. OpenCafe aims to address that problem by providing solutions for the
        commonly occuring challenges in the development and operation of functional
        and end-to-end test suites.
        
        Capabilities
        ------------
        
        - Common sense conventions for test data and log management
        - Per test run and per test logs and results
        - Reference drivers for performing non-UI testing including HTTP, SSH,
          and WinRM
        - Design patterns for building test clients for RESTful API applications
        - Plugin system to allow for further customization
        
        Installation
        ============
        
        CoreÂ package
        ------------
        
        FromÂ PyPIÂ (recommended):
        
        ::
        
            $ pip install opencafe
        
        FromÂ source:
        
        ::
        
            $ git clone https://github.com/CafeHub/opencafe.git
            $ cd opencafe
            $ pip install .
        
        Post-install Configuration
        --------------------------
        
        Post-install, the ``cafe-config`` cli tool will become available. It is used
        for installing plugins and initializing OpenCafe's default directory
        structure.
        
        Initialization
        ^^^^^^^^^^^^^^
        Running the ``cafe-config init`` command will create the default OpenCafe
        directory structure in a directory named ``.opencafe``. This directory will
        be located in either the current user's home directory or in the root of the
        virtual environment you currently have active. This directory contains the
        ``/configs`` directory which stores configuration data, the ``/logs``
        directory which holds the logging output from all tests executed, and the
        ``engine.config`` file, which sets the base test repository and allows the
        user to override the default directories for logging and configuration.
        
        Plugins
        ^^^^^^^
        
        OpenCafeÂ usesÂ aÂ pluginÂ systemÂ toÂ allowÂ forÂ coreÂ functionalityÂ toÂ be extended
        orÂ forÂ additionalÂ capabilitiesÂ toÂ beÂ added.Â PluginsÂ are essentiallyÂ Python
        packages,Â whichÂ mayÂ haveÂ theirÂ ownÂ PythonÂ dependencies. ThisÂ designÂ allows
        implementorsÂ toÂ onlyÂ installÂ dependenciesÂ forÂ the functionalityÂ thatÂ they
        intendÂ toÂ use,Â asÂ theÂ additionalÂ dependencies areÂ installedÂ atÂ theÂ sameÂ time
        asÂ theÂ plugin.
        
        The ``cafe-config plugins`` command is used to list and install plugins.
        
        Example:
        
        ::
        
            $ cafe-config plugins list
            =================================
            * Available Plugins
              ... elasticsearch
              ... http
              ... mongo
              ... pathos_multiprocess
              ... rsyslog
              ... skip_on_issue
              ... soap
              ... ssh
              ... sshv2
              ... subunit
              ... winrm
            =================================
        
            $ cafe-config plugins install http
            =================================
            * Installing Plugins
              ... http
            =================================
        
        Documentation
        -------------
        
        MoreÂ in-depthÂ documentation about the OpenCafe frameworkÂ isÂ locatedÂ at
        http://opencafe.readthedocs.org.
        
        HowÂ toÂ Contribute
        -----------------
        
        ContributionsÂ areÂ alwaysÂ welcome.Â TheÂ CONTIBUTING.mdÂ fileÂ containsÂ further
        guidanceÂ onÂ submittingÂ changesÂ toÂ thisÂ projectÂ andÂ theÂ reviewÂ processÂ that
        weÂ follow.
        
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: License :: Other/Proprietary License
Classifier: Operating System :: POSIX :: Linux
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2.7
