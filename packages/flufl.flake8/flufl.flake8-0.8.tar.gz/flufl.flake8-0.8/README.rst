==============
 flufl.flake8
==============

This is a plugin for flake8_ which checks for my particular import style.  It
was previously part of `flufl.testing`_ but as `nose2`_ becomes much less
popular than pytest_, it makes more sense to provide the flake8 plugin as a
separate package.

Python 3.4 is the minimum supported version.


flake8 import order plugin
==========================

This flake8_ plugin enables import order checks as are used in the `GNU
Mailman`_ project.  Specifically, it enforces the following rules:

* Non-``from`` imports must precede ``from``-imports.
* Exactly one line must separate the block of non-``from`` imports from the
  block of ``from`` imports.
* Import exactly one module per non-``from`` import line.
* Lines in the non-``from`` import block are sorted by length first, then
  alphabetically.  Dotted imports count toward both restrictions.
* Lines in the ``from`` import block are sorted alphabetically.
* Multiple names can be imported in a ``from`` import line, but those names
  must be sorted alphabetically.
* Names imported from the same module in a ``from`` import must appear in the
  same import statement.

It's so much easier to see an example::

    import copy
    import socket
    import logging
    import smtplib

    from mailman import public
    from mailman.config import config
    from mailman.interfaces.mta import IMailTransportAgentDelivery
    from mailman.mta.connection import Connection
    from zope.interface import implementer

To enable this plugin [#]_, add the following to your ``tox.ini`` or any other
`flake8 recognized configuration file`_::

    [testenv]
    deps = flufl.flake8

    [flake8]
    enable-extensions = U4


Author
======

``flufl.flake8`` is Copyright (C) 2013-2018 Barry Warsaw <barry@python.org>

Licensed under the terms of the Apache License, Version 2.0.


Project details
===============

 * Project home: https://gitlab.com/warsaw/flufl.flake8
 * Report bugs at: https://gitlab.com/warsaw/flufl.flake8/issues
 * Code hosting: https://gitlab.com/warsaw/flufl.flake8.git
 * Documentation: https://gitlab.com/warsaw/flufl.flake8/tree/master


Footnotes
=========

.. [#] Note that flake8 3.1 or newer is required.


.. _flake8: http://flake8.pycqa.org/en/latest/index.html
.. _`GNU Mailman`: http://www.list.org
.. _`flake8 recognized configuration file`: http://flake8.pycqa.org/en/latest/user/configuration.html
.. _`nose2`: http://nose2.readthedocs.io/en/latest/index.html
.. _`flufl.testing`: https://gitlab.com/warsaw/flufl.testing/tree/master
.. _pytest: https://docs.pytest.org/en/latest/
