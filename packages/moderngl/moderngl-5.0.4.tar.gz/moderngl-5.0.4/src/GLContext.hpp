#pragma once

#include "Python.hpp"

#if defined(_WIN32) || defined(_WIN64)

struct GLContext {
	void * hwnd;
	void * hrc;
	void * hdc;
	bool standalone;
};

#elif defined(__APPLE__)

struct GLContext {
	void * context;
	bool standalone;
};

#else

struct GLContext {
	void * display;
	void * window;
	void * context;
	void * buffer;
	bool standalone;
};

#endif

GLContext LoadCurrentGLContext();
GLContext CreateGLContext(PyObject * settings);
void DestroyGLContext(const GLContext & context);
