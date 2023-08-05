#include "GLContext.hpp"

#include "Error.hpp"

#if defined(_WIN32) || defined(_WIN64)

// Windows

#include <Windows.h>

#define WGL_ACCELERATION 0x2003
#define WGL_FULL_ACCELERATION 0x2027
#define WGL_CONTEXT_MAJOR_VERSION 0x2091
#define WGL_CONTEXT_MINOR_VERSION 0x2092
#define WGL_CONTEXT_PROFILE_MASK 0x9126
#define WGL_CONTEXT_CORE_PROFILE_BIT 0x0001

typedef int (WINAPI * my_ChoosePixelFormat_type)(HDC hdc, const int * piAttribIList, const float * pfAttribFList, unsigned nMaxFormats, int * piFormats, unsigned * nNumFormats);
typedef HGLRC (WINAPI * my_CreateContextAttribs_type)(HDC hdc, HGLRC hglrc, const int * attribList);

my_ChoosePixelFormat_type my_ChoosePixelFormat;
my_CreateContextAttribs_type my_CreateContextAttribs;

#elif defined(__APPLE__)

// OSX

#include <OpenGL/OpenGL.h>
#include <ApplicationServices/ApplicationServices.h>

#include <OpenGL/gl.h>
#include <OpenGL/glext.h>

#else

// Linux

#include <dlfcn.h>
#include <GL/glx.h>
#include <GL/gl.h>
// #include <X11/Xlib.h>
// #include <X11/X.h>

#define Bool int

typedef unsigned long XID;
typedef struct __GLXFBConfigRec * GLXFBConfig;
typedef struct __GLXcontextRec * GLXContext;
typedef XID Pixmap;
typedef XID Window;

// X11

#define GLX_CONTEXT_MAJOR_VERSION 0x2091
#define GLX_CONTEXT_MINOR_VERSION 0x2092
#define GLX_CONTEXT_PROFILE_MASK 0x9126
#define GLX_CONTEXT_CORE_PROFILE_BIT 0x0001

typedef GLXContext (* GLXCREATECONTEXTATTRIBSARBPROC)(Display * display, GLXFBConfig config, GLXContext context, Bool direct, const int * attribs);

static int SilentXErrorHandler(Display * d, XErrorEvent * e) {
	return 0;
}

typedef Display * (* my_XOpenDisplay_type)(const char * display);
typedef int (* my_XCloseDisplay_type)(Display * display);
typedef int (* my_XDestroyWindow_type)(Display * display, Window window);
typedef Window (* my_XCreateWindow_type)(Display * display, Window window, int x, int y, unsigned int width, unsigned int height, unsigned int border_width, int depth, unsigned int _class, Visual * visual, unsigned long valuemask, XSetWindowAttributes * xsetwindowattributes);
typedef XErrorHandler (* my_XSetErrorHandler_type)(XErrorHandler);
typedef Colormap (* my_XCreateColormap_type)(Display * display, Window window, Visual * visual, int alloc);

my_XOpenDisplay_type my_XOpenDisplay;
my_XCloseDisplay_type my_XCloseDisplay;
my_XDestroyWindow_type my_XDestroyWindow;
my_XCreateWindow_type my_XCreateWindow;
my_XSetErrorHandler_type my_XSetErrorHandler;
my_XCreateColormap_type my_XCreateColormap;

// EGL

typedef Display * EGLNativeDisplayType;
typedef Pixmap EGLNativePixmapType;
typedef Window EGLNativeWindowType;

#define EGL_RED_SIZE 0x3024
#define EGL_GREEN_SIZE 0x3023
#define EGL_BLUE_SIZE 0x3022
#define EGL_NONE 0x3038
#define EGL_BAD_DISPLAY 0x3008
#define EGL_FALSE 0
#define EGL_BAD_MATCH 0x3009
#define EGL_NOT_INITIALIZED 0x3001
#define EGL_BAD_CONFIG 0x3005
#define EGL_BAD_CONTEXT 0x3006
#define EGL_BAD_ATTRIBUTE 0x3004
#define EGL_BAD_ALLOC 0x3003

