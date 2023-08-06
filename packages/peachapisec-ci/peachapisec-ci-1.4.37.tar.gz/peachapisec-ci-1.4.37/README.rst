Peach CI Generic Integration Runner
===================================

This module provides generic integration with CI systems by running a
command that returns non-zero when testing did not pass.
The vast majority of CI systems support this method of integration.

If a specific integration is offered for your CI system that is
preferred over this generic integration.

To use, update the configuration at top of python file and
configure your CI system to run.

See User Guide -> CI Integration for additional information
about using and configuring the generic CI integration runner.

Installation
------------

Install required python dependencies with internet connection.

$ pip install -r requirements.txt

Offline Installation
--------------------

Install required python dependencies using our offline dependencies
folder.

$ pip install --no-index --find-links ../../deps -r requirements.txt
