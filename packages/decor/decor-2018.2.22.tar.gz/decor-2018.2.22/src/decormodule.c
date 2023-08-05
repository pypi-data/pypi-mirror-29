#include <Python.h>
#include <memory.h>
#include <stdint.h>
#include "distortion.h"
#include "bispev.h"


typedef struct {
    PyObject_HEAD
    distortion *dist;
} _distortion;


static int
_distortion_init(_distortion *self, PyObject *args) {
    int dim1, dim2, delta0, delta1;
    PyObject *np_pos;
    Py_buffer pos;
    distortion *dist;

    if (!PyArg_ParseTuple(args, "iiiiO", &dim1, &dim2, &delta0, &delta1, &np_pos))
        return -1;

    destroy_distortion(self->dist);
    PyObject_GetBuffer(np_pos, &pos, PyBUF_C_CONTIGUOUS);
    Py_BEGIN_ALLOW_THREADS
    dist = init_distortion(dim1, dim2, delta0, delta1, (float *)pos.buf);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&pos);

    if (dist == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for lookup tables. Buy more RAM.");
        return -1;
    }
    self->dist = dist;
    return 0;
}


static void
_distortion_dealloc(_distortion *self) {
    destroy_distortion(self->dist);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyTypeObject _distortion_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_decor._distortion",                       /* tp_name */
    sizeof(_distortion),                        /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)_distortion_dealloc,            /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_distortion object",                       /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)_distortion_init,                 /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
    distortion_results *res;
} _distortion_cor;


static int
_distortion_cor_init(_distortion_cor *self, PyObject *args) {
    PyObject *np_image;
    _distortion *py_distortion;
    Py_buffer image;
    distortion_results *res;

    if (!PyArg_ParseTuple(args, "OO", &py_distortion, &np_image))
        return -1;

    destroy_distortion_results(self->res);
    PyObject_GetBuffer(np_image, &image, PyBUF_C_CONTIGUOUS);
    if (image.len != py_distortion->dist->array_buf_size) {
        PyBuffer_Release(&image);
        PyErr_SetString(PyExc_ValueError, "The image has wrong dimensions");
        return -1;
    }

    Py_BEGIN_ALLOW_THREADS
    res = correct_lut(py_distortion->dist, (float *)image.buf);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&image);

    if (res == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Cannot allocate memory for image distortion. Buy more RAM.");
        return -1;
    }
    self->res = res;
    return 0;
}


static void
_distortion_cor_dealloc(_distortion_cor *self) {
    destroy_distortion_results(self->res);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_distortion_cor_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _distortion_cor *self = (_distortion_cor *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->res->image;
    view->len = self->res->array_buf_size;
    view->readonly = 1;
    view->itemsize = sizeof(float);
    view->format = "f";
    view->ndim = 2;
    view->shape = self->res->shape;
    view->strides = self->res->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}

static PyBufferProcs _distortion_cor_as_buffer = {
  (getbufferproc)_distortion_cor_getbuffer,
  (releasebufferproc)0,
};

static PyTypeObject _distortion_cor_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_decor._distortion_cor",                   /* tp_name */
    sizeof(_distortion_cor),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)_distortion_cor_dealloc,        /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &_distortion_cor_as_buffer,                 /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_distortion_cor object",                   /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)_distortion_cor_init,             /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
    spline_result *res;
} _bispev;


static int
_bispev_init(_bispev *self, PyObject *args) {
    int kx, ky;
    PyObject *tx, *ty, *c, *x, *y;
    Py_buffer _tx, _ty, _c, _x, _y;
    spline b;
    spline_result *z;

    if (!PyArg_ParseTuple(args, "OOOiiOO", &tx, &ty, &c, &kx, &ky, &x, &y))
        return -1;

    destroy_bispev(self->res);
    PyObject_GetBuffer(tx, &_tx, PyBUF_C_CONTIGUOUS);
    PyObject_GetBuffer(ty, &_ty, PyBUF_C_CONTIGUOUS);
    PyObject_GetBuffer(c,  &_c,  PyBUF_C_CONTIGUOUS);
    PyObject_GetBuffer(x,  &_x,  PyBUF_C_CONTIGUOUS);
    PyObject_GetBuffer(y,  &_y,  PyBUF_C_CONTIGUOUS);
    Py_BEGIN_ALLOW_THREADS
    b.tx = (float *)_tx.buf;
    b.nx = _tx.shape[0];
    b.ty = (float *)_ty.buf;
    b.ny = _ty.shape[0];
    b.kx = kx;
    b.ky = ky;
    b.c = (float *)_c.buf;
    b.nc = _c.shape[0];
    b.x = (float *)_x.buf;
    b.mx = _x.shape[0];
    b.y = (float *)_y.buf;
    b.my = _y.shape[0];
    b.zs = b.mx * b.my;
    b.zss = b.zs * sizeof(float);
    z = bispev(&b);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&_tx);
    PyBuffer_Release(&_ty);
    PyBuffer_Release(&_c);
    PyBuffer_Release(&_x);
    PyBuffer_Release(&_y);

    if (z == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Cannot allocate memory for spline calculations. Buy more RAM.");
        return -1;
    }
    self->res = z;
    return 0;
}


static void
_bispev_dealloc(_bispev *self) {
    destroy_bispev(self->res);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int
_bispev_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _bispev *self = (_bispev *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->res->z;
    view->len = self->res->zss;
    view->readonly = 1;
    view->itemsize = (Py_ssize_t)sizeof(float);
    view->format = "f";
    view->ndim = 2;
    view->shape = self->res->shape;
    view->strides = self->res->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}

static PyBufferProcs _bispev_as_buffer = {
  (getbufferproc)_bispev_getbuffer,
  (releasebufferproc)0,
};

static PyTypeObject _bispev_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_decor._bispev",                          /* tp_name */
    sizeof(_bispev),                           /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)_bispev_dealloc,               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &_bispev_as_buffer,                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_bispev object",                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)_bispev_init,                    /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


static PyMethodDef _decor_methods[] = {
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _decor_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _decor_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_decor",
    NULL,
    sizeof(struct module_state),
    _decor_methods,
    NULL,
    _decor_traverse,
    _decor_clear,
    NULL
};


PyMODINIT_FUNC PyInit__decor(void) {
    PyObject *module;
    struct module_state *st;

    _distortion_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_distortion_type) < 0)
        return NULL;

    _distortion_cor_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_distortion_cor_type) < 0)
        return NULL;

    _bispev_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&_bispev_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_decor.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&_distortion_type);
    PyModule_AddObject(module, "_distortion", (PyObject *)&_distortion_type);

    Py_INCREF(&_distortion_cor_type);
    PyModule_AddObject(module, "_distortion_cor", (PyObject *)&_distortion_cor_type);

    Py_INCREF(&_bispev_type);
    PyModule_AddObject(module, "_bispev", (PyObject *)&_bispev_type);

    return module;
}