#define EGL_NO_DISPLAY 0
#define EGL_NO_CONTEXT 0
#define EGL_NO_DISPLAY 0
#define EGL_NO_SURFACE 0

typedef void * EGLDisplay;
typedef void * EGLConfig;
typedef void * EGLSurface;
typedef void * EGLContext;

typedef unsigned int EGLBoolean;
typedef int EGLint;

typedef EGLDisplay (* my_eglGetDisplay_type)(EGLNativeDisplayType display_id);
typedef EGLBoolean (* my_eglInitialize_type)(EGLDisplay dpy, EGLint * major, EGLint * minor);
typedef EGLBoolean (* my_eglChooseConfig_type)(EGLDisplay dpy, const EGLint * attrib_list, EGLConfig * configs, EGLint config_size, EGLint * num_config);
typedef EGLContext (* my_eglCreateContext_type)(EGLDisplay dpy, EGLConfig config, EGLContext share_context, const EGLint * attrib_list);
typedef EGLint (* my_eglGetError_type)(void);
typedef EGLBoolean (* my_eglMakeCurrent_type)(EGLDisplay dpy, EGLSurface draw, EGLSurface read, EGLContext ctx);

my_eglGetDisplay_type my_eglGetDisplay;
my_eglInitialize_type my_eglInitialize;
my_eglChooseConfig_type my_eglChooseConfig;
my_eglCreateContext_type my_eglCreateContext;
my_eglGetError_type my_eglGetError;
my_eglMakeCurrent_type my_eglMakeCurrent;

// OSMesa

#define OSMESA_RGBA GL_RGBA
#define OSMESA_DEPTH_BITS 0x30
#define OSMESA_STENCIL_BITS 0x31
#define OSMESA_ACCUM_BITS 0x32
#define OSMESA_PROFILE 0x33
#define OSMESA_CORE_PROFILE 0x34
#define OSMESA_COMPAT_PROFILE 0x35
#define OSMESA_CONTEXT_MAJOR_VERSION 0x36
#define OSMESA_CONTEXT_MINOR_VERSION 0x37

typedef struct osmesa_context * OSMesaContext;

typedef OSMesaContext (* my_OSMesaCreateContextExt_type)(GLenum format, GLint depthBits, GLint stencilBits, GLint accumBits, OSMesaContext sharelist);
typedef GLboolean (* my_OSMesaMakeCurrent_type)(OSMesaContext ctx, void * buffer, GLenum type, GLsizei width, GLsizei height);
typedef void (* my_OSMesaDestroyContext_type)(OSMesaContext ctx);
typedef OSMesaContext (* my_OSMesaCreateContextAttribs_type)(const int * attribList, OSMesaContext sharelist);

my_OSMesaCreateContextExt_type my_OSMesaCreateContextExt;
my_OSMesaMakeCurrent_type my_OSMesaMakeCurrent;
my_OSMesaDestroyContext_type my_OSMesaDestroyContext;
my_OSMesaCreateContextAttribs_type my_OSMesaCreateContextAttribs;

#endif

struct GLVersion {
	int major;
	int minor;
};

GLVersion version[] = {
	{4, 6},
	{4, 5},
	{4, 4},
	{4, 3},
	{4, 2},
	{4, 1},
	{4, 0},
	{3, 3},
	{3, 2},
	{3, 1},
	{0, 0},
};

int versions = sizeof(version) / sizeof(GLVersion);

#if defined(_WIN32) || defined(_WIN64)

PIXELFORMATDESCRIPTOR pfd = {
	sizeof(PIXELFORMATDESCRIPTOR),  // nSize
	1,                              // nVersion
	PFD_DRAW_TO_WINDOW |
	PFD_SUPPORT_OPENGL |
	PFD_GENERIC_ACCELERATED |
	PFD_DOUBLEBUFFER,               // dwFlags
	0,                              // iPixelType
	32,                             // cColorBits
	0,                              // cRedBits
	0,                              // cRedShift
	0,                              // cGreenBits
	0,                              // cGreenShift
	0,                              // cBlueBits
	0,                              // cBlueShift
	0,                              // cAlphaBits
	0,                              // cAlphaShift
	0,                              // cAccumBits
	0,                              // cAccumRedBits
	0,                              // cAccumGreenBits
	0,                              // cAccumBlueBits
	0,                              // cAccumAlphaBits
	24,                             // cDepthBits
	0,                              // cStencilBits
	0,                              // cAuxBuffers
	0,                              // iLayerType
	0,                              // bReserved
	0,                              // dwLayerMask
	0,                              // dwVisibleMask
	0,                              // dwDamageMask
};

