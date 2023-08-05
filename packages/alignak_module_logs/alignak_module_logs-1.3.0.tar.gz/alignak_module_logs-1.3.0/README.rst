Alignak Log Module
==================

*Alignak module for the monitoring logs*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-logs.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-logs
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-logs/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-logs/develop
    :alt: Development code static analysis

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-logs/badge.svg?branch=develop
    :target: https://coveralls.io/r/Alignak-monitoring-contrib/alignak-module-logs
    :alt: Development code tests coverage

.. image:: https://badge.fury.io/py/alignak_module_logs.svg
    :target: https://badge.fury.io/py/alignak-module-logs
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Installation
------------

The installation of this module will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the modules (eg. *arbiter/modules*).

From PyPI
~~~~~~~~~
To install the module from PyPI:
::

   sudo pip install alignak-module-logs


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files (for developing purpose):
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-module-logs
   cd alignak-module-logs
   sudo pip install . -e

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*


Short description
-----------------

This module for Alignak collects the monitoring logs (alerts, notifications, ...) to log them into a dedicated file.

You can plainly use the powerful of the Python logging system thanks to the use of a logging configuration file which will allow you to define when, where and how to send the monitoring logs ....

Known issues
------------
This module is not compatible with Python 2.6 if you intend to use a logger configuration file as this feature is not available before Python 2.7 version.
If you are still using the old 2.6 version, upgrade or define the logger parameters in the module configuration file.

Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-logs.cfg*. This file is commented to help configure all the parameters.

To configure Alignak broker to use this module:

- edit your broker daemon configuration file
- add the `module_alias` parameter value (`logs`) to the `modules` parameter of the daemon

To configure this module to send its log to the Alignak backend:

- edit the module configuration file to set the Alignak backend parameters (eg. url and login information)

To set up several logs collectors:

- copy the default configuration to another file,
- change the module alias parameter (`logs_bis`)
- edit your broker daemon configuration file
- add the new `module_alias` parameter value (`logs_bis`) to the `modules` parameter of the daemon

To set up your own logger:

- edit the module configuration file to uncomment the `logger_configuration` variable
- update the logger configuration file (eg. mod-logs-logger.json) to replace `ALIGNAKLOG` with your target log directory
- update the logger configuration file to suit your needs ... then python logger on the Internet is your best friend :)

Monitoring logs configuration
-----------------------------

As a default configuration this module will create a log file for the monitoring logs. This file will be located in the alignak log directory and it will be rotated every day for a period of 365 days. You can also define your own logging strategy as it is explained in the module configuration file that is largely commented to explain how to configure.

Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-module-logs/issues>`_ are the common way to raise an information.
