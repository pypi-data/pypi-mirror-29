#ifndef CRYIO_MAR345_H_   /* Include guard */
#define CRYIO_MAR345_H_ 1

#include <stdint.h>
#include <Python.h>


typedef struct {
    Py_ssize_t n_pixels;
    Py_ssize_t dim1;
    Py_ssize_t dim2;
    Py_ssize_t buf_size;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
    uint32_t *image;
} mardata;


void _destroy_mar(mardata *mar);
mardata *_decode_mar_image(int32_t dim1, int32_t dim2, int32_t of, char *packed, char *oft);

#endif  // CRYIO_MAR345_H_