GLContext LoadCurrentGLContext() {
	GLContext context = {};
	context.standalone = false;

	HGLRC hrc = wglGetCurrentContext();

	if (!hrc) {
		MGLError_Set("cannot detect context");
		return context;
	}

	HDC hdc = wglGetCurrentDC();

	if (!hdc) {
		MGLError_Set("cannot detect device content");
		return context;
	}

	HWND hwnd = WindowFromDC(hdc);

	if (!hwnd) {
		MGLError_Set("cannot detect window");
		return context;
	}

	context.hwnd = (void *)hwnd;
	context.hdc = (void *)hdc;
	context.hrc = (void *)hrc;

	return context;
}

void InitModernContext() {
	static bool initialized = false;

	if (initialized) {
		return;
	}

	initialized = true;

	HMODULE hinst = GetModuleHandle(0);

	if (!hinst) {
		return;
	}

	WNDCLASS extClass = {
		CS_OWNDC,                       // style
		DefWindowProc,                  // lpfnWndProc
		0,                              // cbClsExtra
		0,                              // cbWndExtra
		hinst,                          // hInstance
		0,                              // hIcon
		0,                              // hCursor
		0,                              // hbrBackground
		0,                              // lpszMenuName
		"ContextLoader",                // lpszClassName
	};

	if (!RegisterClass(&extClass)) {
		return;
	}

	HWND loader_hwnd = CreateWindow(
		"ContextLoader",                // lpClassName
		0,                              // lpWindowName
		0,                              // dwStyle
		0,                              // x
		0,                              // y
		0,                              // nWidth
		0,                              // nHeight
		0,                              // hWndParent
		0,                              // hMenu
		hinst,                          // hInstance
		0                               // lpParam
	);

	if (!loader_hwnd) {
		return;
	}

	HDC loader_hdc = GetDC(loader_hwnd);

	if (!loader_hdc) {
		return;
	}

	int loader_pixelformat = ChoosePixelFormat(loader_hdc, &pfd);

	if (!loader_pixelformat) {
		return;
	}

	if (!SetPixelFormat(loader_hdc, loader_pixelformat, &pfd)) {
		return;
	}

	HGLRC loader_hglrc = wglCreateContext(loader_hdc);

	if (!loader_hglrc) {
		return;
	}

	if (!wglMakeCurrent(loader_hdc, loader_hglrc)) {
		return;
	}

	my_CreateContextAttribs = (my_CreateContextAttribs_type)wglGetProcAddress("wglCreateContextAttribsARB");

	if (!my_CreateContextAttribs) {
		return;
	}

	my_ChoosePixelFormat = (my_ChoosePixelFormat_type)wglGetProcAddress("wglChoosePixelFormatARB");

	if (!my_ChoosePixelFormat) {
		return;
	}

	if (!wglMakeCurrent(0, 0)) {
		return;
	}

	if (!wglDeleteContext(loader_hglrc)) {
		return;
	}

	if (!ReleaseDC(loader_hwnd, loader_hdc)) {
		return;
	}

	if (!DestroyWindow(loader_hwnd)) {
		return;
	}

	if (!UnregisterClass("ContextLoader", hinst)) {
		return;
	}
}

