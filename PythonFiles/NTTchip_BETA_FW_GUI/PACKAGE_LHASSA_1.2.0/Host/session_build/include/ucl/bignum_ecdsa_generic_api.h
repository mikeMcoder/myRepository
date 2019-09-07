//#include <stdio.h>
//#include <stdlib.h>
#include <ucl/ucl_config.h>
#include <ucl/ucl_types.h>

#ifdef WORD32
/*#define DOUBLE_DIGIT unsigned long int
#define DIGIT unsigned short int
#define MAX_DIGIT 0xFFFF
#define HALF_DIGIT 0xFF
#define MAX_DIGITS 20
#define DIGIT_BITS 16*/
#define DOUBLE_DIGIT unsigned long long int
#define DIGIT u32
#define MAX_DIGIT 0xFFFFFFFF
#define HALF_DIGIT 0xFFFF
//move from 16 to 17 then 33 for dsa use of bignum_mod
#define MAX_DIGITS 65
#define DIGIT_BITS 32
#endif//WORD32
#ifdef WORD16
#define DOUBLE_DIGIT unsigned long int
#define DIGIT unsigned short int
#define MAX_DIGIT 0xFFFF
#define HALF_DIGIT 0xFF
#define MAX_DIGITS 16
#define DIGIT_BITS 16
#endif//WORD16

/* Length of digit in bytes */
#define DIGIT_LEN (DIGIT_BITS / 8)

void __API__ bignum_modsquare(DIGIT *r,DIGIT *a,DIGIT *m,DIGIT k);
void __API__ bignum_modmult(DIGIT *r,DIGIT *a,DIGIT *b,DIGIT *m,DIGIT k);
void __API__ bignum_d2us(u8 *a,DIGIT  len,DIGIT *b,DIGIT digits);
void __API__ bignum_us2d(DIGIT *a,DIGIT digits,u8 *b,DIGIT len);
int __API__ bignum_cmp(DIGIT *a,DIGIT *b,DIGIT s);
int __API__ bignum_isnul(DIGIT *A,DIGIT tA);
DIGIT __API__ bignum_digits(DIGIT *N,DIGIT tn);
DIGIT __API__ bignum_digitbits(DIGIT a);
void __API__ bignum_copydigit(DIGIT *E,DIGIT F,DIGIT tE);
void __API__ bignum_copyzero(DIGIT *E,DIGIT tE);
void __API__ bignum_copy(DIGIT *E,DIGIT *F,DIGIT tE);

DIGIT __API__ bignum_add(DIGIT *w,DIGIT *x,DIGIT *y,DIGIT digits);
DIGIT __API__ bignum_sub(DIGIT *w,DIGIT *x,DIGIT *y,DIGIT digits);
void __API__ bignum_mult(DIGIT *t,DIGIT *a,DIGIT *b,DIGIT n);
void __API__ bignum_mult_operand_scanning_form(DIGIT *t,DIGIT *a,DIGIT *b,DIGIT n);
void __API__ bignum_multopt(DIGIT *t,DIGIT *a,DIGIT *b,DIGIT n);
void __API__ bignum_multlimited(DIGIT *t,DIGIT *a,DIGIT *b,DIGIT n);
void __API__ bignum_multscalar(DIGIT *t,DIGIT a,DIGIT *b,DIGIT n);
void __API__ bignum_mult2sizes(DIGIT *t,DIGIT *a,DIGIT na,DIGIT *b,DIGIT nb);
void __API__ bignum_square(DIGIT *a,DIGIT *b,DIGIT digits);
DIGIT __API__ bignum_leftshift(DIGIT *a,DIGIT *b,DIGIT c,DIGIT digits);
DIGIT __API__ bignum_rightshift(DIGIT *a,DIGIT *b,DIGIT c,DIGIT digits);

void __API__ bignum_modinv(DIGIT *x,DIGIT *a0,DIGIT *b0,unsigned int digits);
void __API__ bignum_modinv_subs(DIGIT *x,DIGIT *a0,DIGIT *b0,unsigned int digits);
void __API__ bignum_modinv3(DIGIT *x,DIGIT *a0,DIGIT *b0,unsigned int digits);
void __API__ bignum_modinv4(DIGIT *x,DIGIT *a0,DIGIT *b0,unsigned int digits);
void __API__ bignum_modadd(DIGIT *r,DIGIT *a,DIGIT *b,DIGIT *m,DIGIT k);
void __API__ bignum_modexp(DIGIT *r,DIGIT *a,DIGIT *b,DIGIT *m,DIGIT k);
void __API__ bignum_mod(DIGIT *b,DIGIT *c,DIGIT cDigits,DIGIT *d,DIGIT dDigits);
void __API__ bignum_div(DIGIT *rmd,DIGIT *b,DIGIT *c,DIGIT cDigits,DIGIT *d,DIGIT dDigits);
void __API__ bignum_modmult(DIGIT *r,DIGIT *a,DIGIT *b,DIGIT *m,DIGIT k);
void __API__ bignum_modmult_maa(u32 segR, u32 segA,u32 segB,DIGIT k);
void __API__ bignum_modsquare(DIGIT *r,DIGIT *a,DIGIT *m,DIGIT k);
void __API__ bignum_modsquare_maa(u32 segR, u32 segB,DIGIT k);
void __API__ bignum_modsquaremult_maa(u32 segR, u32 segA,u32 segB,DIGIT k);

void load_maa(u32 seg,DIGIT *a,DIGIT k);
void load_modulus_maa(DIGIT *m,DIGIT k);
void unload_maa(u32 seg,DIGIT *r,DIGIT k);

unsigned long fastmul16(unsigned short a, unsigned short b);
unsigned short fastshr16(unsigned long);

