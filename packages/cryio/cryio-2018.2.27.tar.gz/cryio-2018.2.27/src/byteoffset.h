#ifndef CRYIO_BYTEOFFSET_H_   /* Include guard */
#define CRYIO_BYTEOFFSET_H_

#include <stdint.h>

typedef struct {
    char *data;
    int  len;
} cbfpacked;

void decode_byte_offset(void *in, int size, void *out);
int32_t *_decode_byte_offset(void *buf, int size);
cbfpacked *_encode_byte_offset(void *buf, int len, int size);
void destroy_cbfpacked(cbfpacked *cbfp);

#endif  // CRYIO_BYTEOFFSET_H_
