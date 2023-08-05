/*
#
# Copyright © 2017 Malek Hadj-Ali
# All rights reserved.
#
# This file is part of mood.
#
# mood is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# mood is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mood.  If not, see <http://www.gnu.org/licenses/>.
#
*/


#ifdef _PY_INLINE_HELPERS
#define _Py_INLINE(type) static inline type
#else
#define _Py_INLINE(type) type
#endif

#ifndef _Py_MIN_ALLOC
#define _Py_MIN_ALLOC 8
#endif


/* misc helpers ------------------------------------------------------------- */

#define _Py_SET_MEMBER(m, op) \
    do { \
        PyObject *_py_tmp = (PyObject *)(m); \
        Py_INCREF((op)); \
        (m) = (op); \
        Py_XDECREF(_py_tmp); \
    } while (0)

#define _Py_RETURN_OBJECT(op) \
    do { \
        PyObject *_py_res = (PyObject *)(op); \
        return Py_INCREF(_py_res), _py_res; \
    } while (0)

#define _PyDict_GET_SIZE(op) (((PyDictObject *)(op))->ma_used)

#define _PyTuple_ITEMS(op) (((PyTupleObject *)(op))->ob_item)


/* the std PyObject_HasAttr clears traceback when result is 0 */
int
_PyObject_HasAttr(PyObject *obj, PyObject *name)
{
    PyObject *exc_type = NULL, *exc_value = NULL, *exc_traceback = NULL;
    PyObject *attr = NULL;
    int res = 0;

    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if ((res = ((attr = PyObject_GetAttr(obj, name)) != NULL))) {
        Py_DECREF(attr);
    }
    else {
        PyErr_Clear();
    }
    PyErr_Restore(exc_type, exc_value, exc_traceback);
    return res;
}


int
__PyObject_HasAttrId(PyObject *obj, _Py_Identifier *id)
{
    PyObject *name = NULL;

    // name is borrowed
    return ((name = _PyUnicode_FromId(id))) ? _PyObject_HasAttr(obj, name) : -1;
}


/* module init helpers ------------------------------------------------------ */

#define _PyModule_AddIntConstant(m, n, v) \
    PyModule_AddIntConstant((m), (n), (int)(v))

#define _PyModule_AddUnsignedIntConstant(m, n, v) \
    PyModule_AddIntConstant((m), (n), (unsigned int)(v))

