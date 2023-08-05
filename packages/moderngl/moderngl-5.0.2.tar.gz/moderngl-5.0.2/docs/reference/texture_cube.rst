TextureCube
===========

.. py:module:: moderngl
.. py:currentmodule:: moderngl

.. autoclass:: moderngl.TextureCube

Create
------

.. automethod:: Context.texture_cube(size, components, data=None, alignment=1, dtype='f1') -> TextureCube
    :noindex:

Methods
-------

.. automethod:: TextureCube.read(face, alignment=1) -> bytes
.. automethod:: TextureCube.read_into(buffer, face, alignment=1, write_offset=0)
.. automethod:: TextureCube.write(face, data, viewport=None, alignment=1)
.. automethod:: TextureCube.use(location=0)

Attributes
----------

.. autoattribute:: TextureCube.glo

.. toctree::
    :maxdepth: 2
