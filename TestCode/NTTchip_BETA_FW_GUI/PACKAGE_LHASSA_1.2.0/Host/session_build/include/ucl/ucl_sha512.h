#if !defined( _sha512a_h )
#define _sha512a_h

//#define u8 unsigned char
//#define u32 unsigned long

typedef struct {
      u32 H[ 16 ];
      u32 hbits, lbits;
      u8 M[ 256 ];
      u32 mlen;
} SHA512_ctx;

void SHA512_init ( SHA512_ctx* );
void SHA512_update( SHA512_ctx*, const void*, u32 );
void SHA512_final ( SHA512_ctx* );
void SHA512_digest( SHA512_ctx*, u8* );

#endif 
