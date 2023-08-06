#ifndef CRYIO_AGI_BITFIELD_H_   /* Include guard */
#define CRYIO_AGI_BITFIELD_H_ 1

#include <stdlib.h>
#include <stdint.h>
#include <Python.h>

typedef struct {
    Py_ssize_t n_pixels;
    Py_ssize_t dim;
    Py_ssize_t buf_size;
    int8_t *mem;
    int32_t *addrs;
} espdata;

espdata *encode_agi_bitfield(Py_buffer *buf);
void _destroy_esp(espdata *esp);

#endif  // CRYIO_AGI_BITFIELD_H_
