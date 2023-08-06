Differneces between ModernGL5 and ModernGL4
===========================================

.. py:module:: moderngl
.. py:currentmodule:: moderngl

Package Name
------------

.. rubric:: ModernGL4

.. code-block:: python

    import ModernGL  # mixed case

.. rubric:: ModernGL5

.. code-block:: python

    import moderngl  # this is pep8 style

|
|
|

Program Creation
----------------

.. rubric:: ModernGL4

.. code-block:: python

    my_program = ctx.program([  # extra list
        # vertex_shader returned a Shader object
        ctx.vertex_shader('''
            ...
        '''),
        # fragment_shader returned a Shader object
        ctx.fragment_shader('''
            ...
        '''),
    ])

.. rubric:: ModernGL5

.. code-block:: python

    my_program = ctx.program(  # no list needed
        # vertex_shader is a keyword argument
        vertex_shader='''
            ...
        ''',
        # fragment_shader is a keyword argument
        fragment_shader='''
            ...
        ''',
    )

|
|
|

Program Varyings
----------------

.. rubric:: ModernGL4

.. code-block:: python

    my_program = ctx.program(
        ctx.vertex_shader('''
            ...
        '''),
        ['out_vert', 'out_norm']  # no keyword argument needed
    ])

.. rubric:: ModernGL5

.. code-block:: python

    my_program = ctx.program(
        vertex_shader='''
            ...
        ''',
        varyings=['out_vert', 'out_norm'],  # varyings are explicitly given
    )

|
|
|

Program Members
---------------

.. rubric:: ModernGL4

.. code-block:: python

    my_program.uniforms['ModelViewMatrix'].value = ...
    my_program.uniform_buffers['UniformBuffer'].binding = ...

.. rubric:: ModernGL5

.. code-block:: python

    my_program['ModelViewMatrix'].value = ...
    my_program['UniformBuffer'].binding = ...

|
|
|

Texture Pixel Types
-------------------

.. rubric:: ModernGL4

.. code-block:: python

    my_texture = ctx.texture(size, 4, floats=True)  # floats or not floats

.. rubric:: ModernGL5

.. code-block:: python

    my_texture = ctx.texture(size, 4, dtype='f4')  # floats=True
    my_texture = ctx.texture(size, 4, dtype='f2')  # half-floats
    my_texture = ctx.texture(size, 4, dtype='f1')  # floats=False
    my_texture = ctx.texture(size, 4, dtype='i4')  # integers

This also apply for :py:class:`Texture3D`, :py:class:`TextureCube` and :py:class:`Renderbuffer`.

|
|
|

Buffer Format
-------------

.. rubric:: ModernGL4

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f3f', ['in_vert', 'in_norm']),  # extra list object
        #        ^ no space between the attributes
        ...
    ])

.. rubric:: ModernGL5

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f 3f', 'in_vert', 'in_norm'),  # no list needed
        #         ^ space is obligatory
        ...
    ])

|
|
|

Buffer Format Half-Floats
-------------------------

.. rubric:: ModernGL4

Not available in ModernGL4

.. rubric:: ModernGL5

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f2 3f2', 'in_vert', 'in_norm'),  # '3f2' means '3' of 'f2', where 'f2' is a half-float
        ...
    ])

|
|
|

Buffer Format Padding
---------------------

.. rubric:: ModernGL4

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f12x', ['in_vert']),  # same as above, in_norm was replaced with padding
        ...
    ])

.. rubric:: ModernGL5

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f 3x4', ['in_vert']),  # '3x4' means '3' of 'x4', where 'x4' means 4 bytes of padding
        ...
    ])

|
|
|

Buffer Format Errors
--------------------

Let's assume ``in_vert`` was declared as: ``in vec4 in_vert``

.. rubric:: ModernGL4

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f', ['in_vert']),  # throws an error (3 != 4)
        ...
    ])

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '4i', ['in_vert']),  # throws an error (float != int)
        ...
    ])

.. rubric:: ModernGL5

.. code-block:: python

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '3f', 'in_vert'),  # totally fine
        ...
    ])

    my_vertex_array = ctx.vertex_array(prog, [
        (vbo1, '4i', 'in_vert'),  # totally fine
        ...
    ])

|
|
|

.. rubric:: Found something not covered here? Please file an `issue <https://github.com/cprogrammer1994/ModernGL/issues>`_.
