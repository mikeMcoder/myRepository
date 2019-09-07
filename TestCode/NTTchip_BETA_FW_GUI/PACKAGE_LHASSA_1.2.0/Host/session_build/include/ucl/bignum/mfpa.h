/*============================================================================
 *
 * bignum/mfpa.h
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright © 2009 Innova Card.
 * All Rights Reserved. Do not disclose.
 *
 * This software is the confidential and proprietary information of
 * Innova Card ("Confidential Information"). You shall not
 * disclose such Confidential Information and shall use it only in
 * accordance with the terms of the license agreement you entered
 * into with Innova Card.
 *
 * Innova Card makes no representations or warranties about the suitability of
 * the software, either express or implied, including but not limited to
 * the implied warranties of merchantability, fitness for a particular purpose,
 * or non-infrigement. Innova Card shall not be liable for any damages suffered
 * by licensee as the result of using, modifying or distributing this software
 * or its derivatives.
 *
 *==========================================================================*/
/*============================================================================
 *
 * Purpose :
 *
 *==========================================================================*/
#ifndef _BIGNUM_MFPA_H_
# define _BIGNUM_MFPA_H_

#include "defs.h"

/**
 */
typedef struct mfpa_ctx
{
    u32 *n;
    u32 *r;
    u32 *rs;
    u32 *g;
    u32 np;
    u32 s;
} mfpa_ctx_t;


/* ========================================================================== */
/** <b>MFPA Precalculation</b>.
 *
 * @param[in,out] ctx Pointer to the context
 *
 * @return Error code
 *
 * @retval #UCL_OK if no error occurred
 *
 * @ingroup UCL_MFPA
 */
int mfpa_init(mfpa_ctx_t *ctx);


/*============================================================================*/
/** <b>Modular Multiplication</b>.
 *
 * @param[out] w Pointer to the result
 * @param[in]  x Pointer to @a x
 * @param[in]  y Pointer to @a y
 * @param[in] ctx Pointer to the MFPA context
 *
 * @return Error code
 *
 * @retval #UCL_OK No error occurred
 *
 * @ingroup UCL_MFPA
 */
int mfpa_mult(u32 *w, u32 *x, u32 *y, mfpa_ctx_t *ctx);


/*============================================================================*/
/** <b>Modular Square</b>.
 *
 * @f$ w = x^2 \bmod n @f$
 *
 * @param[out] w Pointer to the result
 * @param[in]  x Pointer to @a x
 * @param[in] ctx Pointer to the MFPA Context
 *
 * @return Error code
 *
 * @retval #UCL_OK No error occurred
 *
 * @ingroup UCL_MFPA
 */
int mfpa_sqr(u32 *w, u32 *x, mfpa_ctx_t *ctx);


/* ========================================================================== */
/** <b>Modular Exponentiation</b>.
 *
 * Let @a x, @a n and @a e be unsigned large numbers.@n
 * Let @a s the precision.@n
 * @n
 * If preconditions are satisfied then @n
 * @f$ w = x^e \bmod n @f$
 *
 * @pre @f$ x < n @f$
 *
 * @param[out] w Pointer to the result
 * @param[in]  x Pointer to an unsigned large number @a x
 * @param[in]  e Pointer to an unsigned large number @a e
 * @param[in] n Pointer to an unsigned large number @a n
 * @param[in] s The precision
 *
 * @retval #UCL_OK     if no error occurred
 *
 * @ingroup UCL_MFPA
 */
int mfpa_exp(u32 *w, u32 *x, u32 *e, mfpa_ctx_t *ctx);


/* ========================================================================== */
/** <b>FBEM Modular Exponentiation Precalculation</b>.
 *
 * @param[in,out] ctx Pointer to the context
 * @param[in]   g Pointer to the base
 *
 * @return Error code
 *
 * @retval #UCL_OK if no error occurred
 *
 * @ingroup UCL_MFPA
 */
int mfpa_exp_fbem_init(mfpa_ctx_t *ctx, u32 *g);

/* ========================================================================== */
/** <b>FBEM Modular Exponentiation Precalculation</b>.
 *
 * Let @a g and @a e be unsigned large numbers. @n
 * @f$ w = g^e \bmod n @f$ @n
 * where
 *
 * @param[out] w Pointer to the result
 * @param[out] g Pointer to @a g
 * @param[out] e Pointer to @a e
 * @param[in]  ctx Pointer to the context
 *
 * @return Error code
 *
 * @retval #UCL_OK if no error occurred
 *
 * @ingroup UCL_MFPA
 */
//int __nomips16__ mfpa_exp_fbem(u32 *w, u32 *g, u32 *e, mfpa_ctx_t *mfpa_ctx);
int mfpa_exp_fbem(u32 *w, u32 *g, u32 *e, mfpa_ctx_t *mfpa_ctx);


/* ========================================================================== */
/** <b>Reduction of unsigned large number</b>.
 * @f$ r = x \bmod n @f$
 *
 * @pre the precision of @a x is @a 2s
 *
 * @param[out] r Pointer to the result
 * @param[in]  x Pointer to @a x
 * @param[in] n Pointer to @a n
 * @param[in] s The precision
 *
 * @retval #OK No error occurred
 *
 * @ingroup MFPA
 */
int mfpa_red(u32 *r, u32 *x, u32 *n, u32 s);


/* ========================================================================== */
/** <b>Modular Exponentiation</b>.
 *
 * Let @a x and @a n be unsigned large numbers.@n
 * Let @a e a 32-bits unsigned integer.@n
 * Let @a s the precision.@n
 *  @n
 * If preconditions are satisfied then @n
 * @f$ w = x^e \bmod n @f$
 *
 * @pre @f$ x < n @f$
 *
 * @param[out]  w   Pointer to the result
 * @param[in]   x   Pointer to an unsigned large number @a x
 * @param[in]   e   Pointer to an unsigned large number @a e
 * @param[in]   n   Pointer to an unsigned large number @a n
 * @param[in]   s   The precision
 *
 * @return  Error code
 *
 * @retval #UCL_OK                  No error occurred
 * @retval #UCL_INVALID_OUTPUT      @p w is the pointer NULL
 * @retval #UCL_INVALID_INPUT       @p x, @p n or @p e is the pointer NULL
 * @retval #UCL_INVALID_PRECISION   Invalid precision
 *
 * @ingroup UCL_MFPA
 */
int mfpa_exp_w32(u32 *w, u32 *x, u32 e, mfpa_ctx_t *ctx);

void mfpa_div2(u32 *x, u32 *q, u32 s);
int mfpa_mult_noctx(u32 *w, u32 *x, u32 *y, u32 *n, u32 s);

#endif //_BIGNUM_MFPA_H_
