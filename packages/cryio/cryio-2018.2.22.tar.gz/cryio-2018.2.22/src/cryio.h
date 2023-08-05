#ifndef CRYIO_CRYIO_H_   /* Include guard */
#define CRYIO_CRYIO_H_ 1

#include <stdint.h>


typedef union {
    int8_t  *_8;
    int16_t *_16;
    int32_t *_32;
    int64_t *_64;
} memptr;


#endif  //
