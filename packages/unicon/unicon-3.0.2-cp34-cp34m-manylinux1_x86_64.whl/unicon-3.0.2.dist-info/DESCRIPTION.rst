Unicon - Universal Connection Library
=====================================

Unicon is a framework for developing device control 
libraries for routers, switches and servers and the likes. It is developed 
purely in Python, and aims to reduce the amount of boiler-plate coding required
to handle device connections in Expect-like progamming. Unicon is designed to 
integrate as the default device connection class in `Cisco pyATS`_, and as well
can be used stand-alone if required.

Unicon is initially developed internally in Cisco, and is now available to the
general public starting late 2017 through `Cisco DevNet`_. 


.. _Cisco DevNet: https://developer.cisco.com/
.. _Cisco pyATS: https://developer.cisco.com/site/pyats/

As a framework, Unicon provides a set of classes and settings which can be
further sub-classed to create platform specific implementations.

One of the main design goals of unicon is `DRY` (Do Not Repeat Yourself).
Hence the base classes handle all the common stuff which are applicable to all
the platforms. This makes it very easy for a developer to implement connection
library (via plugins) for new platforms, as they only ends up writing the 
differential code.


Requirements
------------

Unicon currently supports Python 3.4+ on Linux & Mac systems. Windows platforms
are not yet supported.

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade unicon


For more information on setting up your Python development environment,
such as creating virtual environment and installing ``pip`` on your system, 
please refer to `Virtual Environment and Packages`_ in Python tutorials.

.. _Virtual Environment and Packages: https://docs.python.org/3/tutorial/venv.html

Examples
--------

See example of a Unicon connection usag with Cisco IOS devices at:

    https://github.com/CiscoDevNet/pyats-ios-sample

In addition, there is a sample plugin package you can follow to develop Unicon
plugins for new platforms on top of Unicon:

    https://github.com/CiscoDevNet/pyats-plugin-examples/tree/master/unicon_plugin_example

Support
-------

Join us at our DevNet community for support:

    https://communities.cisco.com/community/developer/pyats

