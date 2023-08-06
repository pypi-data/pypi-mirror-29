News
====

.. _release3.2:

3.2
---
* Slightly corrected colours, now visible on white background

.. _release3.1:

3.1
---
* Fix bug related to DecodeError showing with DecodePathDefBy entities
* Respect ``NO_COLOR`` environment variable

.. _release3.0:

3.0
---
* :py:func:`pyderasn.decode_path_defby` is replaced with
  :py:class:`pyderasn.DecodePathDefBy`
* Ability to turn colourized terminal output by calling
  ``pprint(..., with_colours=True)``. You will need
  `termcolor package <https://pypi.python.org/pypi/termcolor>`__

.. _release2.1:

2.1
---
* Fixed invalid offset calculation when dealing with DEFINED BY objects
  having explicit tags

.. _release2.0:

2.0
---
* BIT STRINGs can also be :ref:`DEFINED BY <definedby>`
* Decoding process can be governed with optional :ref:`ctx <ctx>`
  keyword argument to ``decode()`` method
* :ref:`defines_by_path <defines_by_path_ctx>` option is now
  :ref:`decode context <ctx>` option, not a keyword argument
* Ability to do :ref:`strict validation <strict_default_existence_ctx>`
  of defaulted values met in sequence, raising an exception

.. _release1.6:

1.6
---
Ability to skip specified number of bytes (``--skip``) in command line
utility.

.. _release1.5:

1.5
---
* Generic decoder's scheme and pretty printer
  (:py:func:`pyderasn.generic_decoder`) can be used in libraries.
* Ability to specify :ref:`defines_by_path <defines_by_path_ctx>`
  during command line invocation.

.. _release1.4:

1.4
---
Ability to automatically decode :ref:`DEFINED BY <definedby>` fields
inside SEQUENCEs.

.. _release1.3:

1.3
---
Removed ``__lt__``/``__eq__`` from base class, as pylint likes it.

.. _release1.2:

1.2
---
Full rich comparison operators added.


.. _release1.1:

1.1
---
Trivial README addition.

.. _release1.0:

1.0
---
Initial release.
