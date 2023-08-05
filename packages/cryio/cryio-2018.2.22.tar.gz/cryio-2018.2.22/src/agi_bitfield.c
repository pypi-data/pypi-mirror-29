/*
 * Agilent bitfield compression
 * Thanks to Pascal <pascal22p@parois.net>
 * The code is based on
 * https://redmine.debroglie.net/projects/debroglie/repository/entry/Oxford/trunk/diamond2crysalis/bitfield.F90
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <Python.h>
#include "cryio.h"
#include "agi_bitfield.h"


#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))


static void mvbits(int64_t *from, int64_t frompos, int64_t len, int64_t *to, int64_t topos) {
    int64_t oldbits, newbits, lenmask;

    lenmask = (len == sizeof(int64_t)*8) ? ~(int64_t)0 : (1 << len) - 1;
    newbits = ((*from >> frompos) & lenmask) << topos;
    oldbits = *to & (~(lenmask << topos));
    *to = newbits | oldbits;
}


static size_t packint(int32_t pixel, Py_ssize_t size, memptr *mem, int64_t *result) {
    memptr t;
    Py_ssize_t s;
    int8_t val;

    t = *mem;
    s = (Py_ssize_t)t._8;
    if (pixel >= -127 && pixel < 127) {
        val = pixel + (1 << (size - 1)) - 1;
        if (result == NULL)
            *t._8++ = val;
        else
            *result = val;
    } else if (pixel >= -32767 && pixel < 32767) {
        if (result == NULL)
            *t._8++ = 0xfe;
        else
            *result = 0xfe;
        *t._16++ = (int16_t)pixel;
    } else {
        if (result == NULL)
            *t._8++ = 0xff;
        else
            *result = 0xff;
        *t._32++ = pixel;
    }
    return (Py_ssize_t)(t._8 - s);
}


static int64_t packblock(int32_t block[8], Py_ssize_t size, int8_t *table, int8_t *index) {
    int64_t result, tmp;
    Py_ssize_t i;
    memptr t;

    result = 0;
    t._8 = table;
    for (i=0; i<8; ++i) {
        t._8 += packint(block[i], size, &t, &tmp);
        mvbits(&tmp, 0, size, &result, i*size);
    }
    *index = (int8_t)(t._8 - table);
    return result;
}


static int64_t bitsize(int64_t val) {
    int64_t result;

    if (val < -63)
        result = 8;
    else if (val < -31)
        result = 7;
    else if (val < -15)
        result = 6;
    else if (val < -7)
        result = 5;
    else if(val < -3)
        result = 4;
    else if(val < -1)
        result = 3;
    else if(val < 0)
        result = 2;
    else if(val < 2)
        result = 1;
    else if(val < 3)
        result = 2;
    else if(val < 5)
        result = 3;
    else if(val < 9)
        result = 4;
    else if(val < 17)
        result = 5;
    else if(val < 33)
        result = 6;
    else if(val < 65)
        result = 7;
    else
        result = 8;
    return result;
}


static void minmax(Py_ssize_t k, int32_t v1, int32_t v2, int32_t *min1, int32_t *max1, int32_t *min2, int32_t *max2) {
    if (k==0) {
        *min1 = v1;
        *max1 = v1;
        *min2 = v2;
        *max2 = v2;
    } else {
        if (v1 < *min1)
            *min1 = v1;
        if (v1 > *max1)
            *max1 = v1;
        if (v2 < *min2)
            *min2 = v2;
        if (v2 > *max2)
            *max2 = v2;
    }
}


static espdata *alloc_esp(Py_ssize_t dim) {
    espdata *esp;

    esp = (espdata *)malloc(sizeof(espdata));
    if (esp == NULL)
        return NULL;

    esp->dim = dim;
    esp->n_pixels = dim * dim;
    esp->mem = (int8_t *)malloc((esp->n_pixels + esp->dim + 1) * sizeof(int32_t));
    if (esp->mem == NULL) {
        _destroy_esp(esp);
        return NULL;
    }
    esp->addrs = (int32_t *)(esp->mem + esp->n_pixels * sizeof(int32_t));
    return esp;
}


espdata *encode_agi_bitfield(Py_buffer *buf) {
    Py_ssize_t i, j, k;
    int8_t of_table1[64], of_table2[64], index1, index2;
    int32_t block1[8], block2[8], size_packed, *addrs, min1, max1, min2, max2, *array;
    int64_t cf1, cf2, size1, size2, s_f;
    memptr t;
    espdata *esp;

    esp = alloc_esp(buf->shape[0]);
    if (esp == NULL)
        return NULL;

    size1 = 0; size2 = 0;
    t._8 = esp->mem + sizeof(int32_t); //offset for the size of the data
    addrs = esp->addrs;
    array = (int32_t *)buf->buf;

    *addrs++ = 0;
    for (i=0; i<esp->dim; ++i) {
        t._8 += packint(array[i*esp->dim], 8, &t, NULL);

        for (j=1; j<esp->dim-16; j+=16) {
            for (k=0; k<8; k++) {
                block1[k] = array[i*esp->dim+j+k] - array[i*esp->dim+j+k-1];
                block2[k] = array[i*esp->dim+j+k+8] - array[i*esp->dim+j+k+8-1];
                minmax(k, block1[k], block2[k], &min1, &max1, &min2, &max2);
            }

            size1 = MAX(bitsize(min1), bitsize(max1));
            size2 = MAX(bitsize(min2), bitsize(max2));

            s_f = 0;
            mvbits(&size1, 0, 4, &s_f, 0);
            mvbits(&size2, 0, 4, &s_f, 4);
            *t._8++ = (int8_t)s_f;

            cf1 = packblock(block1, size1, of_table1, &index1);
            memcpy(t._8, &cf1, size1);
            t._8 += size1;

            cf2 = packblock(block2, size2, of_table2, &index2);
            memcpy(t._8, &cf2, size2);
            t._8 += size2;

            memcpy(t._8, of_table1, index1);
            t._8 += index1;
            memcpy(t._8, of_table2, index2);
            t._8 += index2;
        }

        for (j=esp->dim-15; j<esp->dim; ++j)
            t._8 += packint(array[i*esp->dim+j]-array[i*esp->dim+j-1], 8, &t, NULL);
        *addrs++ = (int32_t)(t._8 - esp->mem - sizeof(int32_t));
    }
    memcpy(t._8, esp->addrs, (addrs - esp->addrs - 1) * sizeof(int32_t));
    t._32 += addrs - esp->addrs - 1;

    size_packed = (int32_t)(t._8 - esp->mem - (addrs - esp->addrs) * sizeof(int32_t));
    memcpy(esp->mem, &size_packed, sizeof(int32_t));
    esp->buf_size = t._8 - esp->mem;
    return esp;
}


void _destroy_esp(espdata *esp) {
    if (esp != NULL) {
        if (esp->mem != NULL)
            free(esp->mem);
        free(esp);
    }
}