GLContext CreateGLContext(PyObject * settings) {
	GLContext context = {};
	context.standalone = true;

	int width = 1;
	int height = 1;
	PyObject * size_hint = (settings != Py_None) ? PyDict_GetItemString(settings, "size") : 0;
	if (size_hint && Py_TYPE(size_hint) == &PyTuple_Type && PyTuple_GET_SIZE(size_hint) == 2) {
		width = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 0));
		height = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 1));
		width = width < 1 ? width : 1;
		height = height < 1 ? height : 1;
	}

	InitModernContext();

	HINSTANCE inst = GetModuleHandle(0);

	if (!inst) {
		MGLError_Set("module handle is null");
		return context;
	}

	static bool registered = false;

	if (!registered) {
		WNDCLASS wndClass = {
			CS_OWNDC,                            // style
			DefWindowProc,                       // lpfnWndProc
			0,                                   // cbClsExtra
			0,                                   // cbWndExtra
			inst,                                // hInstance
			0,                                   // hIcon
			0,                                   // hCursor
			0,                                   // hbrBackground
			0,                                   // lpszMenuName
			"StandaloneContext",                 // lpszClassName
		};

		if (!RegisterClass(&wndClass)) {
			MGLError_Set("cannot register window class");
			return context;
		}

		registered = true;
	}

	HWND hwnd = CreateWindowEx(
		0,                                   // exStyle
		"StandaloneContext",                 // lpClassName
		0,                                   // lpWindowName
		0,                                   // dwStyle
		0,                                   // x
		0,                                   // y
		width,                               // nWidth
		height,                              // nHeight
		0,                                   // hWndParent
		0,                                   // hMenu
		inst,                                // hInstance
		0                                    // lpParam
	);

	if (!hwnd) {
		MGLError_Set("cannot create window");
		return context;
	}

	HDC hdc = GetDC(hwnd);

	if (!hdc) {
		MGLError_Set("cannot create device content");
		return context;
	}

	HGLRC hrc = 0;

	if (my_CreateContextAttribs && my_ChoosePixelFormat) {

		int pixelformat = 0;
		unsigned num_formats = 0;

		if (!my_ChoosePixelFormat(hdc, 0, 0, 1, &pixelformat, &num_formats)) {
			MGLError_Set("cannot choose pixel format");
			return context;
		}

		if (!num_formats) {
			MGLError_Set("no pixel formats available");
			return context;
		}

		if (!SetPixelFormat(hdc, pixelformat, &pfd)) {
			MGLError_Set("cannot set pixel format");
			return context;
		}

		for (int i = 0; i < versions; ++i) {
			int attribs[] = {
				WGL_CONTEXT_PROFILE_MASK, WGL_CONTEXT_CORE_PROFILE_BIT,
				WGL_CONTEXT_MAJOR_VERSION, version[i].major,
				WGL_CONTEXT_MINOR_VERSION, version[i].minor,
				0, 0,
			};

			hrc = my_CreateContextAttribs(hdc, 0, attribs);

			if (hrc) {
				break;
			}
		}

	} else {

		int pf = ChoosePixelFormat(hdc, &pfd);

		if (!pf) {
			MGLError_Set("cannot choose pixel format");
			return context;
		}

		int set_pixel_format = SetPixelFormat(hdc, pf, &pfd);

		if (!set_pixel_format) {
			MGLError_Set("cannot set pixel format");
			return context;
		}

		hrc = wglCreateContext(hdc);

	}

	if (!hrc) {
		MGLError_Set("cannot create OpenGL context");
		return context;
	}

	int make_current = wglMakeCurrent(hdc, hrc);

	if (!make_current) {
		MGLError_Set("cannot select OpenGL context");
		return context;
	}

	context.hwnd = (void *)hwnd;
	context.hrc = (void *)hrc;
	context.hdc = (void *)hdc;

	return context;
}

void DestroyGLContext(const GLContext & context) {
	if (!context.standalone) {
		return;
	}

	if (wglGetCurrentContext() == context.hrc) {
		wglMakeCurrent(0, 0);
	}

	wglDeleteContext((HGLRC)context.hrc);
	ReleaseDC((HWND)context.hwnd, (HDC)context.hdc);
	DestroyWindow((HWND)context.hwnd);
}

#elif defined(__APPLE__)

GLContext LoadCurrentGLContext() {
	GLContext context = {};
	context.standalone = false;

	CGLContextObj cgl_context = CGLGetCurrentContext();

	if (!cgl_context) {
		MGLError_Set("cannot detect OpenGL context");
		return context;
	}

	context.context = (void *)cgl_context;

	return context;
}

