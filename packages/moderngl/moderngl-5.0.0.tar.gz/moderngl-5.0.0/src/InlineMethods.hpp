#pragma once

inline void clean_glsl_name(char * name, int & name_len) {
	if (name_len && name[name_len - 1] == ']') {
		name_len -= 1;
		while (name_len && name[name_len] != '[') {
			name_len -= 1;
		}
	}
	name[name_len] = 0;
}

inline int swizzle_from_char(char c) {
	switch (c) {
		case 'R':
		case 'r':
			return GL_RED;

		case 'G':
		case 'g':
			return GL_GREEN;

		case 'B':
		case 'b':
			return GL_BLUE;

		case 'A':
		case 'a':
			return GL_ALPHA;

		case '0':
			return GL_ZERO;

		case '1':
			return GL_ONE;
	}

	return -1;
}

inline char char_from_swizzle(int c) {
	switch (c) {
		case GL_RED:
			return 'R';

		case GL_GREEN:
			return 'G';

		case GL_BLUE:
			return 'B';

		case GL_ALPHA:
			return 'A';

		case GL_ZERO:
			return '0';

		case GL_ONE:
			return '1';
	}

	return '?';
}

inline int compare_func_from_string(const char * str) {
	if (!str[0] || (str[1] && str[2])) {
		return 0;
	}

	switch (str[0] * 255 + str[1]) {
		case ('<' * 256 + '='):
			return GL_LEQUAL;

		case ('<' * 256):
			return GL_LESS;

		case ('>' * 256 + '='):
			return GL_GEQUAL;

		case ('>' * 256):
			return GL_GREATER;

		case ('=' * 256 + '='):
			return GL_EQUAL;

		case ('!' * 256 + '='):
			return GL_NOTEQUAL;

		case ('0' * 256):
			return GL_NEVER;

		case ('1' * 256):
			return GL_ALWAYS;

		default:
			return 0;
	}
}

inline PyObject * compare_func_to_string(int func) {
	switch (func) {
		case GL_LEQUAL:
			static PyObject * lequal = PyUnicode_FromString("<=");
			return lequal;

		case GL_LESS:
			static PyObject * less = PyUnicode_FromString("<");
			return less;

		case GL_GEQUAL:
			static PyObject * gequal = PyUnicode_FromString(">=");
			return gequal;

		case GL_GREATER:
			static PyObject * greater = PyUnicode_FromString(">");
			return greater;

		case GL_EQUAL:
			static PyObject * equal = PyUnicode_FromString("==");
			return equal;

		case GL_NOTEQUAL:
			static PyObject * notequal = PyUnicode_FromString("!=");
			return notequal;

		case GL_NEVER:
			static PyObject * never = PyUnicode_FromString("0");
			return never;

		case GL_ALWAYS:
			static PyObject * always = PyUnicode_FromString("1");
			return always;

		default:
			static PyObject * unk = PyUnicode_FromString("?");
			return unk;
	}
}

inline PyObject * tuple2(PyObject * a, PyObject * b) {
	PyObject * res = PyTuple_New(2);
	PyTuple_SET_ITEM(res, 0, a);
	PyTuple_SET_ITEM(res, 1, b);
	return res;
}

inline PyObject * tuple3(PyObject * a, PyObject * b, PyObject * c) {
	PyObject * res = PyTuple_New(3);
	PyTuple_SET_ITEM(res, 0, a);
	PyTuple_SET_ITEM(res, 1, b);
	PyTuple_SET_ITEM(res, 2, c);
	return res;
}
