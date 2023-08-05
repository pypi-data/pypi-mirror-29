VertexArray
===========

.. py:module:: moderngl
.. py:currentmodule:: moderngl

.. autoclass:: moderngl.VertexArray

    .. note::
        Compared to OpenGL, :py:class:`VertexArray` objects have some additional responsibilities:

        - Binding a :py:class:`Program` when :py:meth:`VertexArray.render` or :py:meth:`VertexArray.transform` is called.
        - Subroutines can be assigned. Please see the example below.

Create
------

.. automethod:: Context.simple_vertex_array(program, buffer, *attributes, index_buffer=None) -> VertexArray
    :noindex:

.. automethod:: Context.vertex_array(program, content, index_buffer=None) -> VertexArray
    :noindex:

Methods
-------

.. automethod:: VertexArray.render(mode=None, vertices=-1, first=0, instances=1)
.. automethod:: VertexArray.transform(buffer, mode=None, vertices=-1, first=0, instances=1)
.. automethod:: VertexArray.bind(attribute, cls, buffer, fmt, offset=0, stride=0, divisor=0, normalize=False)

Attributes
----------

.. autoattribute:: VertexArray.program
.. autoattribute:: VertexArray.index_buffer
.. autoattribute:: VertexArray.vertices
.. autoattribute:: VertexArray.subroutines
.. autoattribute:: VertexArray.glo

.. toctree::
    :maxdepth: 2
