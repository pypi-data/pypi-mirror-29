/*
 * Copied from pyFAI
 */

#include <stdlib.h>
#include <stdint.h>
#include <memory.h>
#include <Python.h>
#include "bispev.h"


static void fpbspl(float *t, int k, float x, int l, float *h, float *hh) {
    int i, j;
    float f;

    h[0] = 1;
    for (j=1; j<=k; ++j) {
        for (i=0; i<j; ++i)
            hh[i] = h[i];
        h[0] = 0;
        for (i=0; i<j; ++i) {
            f = hh[i] / (t[l + i] - t[l + i - j]);
            h[i] = h[i] + f * (t[l + i] - x);
            h[i + 1] = f * (x - t[l + i - j]);
        }
    }
}


static void init_w(float *t, int n, int k, float *x, int m, int32_t *lx, float *w) {
    int i, j, l, l1;
    float arg, tb, te, h[6], hh[5];

    tb = t[k];
    te = t[n - k - 1];
    l = k + 1;
    l1 = l + 1;
    for (i=0; i<m; ++i) {
        arg = x[i];
        if (arg < tb)
            arg = tb;
        if (arg > te)
            arg = te;
        while (!(arg < t[l] || l == (n - k - 1))) {
            l = l1;
            l1 = l + 1;
        }
        fpbspl(t, k, arg, l, h, hh);

        lx[i] = l - k - 1;
        for (j=0; j<=k; ++j)
            w[i*(k+1)+j] = h[j];
    }
}


spline_result *bispev(spline *b) {
    int kx1, ky1, nky1, i, j, i1, l2, j1, wxs, wys;
    float *wx, *wy, *z, sp, err, tmp, a;
    int32_t *lx, *ly;
    char *mem;
    spline_result *res;

    res = malloc(sizeof(spline_result));
    if (res == NULL)
        return NULL;

    kx1 = b->kx + 1;
    ky1 = b->ky + 1;
    nky1 = (int)b->ny - ky1;

    wxs = (int)b->mx * kx1;
    wys = (int)b->my * ky1;
    mem = malloc((wxs + wys) * sizeof(float) + (b->mx + b->my) * sizeof(int32_t));
    if (mem == NULL)
        return NULL;
    z = calloc(b->zs, sizeof(float));
    if (z == NULL)
        return NULL;

    wx = (float *)mem;
    wy = wx + wxs;
    lx = (int32_t *)(wy + wys);
    ly = lx + b->mx;

    init_w(b->tx, (int)b->nx, b->kx, b->x, (int)b->mx, lx, wx);
    init_w(b->ty, (int)b->ny, b->ky, b->y, (int)b->my, ly, wy);

    for (j=0; j<b->my; ++j) {
        for (i=0; i<b->mx; ++i) {
            sp = 0; err = 0;
            for (i1=0; i1<kx1; ++i1) {
                for (j1=0; j1<ky1; ++j1) {
                    l2 = lx[i] * nky1 + ly[j] + i1 * nky1 + j1;
                    a = b->c[l2] * wx[i*kx1+i1] * wy[j*ky1+j1] - err;
                    tmp = sp + a;
                    err = tmp - sp - a;
                    sp = tmp;
                }
            }
            z[j*b->mx+i] += sp;
        }
    }
    res->z = z;
    res->mx = b->mx;
    res->my = b->my;
    res->zs = b->zs;
    res->zss = b->zss;
    res->shape[0] = res->my;
    res->shape[1] = res->mx;
    res->strides[0] = res->my * (Py_ssize_t)sizeof(float);
    res->strides[1] = (Py_ssize_t)sizeof(float);
    free(mem);
    return res;
}

void destroy_bispev(spline_result *res) {
    if (res != NULL) {
        if (res->z != NULL)
            free(res->z);
        free(res);
    }
}
