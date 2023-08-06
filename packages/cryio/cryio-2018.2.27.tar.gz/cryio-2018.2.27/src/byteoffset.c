#include <stdlib.h>
#include <stdint.h>
#include "cryio.h"
#include "byteoffset.h"


void decode_byte_offset(void *in, int size, void *out) {
    int8_t delta8;
    int16_t delta16;
    int32_t pixel = 0, *array;
    int i;
    char *ain = (char *)in;

    array = (int32_t *)out;
    for (i=0; i<size; i++) {
        delta8 = *(int8_t *)ain;
        ain += sizeof(int8_t);
        if ((delta8 & 0xff) == 0x80) {
            delta16 = *(int16_t *)ain;
            ain += sizeof(int16_t);
            if ((delta16 & 0xffff) == 0x8000) {
                pixel += *(int32_t *)ain;
                ain += sizeof(int32_t);
            } else {
                pixel += delta16;
            }
        } else {
            pixel += delta8;
        }
        array[i] = pixel;
    }
}

int32_t *_decode_byte_offset(void *buf, int size)
{
    void *array;

    array = malloc(size * sizeof(int32_t));
    if (!array)
        return NULL;
    decode_byte_offset(buf, size, array);
    return (int32_t *)array;
}


cbfpacked *_encode_byte_offset(void *buf, int len, int size) {
    int i;
    int32_t diff, nval, cval = 0, adiff, *array;
    memptr t;
    cbfpacked *cbf;

    /* if we have an array where every number is bigger than the max int16 = 0x7fff
     * then we need 3 bytes for the overflow and 4 bytes for a number,
     * i.e. an array value of 0x8001 gives the following "packed" byte sequence:
     *   0x80   0x00 0x80   0x01 0x80
     *   ^^^^   ^^^^^^^^^   ^^^^^^^^^
     *   8bit     16bit       32bit
     * overflow  overflow   our value
     * it is not really a packing, but we have to be prepared for a possible memory
     * corruption in this case, thus maximum amount of memory we need is
     * array_size * sizeof(int32) + array_size * 3 additional bytes
     * i.e len + len - array_size = len + len * 3 / 4
     */
    cbf = malloc(sizeof(cbfpacked) + (int)(len * 1.75));
    if (!cbf)
        return NULL;

    cbf->data = (char *)(cbf + 1);
    array = (int32_t *)buf;
    t._8 = (int8_t *)cbf->data;
    for (i=0; i<size; i++) {
        nval = array[i];
        diff = nval - cval;
        adiff = abs(diff);
        if (adiff < 0x80) {
            *t._8++ = (int8_t)diff;
        } else {
            *t._8++ = 0x80;
            if (adiff < 0x8000) {
                *t._16++ = (int16_t)diff;
            } else {
                *t._16++ = 0x8000;
                *t._32++ = diff;
            }
        }
        cval = nval;
    }
    cbf->len = (int)((char *)t._8 - cbf->data);
    return cbf;
}


void destroy_cbfpacked(cbfpacked *cbfp) {
    if (cbfp != NULL)
        free(cbfp);
}
