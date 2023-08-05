#ifndef CDECOR_BISPEV_H_   /* Include guard */
#define CDECOR_BISPEV_H_ 1

#include <Python.h>

typedef struct {
    float *tx;
    Py_ssize_t nx;
    float *ty;
    Py_ssize_t ny;
    float *c;
    Py_ssize_t nc;
    int kx;
    int ky;
    float *x;
    Py_ssize_t mx;
    float *y;
    Py_ssize_t my;
    Py_ssize_t zs;
    Py_ssize_t zss;
} spline;


typedef struct {
    float *z;
    Py_ssize_t mx;
    Py_ssize_t my;
    Py_ssize_t zs;
    Py_ssize_t zss;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} spline_result;


spline_result *bispev(spline *b);
void destroy_bispev(spline_result *res);

#endif  // CDECOR_BISPEV_H_
