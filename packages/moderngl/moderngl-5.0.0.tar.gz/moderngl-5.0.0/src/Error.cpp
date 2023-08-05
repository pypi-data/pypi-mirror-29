#include "Types.hpp"

#include <cstdarg>

PyObject * MGLError_TypePtr;

struct MGLError {
	PyException_HEAD
};

void MGLError_Init(MGLError * error) {
	error->dict = 0;
	error->args = 0;
	error->traceback = 0;
	error->context = 0;
	error->cause = 0;
	error->suppress_context = 0;
}

void MGLError_SetTrace(const char * filename, const char * function, int line, const char * format, ...) {
	va_list va_args;
	va_start(va_args, format);
	PyObject * message = PyUnicode_FromFormatV(format, va_args);
	va_end(va_args);

	MGLError_SetTrace(filename, function, line, message);
}

void MGLError_SetTrace(const char * filename, const char * function, int line, PyObject * message) {
	PyObject * attr_args = PyTuple_New(1);
	PyTuple_SET_ITEM(attr_args, 0, message);

	PyObject * attr_filename = PyUnicode_FromString(filename + 4);
	PyObject * attr_function = PyUnicode_FromString(function);
	PyObject * attr_line = PyLong_FromLong(line);

	PyObject * error = _PyObject_New((PyTypeObject *)MGLError_TypePtr);
	MGLError_Init((MGLError *)error);

	PyObject_SetAttrString((PyObject *)error, "args", attr_args);
	PyObject_SetAttrString((PyObject *)error, "filename", attr_filename);
	PyObject_SetAttrString((PyObject *)error, "function", attr_function);
	PyObject_SetAttrString((PyObject *)error, "line", attr_line);
	PyErr_SetObject(MGLError_TypePtr, (PyObject *)error);

	Py_DECREF(attr_args);
	Py_DECREF(attr_filename);
	Py_DECREF(attr_function);
	Py_DECREF(attr_line);
}
