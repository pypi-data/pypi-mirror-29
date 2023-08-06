/* Created by "go tool cgo" - DO NOT EDIT. */

/* package github.com/asottile/dockerfile/pylib */

/* Start of preamble from import "C" comments.  */


#line 3 "/tmp/tmpl6qr1ui6/src/github.com/asottile/dockerfile/pylib/main.go"
 #include <stdlib.h>
 #include <Python.h>

 extern int PyDockerfile_PyArg_ParseTuple_U(PyObject*, PyObject**);
 extern PyObject* PyDockerfile_Py_None;

 extern PyObject* PyDockerfile_GoIOError;
 extern PyObject* PyDockerfile_GoParseError;
 extern PyObject* PyDockerfile_NewCommand(
     PyObject*, PyObject*, PyObject*, PyObject*, PyObject*, PyObject*,
     PyObject*
 );



/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

typedef struct { const char *p; GoInt n; } GoString;
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


extern PyObject* all_cmds(PyObject* p0);

extern PyObject* parse_file(PyObject* p0, PyObject* p1);

extern PyObject* parse_string(PyObject* p0, PyObject* p1);

#ifdef __cplusplus
}
#endif
