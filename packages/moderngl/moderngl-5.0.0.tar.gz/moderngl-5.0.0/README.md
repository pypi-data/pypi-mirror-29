# ModernGL

- [Documentation](https://moderngl.readthedocs.io/)

## Backward compatibility

Install ModernGL 4.x

```
pip install ModernGL<5.0.0
```

---

[![docs](https://readthedocs.org/projects/moderngl/badge/?version=stable)](https://moderngl.readthedocs.io/)
[![build](https://img.shields.io/travis/cprogrammer1994/ModernGL/master.svg?label=build)](https://travis-ci.org/cprogrammer1994/ModernGL)
[![build](https://img.shields.io/appveyor/ci/cprogrammer1994/ModernGL/master.svg?label=build)](https://ci.appveyor.com/project/cprogrammer1994/ModernGL)
[![health](https://landscape.io/github/cprogrammer1994/ModernGL/master/landscape.svg?style=flat)](https://landscape.io/github/cprogrammer1994/ModernGL/master)
[![pypi](https://img.shields.io/pypi/v/ModernGL.svg)](https://pypi.python.org/pypi/ModernGL/)
[![license](https://img.shields.io/github/license/cprogrammer1994/ModernGL.svg)](https://github.com/cprogrammer1994/ModernGL/blob/master/LICENSE)
[![platforms](https://img.shields.io/badge/platforms-windows%2C%20mac%2C%20linux-blue.svg)](https://pypi.python.org/pypi/ModernGL/)

## Pythonic OpenGL and GLSL support

- [ModernGL on PyPI](https://pypi.python.org/pypi/ModernGL/)
- [Documentation](https://moderngl.readthedocs.io/)
- [Examples](https://github.com/cprogrammer1994/ModernGL/tree/master/examples)
- [Changelog](https://github.com/cprogrammer1994/ModernGL/blob/master/CHANGELOG.md)

## Installation

```sh
pip install ModernGL
```

<!-- ![sample](https://github.com/cprogrammer1994/ModernGL/raw/master/docs/Examples/images/sample.gif) -->

## Description

### Why ModernGL?

If you prefer **GPU accelerated high quality graphics** then you should develop your applications using ModernGL.
It is much simpler than PyOpenGL and capable of rendering with the same quality and performace.

- Full linting support - (using [vscode] and [pylint])
- Create GLSL shaders with only a few lines of code
- Create framebuffers and validate them with a single call
- Access cool OpenGL features by writing clean and self-explaining code
- [vscode snippets] for fast prototyping
- Render to pillow image - (no window required)

[vscode]: https://code.visualstudio.com/
[vscode snippets]: https://github.com/cprogrammer1994/ModernGL/blob/master/extras/vscode/snippets/python.json
[pylint]: https://www.pylint.org/

### Why is it simpler?

With the original OpenGL API you have to write a couple of lines to achieve a **simple task** like compiling a shader or running a computation on the GPU. With ModernGL you will need just a **few lines** to achieve the same result.

#### Using PyOpenGL

```py
vbo1 = glGenBuffers(1)
GL.glBindBuffer(GL_ARRAY_BUFFER, vbo1)
GL.glBufferData(GL_ARRAY_BUFFER, b'Hello World!', GL_STATIC_DRAW)

vbo2 = glGenBuffers(1)
GL.glBindBuffer(GL_ARRAY_BUFFER, vbo2)
GL.glBufferData(GL_ARRAY_BUFFER, b'\x00' * 1024, GL_DYNAMIC_DRAW)
```

#### Using ModernGL

```py
vbo1 = ctx.buffer(b'Hello World!')
vbo2 = ctx.buffer(reserve=1024, dynamic=True)
```

#### Some cool features

```py
# Read the content
>>> vbo1.read()
b'Hello World!'

# Copy between buffers
>>> ctx.copy_buffer(vbo2, vbo1)

>>> vbo2.read(5)
b'Hello'

# Buffer re-specification
>>> vbo2.orphan()
>>> vbo2.write(b'Some other data')
```

### Is ModernGL faster than PyOpenGL?

In some cases **yes**, the core functions of ModernGL are written in C++, OpenGL functions are called in quick succession so these calls together count as a single python function call.

### What version of OpenGL is used?

Most of the calls only require **OpenGL 3.3** but Subroutines and Compute Shaders require **OpenGL 4.0** and **OpenGL 4.3**

### Is my old PC supported?

OpenGL 3.3 came out in February 2010. With **up to date drivers** you will be able to use the most of the ModernGL functions, even on integrated graphics cards. _(No, Compute Shaders won't work)_

### Render to pillow image

```py
size = (256, 256)
fbo = ctx.framebuffer(ctx.renderbuffer(size))
fbo.use()

# Render scene

Image.frombytes('RGB', size, fbo.read(components=3))
```

### Render to pillow image (multisample)

```py
size = (256, 256)
fbo1 = ctx.framebuffer(ctx.renderbuffer(size, samples=8))
fbo2 = ctx.framebuffer(ctx.renderbuffer(size))
fbo1.use()

# Render scene

ctx.copy_framebuffer(fbo2, fbo1)
Image.frombytes('RGB', size, fbo1.read(components=3))
```

## Render to pillow image (larger than screen)

Just change the size to `(4096, 4096)`<br>

> This will require much more video ram.

## Working with uniforms and attributes

```py
# The declaration of the program is omitted.

>>> prog.uniforms
{
    'Matrix': <Uniform: 0>,
    'Lights': <Uniform: 1>,
    'Color': <Uniform: 2>,
}

>>> prog.uniforms['Lights'].value
[(0.0, 0.0, 100.0), [(10.0, 10.0, 90.0)]

>>> prog.attributes
{
    'vertex': <Attribute: 0>,
    'normal': <Attribute: 1>,
    'texcoord': <Attribute: 2>,
}

>>> ctx.detect_format(prog, ['vertex', 'normal'])
'4f3f'

>>> color_uniform = prog.uniforms['Color']
>>> color_uniform.value = (0.0, 1.0, 0.0)
```

> Don't read uniform values too often they force some GPUs to sync.

### How can I start using ModernGL?

Take a look at the [examples] and [docs].

[examples]: https://github.com/cprogrammer1994/ModernGL/tree/master/examples
[docs]: https://moderngl.readthedocs.io/

### Where can I use ModernGL?

**Anywhere where OpenGL is supported.** ModernGL is capable of rendering using a [standalone_context] as well. Rendering to a window only requires a valid OpenGL context.

[standalone_context]: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/standalone

### Can ModernGL create a Window?

**NO**, Window creation is up to you. You can choose from a large variety of modules that can create a window: [PyQt5], [pyglet], [pygame], [GLUT] and many others.

[PyQt5]: https://pypi.python.org/pypi/PyQt5/
[pyglet]: https://bitbucket.org/pyglet/pyglet/wiki/Home
[pygame]: https://www.pygame.org/news
[GLUT]: https://wiki.python.org/moin/PyOpenGL

### Limitations using ModernGL over PyOpenGL?

All the neccessary calls are (or can be) implemented in ModernGL. However you can interract with the ModernGL objects from PyOpenGL. If something is missing write an [issue](https://github.com/cprogrammer1994/ModernGL/issues) or raise a [PR](https://github.com/cprogrammer1994/ModernGL/pulls).

## Supported platforms

- [x] Windows
- [x] Linux
- [x] Mac

## Installing from source

### Installing on Ubuntu from source

```sh
apt-get install python3-dev libgl1-mesa-dev libx11-dev
python3 setup.py install
```

### Building the sphinx documentation

```sh
pip install -r docs/requirements.txt
python setup.py build_sphinx
```

### Running tests

```sh
pytest
```

> Some of the tests may be skipped when the supported OpenGL version is below the requirements of the given test.

### Headless rendering

```sh
apt-get install xvfb
alias xpy='xvfb-run -s "-screen 0 1x1x24" python3'
xpy -m ModernGL
```

## Code quality

Code is tested with [pep8], [flake8], [prospector] and [pylint]

[pep8]: https://www.python.org/dev/peps/pep-0008/
[flake8]: http://flake8.pycqa.org/en/latest/
[prospector]: https://prospector.landscape.io/en/master/
[pylint]: https://www.pylint.org/

## Community

- [Code of conduct](https://github.com/cprogrammer1994/ModernGL/blob/master/.github/CODE_OF_CONDUCT.md)

## Contributors

- [Szabolcs Dombi](https://github.com/cprogrammer1994)
- [SimLeek](https://github.com/SimLeek)
- [Aljenci](https://github.com/Aljenci)
- [MinchinWeb](https://github.com/MinchinWeb)
- [Silexstudio](https://github.com/Silexstudio)
- [stuaxo](https://github.com/stuaxo)
- [Tomi Aarnio](https://github.com/toaarnio)

and [many others](https://github.com/cprogrammer1994/ModernGL/graphs/contributors)

Thank You!

Contributions are welcome. _(Please add yourself to the list)_
