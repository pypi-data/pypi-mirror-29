#ifndef CDECOR_DISTORTION_H_   /* Include guard */
#define CDECOR_DISTORTION_H_ 1

#include <stdint.h>
#include <Python.h>

typedef struct {
    uint32_t dim1;
    uint32_t dim2;
    uint32_t array_size;
    uint32_t array_buf_size;
    uint32_t *lut_size;
    uint32_t lut_size_max;
    int delta0;
    int delta1;
    float *lut_coef;
    int32_t *lut_idx;
    int *out_max;
    float *buffer;
    uint32_t buffer_size;
} distortion;

typedef struct {
    float *image;
    Py_ssize_t dim1;
    Py_ssize_t dim2;
    Py_ssize_t array_size;
    Py_ssize_t array_buf_size;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} distortion_results;

void destroy_distortion(distortion *dist);
distortion *init_distortion(int dim1, int dim2, int delta0, int delta1, float *pos);
distortion_results *correct_lut(distortion *dist, float *image);
void destroy_distortion_results(distortion_results *res);

#endif  // CDECOR_DISTORTION_H_
