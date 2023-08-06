``fsleyes-props``
=================

.. toctree::
   :hidden:

   self
   fsleyes_props
   changelog


``fsleyes-props`` is a library which allows you to:

  - Listen for change to attributes on a python object,

  - Automatically generate ``wxpython`` widgets which are bound
    to attributes of a python object

  - Automatically generate a command line interface to set
    values of the attributes of a python object.


To do this, you just need to subclass the :class:`.HasProperties` class,
and add some :class:`.PropertyBase` types as class attributes.


The ``fsleyes-props`` package uses `python descriptors
<http://nbviewer.ipython.org/gist/ChrisBeaumont/5758381/descriptor_writeup.ipynb>`_
to implement an event programming framework. It also includes the ability for
automatic CLI generation and, optionally, automatic GUI generation (if
`wxPython <http://www.wxpython.org>`_ is present).

The more important parts of this documentation are as follows:

 - The :mod:`fsleyes_props` package, for a quick overview.

 - The :mod:`.properties_types` module for details of available property types.

 - The :mod:`.build` module for details on GUI specification and generation.

 - The :mod:`.cli` module for details on CLI specification and generation.

 - The :mod:`.widgets` module for creating widgets linked to properties.

 - The :mod:`.bindable` and :mod:`.syncable` modules for details on binding
   properties between instances, and building hierarchical relationships between
   instances.

 - The :mod:`.properties` and :mod:`.properties_value` modules for details on
   how ``fsleyes-props`` works.