GLContext CreateGLContext(PyObject * settings) {
	GLContext context = {};
	context.standalone = true;

	int width = 1;
	int height = 1;
	PyObject * size_hint = (settings != Py_None) ? PyDict_GetItemString(settings, "size") : 0;
	if (size_hint && Py_TYPE(size_hint) == &PyTuple_Type && PyTuple_GET_SIZE(size_hint) == 2) {
		width = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 0));
		height = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 1));
		width = width < 1 ? width : 1;
		height = height < 1 ? height : 1;
	}

	// CGDirectDisplayID display = CGMainDisplayID();
	// CGOpenGLDisplayMask cglDisplayMask = CGDisplayIDToOpenGLDisplayMask(display);
	// CGLContextObj curr_ctx = CGLGetCurrentContext();

	GLint num_pixelformats = 0;
	CGLPixelFormatObj pixelformat = 0;

	// kCGLPFAAccelerated
	CGLPixelFormatAttribute attribs[] = {
		kCGLPFAOpenGLProfile,
		(CGLPixelFormatAttribute)kCGLOGLPVersion_GL4_Core,
		(CGLPixelFormatAttribute)0,
	};

	CGLChoosePixelFormat(attribs, &pixelformat, &num_pixelformats);

	if (!pixelformat) {

		CGLPixelFormatAttribute attribs[] = {
			kCGLPFAOpenGLProfile,
			(CGLPixelFormatAttribute)kCGLOGLPVersion_GL3_Core,
			(CGLPixelFormatAttribute)0,
		};

		CGLChoosePixelFormat(attribs, &pixelformat, &num_pixelformats);

		if (!pixelformat) {
			CGLPixelFormatAttribute attribs[] = {
				(CGLPixelFormatAttribute)0,
			};

			CGLChoosePixelFormat(attribs, &pixelformat, &num_pixelformats);
		}
	}

	if (!pixelformat) {
		MGLError_Set("cannot choose pixel format");
		return context;
	}

	CGLContextObj cgl_context = 0;

	CGLCreateContext(pixelformat, 0, &cgl_context);
	CGLDestroyPixelFormat(pixelformat);

	if (!cgl_context) {
		MGLError_Set("cannot create OpenGL context");
		return context;
	}

	CGLSetCurrentContext(cgl_context);

	int fbo = 0;
	int color_rbo = 0;
	int depth_rbo = 0;

	glGenFramebuffers(1, (GLuint *)&fbo);
	glBindFramebuffer(GL_FRAMEBUFFER, fbo);

	glGenRenderbuffers(1, (GLuint *)&color_rbo);
	glBindRenderbuffer(GL_RENDERBUFFER, color_rbo);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, width, height);

	glGenRenderbuffers(1, (GLuint *)&depth_rbo);
	glBindRenderbuffer(GL_RENDERBUFFER, depth_rbo);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height);

	glFramebufferRenderbuffer(
		GL_FRAMEBUFFER,
		GL_COLOR_ATTACHMENT0,
		GL_RENDERBUFFER,
		color_rbo
	);

	glFramebufferRenderbuffer(
		GL_FRAMEBUFFER,
		GL_DEPTH_ATTACHMENT,
		GL_RENDERBUFFER,
		depth_rbo
	);

	int status = glCheckFramebufferStatus(GL_FRAMEBUFFER);

	if (status != GL_FRAMEBUFFER_COMPLETE) {
		const char * message = "the framebuffer is not complete";

		switch (status) {
			case GL_FRAMEBUFFER_UNDEFINED:
				message = "the framebuffer is not complete (UNDEFINED)";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:
				message = "the framebuffer is not complete (INCOMPLETE_ATTACHMENT)";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT:
				message = "the framebuffer is not complete (INCOMPLETE_MISSING_ATTACHMENT)";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER:
				message = "the framebuffer is not complete (INCOMPLETE_DRAW_BUFFER)";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER:
				message = "the framebuffer is not complete (INCOMPLETE_READ_BUFFER)";
				break;

			case GL_FRAMEBUFFER_UNSUPPORTED:
				message = "the framebuffer is not complete (UNSUPPORTED)";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE:
				message = "the framebuffer is not complete (INCOMPLETE_MULTISAMPLE)";
				break;
		}

		MGLError_Set(message);
		return context;
	}

	context.context = (void *)cgl_context;

	return context;
}

