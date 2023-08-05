|Build Status| |Code Health| |Pyup Updates| |Pyup Py3|

Pyros-msgs
==========

Package enabling ROS communication for other Pyros multiprocess
systems.

Features
--------

ROS
~~~

-  optional field as a ROS array
-  optional field indicated by a specific message type

.. |Build Status| image:: https://travis-ci.org/pyros-dev/pyros-msgs.svg?branch=master
   :target: https://travis-ci.org/pyros-dev/pyros-msgs
   :alt: Build Status

.. |Code Health| image:: https://landscape.io/github/pyros-dev/pyros-msgs/master/landscape.svg?style=flat
   :target: https://landscape.io/github/pyros-dev/pyros-msgs/master
   :alt: Code Health

.. |Pyup Updates| image:: https://pyup.io/repos/github/pyros-dev/pyros-msgs/shield.svg
   :target: https://pyup.io/repos/github/pyros-dev/pyros-msgs/
   :alt: Updates

.. |Pyup Py3| image:: https://pyup.io/repos/github/pyros-dev/pyros-msgs/python-3-shield.svg
   :target: https://pyup.io/repos/github/pyros-dev/pyros-msgs/
   :alt: Python 3

Testing
-------

1) make sure you have downloaded the submodules (ros message definitions)
2) check `tox -l` to list the test environments
3) choose the tests matching your platform and run them

The tests are also run on travis, so any pull request need to have tests failing at first ( create test to illustrate the problem if needed).
Then add commits to fix the broken tests, and all must pass before merging.