#define _PyModule_AddIntMacro(m, c) \
    _PyModule_AddIntConstant((m), #c, (c))

#define _PyModule_AddUnsignedIntMacro(m, c) \
    _PyModule_AddUnsignedIntConstant((m), #c, (c))


int
_PyType_ReadyWithBase(PyTypeObject *type, PyTypeObject *base)
{
    type->tp_base = base;
    return PyType_Ready(type);
}


static inline int
_PyModule_AddObject(PyObject *module, const char *name, PyObject *object)
{
    Py_INCREF(object);
    if (PyModule_AddObject(module, name, object)) {
        Py_DECREF(object);
        return -1;
    }
    return 0;
}


int
_PyModule_AddType(PyObject *module, const char *name, PyTypeObject *type)
{
    if (PyType_Ready(type)) {
        return -1;
    }
    return _PyModule_AddObject(module, name, (PyObject *)type);
}


int
_PyModule_AddTypeWithBase(PyObject *module, const char *name,
                          PyTypeObject *type, PyTypeObject *base)
{
    type->tp_base = base;
    return _PyModule_AddType(module, name, type);
}


int
_PyModule_AddNewException(PyObject *module, const char *name,
                          const char *module_name, PyObject *base,
                          PyObject *dict, PyObject **result)
{
    const char *mod_name = NULL;
    char *full_name = NULL;
    PyObject *exception = NULL;
    size_t full_size = 1; // dot

    if (!(mod_name = (module_name) ? module_name : PyModule_GetName(module))) {
        return -1;
    }
    full_size += strlen(mod_name) + strlen(name);
    if (!(full_name = PyObject_Malloc(full_size + 1))) { // terminator
        PyErr_NoMemory();
        return -1;
    }
    if (PyOS_snprintf(full_name, full_size + 1,
                      "%s.%s", mod_name, name) != full_size) {
        PyObject_Free(full_name);
        if (errno) {
            PyErr_SetFromErrno(PyExc_OSError);
        }
        else {
            PyErr_SetString(PyExc_OSError, "PyOS_snprintf failed");
        }
        return -1;
    }
    exception = PyErr_NewException(full_name, base, dict);
    PyObject_Free(full_name);
    if (!exception || _PyModule_AddObject(module, name, exception)) {
        Py_XDECREF(exception);
        return -1;
    }
    if (result) {
        *result = exception;
    }
    else {
        Py_DECREF(exception);
    }
    return 0;
}


/* module state helpers ----------------------------------------------------- */

void *
_PyModule_GetState(PyObject *module)
{
    void *state = NULL;

    if (!(state = PyModule_GetState(module)) && !PyErr_Occurred()) {
        PyErr_Format(PyExc_SystemError, "no state attached to %R", module);
    }
    return state;
}


void *
_PyModuleDef_GetState(PyModuleDef *def)
{
    PyObject *module = NULL;

    if (!(module = PyState_FindModule(def))) { // borrowed
        PyErr_Format(PyExc_SystemError,
                     "<module '%s'> not found in interpreter state",
                     def->m_name ? def->m_name : "unknown");
        return NULL;
    }
    return _PyModule_GetState(module);
}


/* err helpers -------------------------------------------------------------- */

PyObject *
_PyErr_SetFromErrnoWithFilename(const char *filename)
{
    switch (errno) {
        case ENOMEM:
            return PyErr_NoMemory();
        default:
            return PyErr_SetFromErrnoWithFilename(PyExc_OSError, filename);
    }
}


PyObject *
_PyErr_SetFromErrnoWithFilenameAndChain(const char *filename)
{
    PyObject *exc_type, *exc_value, *exc_traceback;

    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    _PyErr_SetFromErrnoWithFilename(filename);
    _PyErr_ChainExceptions(exc_type, exc_value, exc_traceback);
    return NULL;
}


#define _PyErr_SetFromErrno() \
    _PyErr_SetFromErrnoWithFilename(NULL)

#define _PyErr_SetFromErrnoAndChain() \
    _PyErr_SetFromErrnoWithFilenameAndChain(NULL)


/* alloc helpers ------------------------------------------------------------ */

/* the std _PyObject_GC_New doesn't memset -> segfault when subclassing */
PyObject *
__PyObject_GC_New(PyTypeObject *type)
{
    PyObject *self = NULL;

    if (!(self = _PyObject_GC_Calloc(_PyObject_SIZE(type)))) {
        return PyErr_NoMemory();
    }
    return PyObject_INIT(self, type);
}


#define __PyObject_Alloc(type, typeobj) ((type *)__PyObject_GC_New((typeobj)))


/* bytearray helpers -------------------------------------------------------- */

_Py_INLINE(int)
__PyByteArray_Grow(PyByteArrayObject *self, Py_ssize_t size, const char *bytes,
                   Py_ssize_t initsize)
{
    Py_ssize_t osize, nsize, nalloc, alloc;
    char *tmp = NULL;

    if (size <= 0) {
        PyErr_BadInternalCall();
        return -1;
    }
    if ((nalloc = ((nsize = ((osize = Py_SIZE(self)) + size)) + 1)) < 0) {
        PyErr_NoMemory();
        return -1;
    }
    if (self->ob_alloc < nalloc) {
        alloc = (self->ob_alloc) ? (self->ob_alloc << 1) : initsize;
        while (alloc < nalloc) {
            alloc <<= 1;
            if (alloc < 0) {
                alloc = nalloc;
                break;
            }
        }
        if (!(tmp = (char *)PyObject_Realloc(self->ob_bytes, alloc))) {
            PyErr_NoMemory();
            return -1;
        }
        self->ob_bytes = self->ob_start = tmp;
        self->ob_alloc = alloc;
    }
    memcpy((self->ob_bytes + osize), bytes, size);
    Py_SIZE(self) = nsize;
    self->ob_bytes[nsize] = '\0';
    return 0;
}


_Py_INLINE(int)
__PyByteArray_Shrink(PyByteArrayObject *self, Py_ssize_t size)
{
    Py_ssize_t nsize = Py_SIZE(self) - size;
    char *buf = PyByteArray_AS_STRING(self);

    if (nsize < 0) {
        PyErr_BadInternalCall();
        return -1;
    }
    if (nsize > 0) {
        memmove(buf, buf + size, nsize);
    }
    // XXX: very bad shortcut ¯\_(ツ)_/¯
    Py_SIZE(self) = nsize;
    PyByteArray_AS_STRING(self)[nsize] = '\0';
    return 0;
}
