============================
roslibpy: ROS Bridge library
============================



**Python ROS Bridge library** allows to use Python to interact with `ROS <http://www.ros.org>`_,
the open-source robotic middleware. It uses WebSockets to connect to
`rosbridge 2.0 <http://wiki.ros.org/rosbridge_suite>`_ and provides publishing,
subscribing, service calls, actionlib, TF, and other essential ROS functionality.

Unlike the `rospy <http://wiki.ros.org/rospy>`_ library, this does not require a
local ROS environment, allowing usage from platforms other than Linux.

The API of **roslibpy** is modeled to closely match that of `roslibjs <http://wiki.ros.org/roslibjs>`_.


Main features
-------------

* Topic publishing and subscribing.
* Service calls (client).
* Service advertisement (server).
* ROS parameter management (get/set/delete).
* ROS API services for getting ROS meta-information.
* Actionlib support for interfacing with preemptable tasks.
* TF Client via the ``tf2_web_republisher``.

**Roslibpy** runs on Python 2.7 and 3.x.


Installation
------------

To install **roslibpy**, simply use ``pip``::

    pip install roslibpy

Remember that you will need a working ROS setup including the
**rosbridge server** and **TF2 web republisher** accessible within your network.


Documentation
-------------

The full documentation, including examples and API reference
is available on `readthedocs <https://roslibpy.readthedocs.io/>`_.


Contributing
------------

Make sure you setup your local development environment correctly:

* Clone the `roslibpy <https://github.com/gramaziokohler/roslibpy>`_ repository.
* Create a virtual environment.
* Install development dependencies:

::

    pip install -r requirements-dev.txt

**You're ready to start coding!**

During development, use `pyinvoke <http://docs.pyinvoke.org/>`_ tasks on the
command line to ease recurring operations:

* ``invoke clean``: Clean all generated artifacts.
* ``invoke check``: Run various code and documentation style checks.
* ``invoke docs``: Generate documentation.
* ``invoke test``: Run all tests and checks in one swift command.
* ``invoke``: Show available tasks.

For more details, check the *Contributor's Guide* available as part of `the documentation <https://roslibpy.readthedocs.io/>`_.


Releasing this project
----------------------

Ready to release a new version **roslibpy**? Here's how to do it:

* We use `semver <http://semver.org/>`_, i.e. we bump versions as follows:

  * ``patch``: bugfixes.
  * ``minor``: backwards-compatible features added.
  * ``major``: backwards-incompatible changes.

* Update the ``CHANGELOG.rst`` with all novelty!
* Ready? Release everything in one command:

::

    invoke release [patch|minor|major]

* Profit!


Changelog
=========

0.1.1
-------

* Minimal documentation fixes

0.1.0
-------

* Initial version