void DestroyGLContext(const GLContext & context) {
	if (!context.standalone) {
		return;
	}

	if (context.context) {
		CGLDestroyContext((CGLContextObj)context.context);
		// context.context = 0;
	}
}

#else

GLContext LoadCurrentGLContext() {
	GLContext context = {};
	context.standalone = false;

	Display * dpy = glXGetCurrentDisplay();

	if (!dpy) {
		MGLError_Set("cannot detect display");
		return context;
	}

	Window win = glXGetCurrentDrawable();

	if (!win) {
		MGLError_Set("cannot detect window");
		return context;
	}

	GLXContext ctx = glXGetCurrentContext();

	if (!ctx) {
		MGLError_Set("cannot detect OpenGL context");
		return context;
	}

	context.display = (void *)dpy;
	context.window = (void *)win;
	context.context = (void *)ctx;

	return context;
}

GLContext CreateGLContext(PyObject * settings) {
	GLContext context = {};
	context.standalone = true;

	PyObject * backend_obj = PyDict_GetItemString(settings, "backend");
	const char * backend = backend_obj ? PyUnicode_AsUTF8(backend_obj) : "X11";

	if (!strcmp(backend, "EGL")) {
		const char * so = "libEGL.so.1";
		void * handle = dlopen(so, RTLD_LAZY);

		if (!handle) {
			MGLError_Set("cannot load %s\n", so);
			return context;
		}

		my_eglGetDisplay = (my_eglGetDisplay_type) dlsym(handle, "eglGetDisplay");
		if (!my_eglGetDisplay) {
			MGLError_Set("cannot load eglGetDisplay");
			return context;
		}

		my_eglInitialize = (my_eglInitialize_type) dlsym(handle, "eglInitialize");
		if (!my_eglInitialize) {
			MGLError_Set("cannot load eglInitialize");
			return context;
		}

		my_eglChooseConfig = (my_eglChooseConfig_type) dlsym(handle, "eglChooseConfig");
		if (!my_eglChooseConfig) {
			MGLError_Set("cannot load eglChooseConfig");
			return context;
		}

		my_eglCreateContext = (my_eglCreateContext_type) dlsym(handle, "eglCreateContext");
		if (!my_eglCreateContext) {
			MGLError_Set("cannot load eglCreateContext");
			return context;
		}

		my_eglGetError = (my_eglGetError_type) dlsym(handle, "eglGetError");
		if (!my_eglGetError) {
			MGLError_Set("cannot load eglGetError");
			return context;
		}

		my_eglMakeCurrent = (my_eglMakeCurrent_type) dlsym(handle, "eglMakeCurrent");
		if (!my_eglMakeCurrent) {
			MGLError_Set("cannot load eglMakeCurrent");
			return context;
		}

		EGLDisplay display = my_eglGetDisplay(0);

		if (display == EGL_NO_DISPLAY) {
			MGLError_Set("cannot detect EGL display");
			return context;
		}

		int init = my_eglInitialize(display, NULL, NULL);
		if (init == EGL_BAD_DISPLAY) {
			MGLError_Set("invalid EGL display");
			return context;
		}

		static int const attribute_list_egl[] = {
			EGL_RED_SIZE, 1,
			EGL_GREEN_SIZE, 1,
			EGL_BLUE_SIZE, 1,
			EGL_NONE
		};

		int num_config = 0;
		EGLConfig config;

		if (!my_eglChooseConfig(display, attribute_list_egl, &config, 1, &num_config)) {
			MGLError_Set("cannot get EGL display config");
			return context;
		}

		EGLContext ctx = my_eglCreateContext(display, config, EGL_NO_CONTEXT, NULL);

		if (!ctx) {
			MGLError_Set("cannot create EGL context");
			return context;
		}

		if (!my_eglMakeCurrent(display, NULL, NULL, ctx)) {
			MGLError_Set("cannot select OpenGL context");
			return context;
		}

		context.display = display;
		context.context = ctx;
		return context;
	}

	if (!strcmp(backend, "OSMesa")) {
		const char * so = "libOSMesa.so";
		void * handle = dlopen(so, RTLD_LAZY);

		if (!handle) {
			MGLError_Set("cannot load %s\n", so);
			return context;
		}

		my_OSMesaCreateContextExt = (my_OSMesaCreateContextExt_type) dlsym(handle, "OSMesaCreateContextExt");
		if (!my_OSMesaCreateContextExt) {
			MGLError_Set("cannot load OSMesaCreateContextExt");
			return context;
		}

		my_OSMesaMakeCurrent = (my_OSMesaMakeCurrent_type) dlsym(handle, "OSMesaMakeCurrent");
		if (!my_OSMesaMakeCurrent) {
			MGLError_Set("cannot load OSMesaMakeCurrent");
			return context;
		}

		my_OSMesaDestroyContext = (my_OSMesaDestroyContext_type) dlsym(handle, "OSMesaDestroyContext");
		if (!my_OSMesaDestroyContext) {
			MGLError_Set("cannot load OSMesaDestroyContext");
			return context;
		}

		my_OSMesaCreateContextAttribs = (my_OSMesaCreateContextAttribs_type) dlsym(handle, "OSMesaCreateContextAttribs");
		if (!my_OSMesaCreateContextAttribs) {
			MGLError_Set("cannot load OSMesaCreateContextAttribs");
			return context;
		}

		const int attribList[] = {
			OSMESA_PROFILE, OSMESA_COMPAT_PROFILE,
			OSMESA_CONTEXT_MAJOR_VERSION, 2,
			OSMESA_CONTEXT_MINOR_VERSION, 0,
			0, 0
		};

		OSMesaContext ctx = my_OSMesaCreateContextAttribs(attribList, NULL);

		if (!ctx) {
			MGLError_Set("OSMesaCreateContextExt failed");
			return context;
		}

		void * buffer = malloc(1 * 1 * 4 * sizeof(GLubyte));

		if (!my_OSMesaMakeCurrent(ctx, buffer, GL_UNSIGNED_BYTE, 1, 1)) {
			MGLError_Set("cannot select OpenGL context");
			return context;
		}

		context.context = ctx;
		context.buffer = buffer;
		return context;
	}

	if (!strcmp(backend, "X11")) {
		const char * so = "libX11.so";
		void * handle = dlopen(so, RTLD_LAZY);

		if (!handle) {
			MGLError_Set("cannot load %s\n", so);
			return context;
		}

		my_XOpenDisplay = (my_XOpenDisplay_type) dlsym(handle, "XOpenDisplay");
		if (!my_XOpenDisplay) {
			MGLError_Set("cannot load XOpenDisplay");
			return context;
		}

		my_XCloseDisplay = (my_XCloseDisplay_type) dlsym(handle, "XCloseDisplay");
		if (!my_XCloseDisplay) {
			MGLError_Set("cannot load XCloseDisplay");
			return context;
		}

		my_XDestroyWindow = (my_XDestroyWindow_type) dlsym(handle, "XDestroyWindow");
		if (!my_XDestroyWindow) {
			MGLError_Set("cannot load XDestroyWindow");
			return context;
		}

		my_XCreateWindow = (my_XCreateWindow_type) dlsym(handle, "XCreateWindow");
		if (!my_XCreateWindow) {
			MGLError_Set("cannot load XCreateWindow");
			return context;
		}

		my_XSetErrorHandler = (my_XSetErrorHandler_type) dlsym(handle, "XSetErrorHandler");
		if (!my_XSetErrorHandler) {
			MGLError_Set("cannot load XSetErrorHandler");
			return context;
		}

		my_XCreateColormap = (my_XCreateColormap_type) dlsym(handle, "XCreateColormap");
		if (!my_XCreateColormap) {
			MGLError_Set("cannot load XCreateColormap");
			return context;
		}

		int width = 1;
		int height = 1;
		PyObject * size_hint = (settings != Py_None) ? PyDict_GetItemString(settings, "size") : 0;
		if (size_hint && Py_TYPE(size_hint) == &PyTuple_Type && PyTuple_GET_SIZE(size_hint) == 2) {
			width = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 0));
			height = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 1));
			width = width < 1 ? width : 1;
			height = height < 1 ? height : 1;
		}

		Display * dpy = my_XOpenDisplay(0);

		if (!dpy) {
			dpy = my_XOpenDisplay(":0.0");
		}

		if (!dpy) {
			MGLError_Set("cannot detect the display");
			return context;
		}

		int nelements = 0;

		GLXFBConfig * fbc = glXChooseFBConfig(dpy, 0, 0, &nelements);

		if (!fbc) {
			MGLError_Set("cannot read the display configuration");
			my_XCloseDisplay(dpy);
			return context;
		}

		static int attributeList[] = {
			GLX_RGBA,
			GLX_DOUBLEBUFFER,
			GLX_RED_SIZE, 8,
			GLX_GREEN_SIZE, 8,
			GLX_BLUE_SIZE, 8,
			GLX_DEPTH_SIZE, 24,
			GLX_NONE,
		};

		XVisualInfo * vi = glXChooseVisual(dpy, 0, attributeList);

		if (!vi) {
			my_XCloseDisplay(dpy);

			MGLError_Set("cannot choose a visual info");
			return context;
		}

		XSetWindowAttributes swa;
		swa.colormap = my_XCreateColormap(dpy, RootWindow(dpy, vi->screen), vi->visual, AllocNone);
		swa.border_pixel = 0;
		swa.event_mask = StructureNotifyMask;

		Window win = my_XCreateWindow(dpy, RootWindow(dpy, vi->screen), 0, 0, width, height, 0, vi->depth, InputOutput, vi->visual, CWBorderPixel | CWColormap | CWEventMask, &swa);

		if (!win) {
			my_XCloseDisplay(dpy);

			MGLError_Set("cannot create window");
			return context;
		}

		GLXCREATECONTEXTATTRIBSARBPROC glXCreateContextAttribsARB = (GLXCREATECONTEXTATTRIBSARBPROC)glXGetProcAddress((const GLubyte *)"glXCreateContextAttribsARB");

		GLXContext ctx = 0;

		my_XSetErrorHandler(SilentXErrorHandler);

		if (glXCreateContextAttribsARB) {
			for (int i = 0; i < versions; ++i) {
				int attribs[] = {
					GLX_CONTEXT_PROFILE_MASK, GLX_CONTEXT_CORE_PROFILE_BIT,
					GLX_CONTEXT_MAJOR_VERSION, version[i].major,
					GLX_CONTEXT_MINOR_VERSION, version[i].minor,
					0, 0,
				};

				ctx = glXCreateContextAttribsARB(dpy, *fbc, 0, true, attribs);

				if (ctx) {
					break;
				}
			}
		}

		if (!ctx) {
			ctx = glXCreateContext(dpy, vi, 0, GL_TRUE);
		}

		if (!ctx) {
			my_XDestroyWindow(dpy, win);
			my_XCloseDisplay(dpy);

			MGLError_Set("cannot create OpenGL context");
			return context;
		}

		my_XSetErrorHandler(0);

		int make_current = glXMakeCurrent(dpy, win, ctx);

		if (!make_current) {
			glXDestroyContext(dpy, ctx);
			my_XDestroyWindow(dpy, win);
			my_XCloseDisplay(dpy);

			MGLError_Set("cannot select OpenGL context");
			return context;
		}

		context.display = (void *) dpy;
		context.window = (void *) win;
		context.context = (void *) ctx;
		return context;
	}

	MGLError_Set("cannot find implementation for %s", backend);
	return context;
}

void DestroyGLContext(const GLContext & context) {
	if (!context.standalone) {
		return;
	}

	if (context.display) {
		glXMakeCurrent((Display *)context.display, 0, 0);

		if (context.context) {
			glXDestroyContext((Display *)context.display, (GLXContext)context.context);
			// context.context = 0;
		}

		if (context.window) {
			XDestroyWindow((Display *)context.display, (Window)context.window);
			// context.window = 0;
		}

		XCloseDisplay((Display *)context.display);
		// context.display = 0;
	}
}

#endif
