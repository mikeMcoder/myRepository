/*============================================================================
 *
 * monty.h
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
 * Purpose : Montgomery Product and associated functions.
 *
 *==========================================================================*/
#ifndef _MONTY_H_
#define _MONTY_H_


/** @internal
 * @defgroup MONTY Montgomery Product
 * Montgomery Product and its applications.
 *
 * @ingroup BIGNUM
 */


/* ========================================================================== */
/** <b>Montgomery Product</b>.
 * Let @a x , @a y and @a n be large numbers @n
 * Let @a s the precision @n
 * Let @a r, @a r' and @a n' such as @n
 * @f$ r = (2^{32})^s @f$ @n
 * @f$ r' \times r - n' \times n = \gcd(n,r) = 1 @f$
 * @n
 * If preconditions are satisfied then @n
 * @f$ x = x \times y \times r^{-1} mod\ n @f$
 *
 * @param[in, out] x The pointer to @a x, replaced by the result of the
 *       product
 * @param[in]   y The pointer to @a y
 * @param[in]  n The pointer to @a n
 * @param[in]  s The precision
 * @param[in]  np The first word of @a n'
 *
 * @warning No management of error
 *
 * @ingroup MONTY
 */
void monty_prod(u32 *x, u32 *y, u32 *n, u32 s, u32 np);


/* ========================================================================== */
/* <b>Montgomery inversion</b>.
 * Return @f$ w = a^-1.r \bmod p @f$.
 *
 * @param[out] w    @p w
 * @param[in]  x    @p x
 * @param[in]  p    @p p
 * @param[in]  s    @p s
 * @param[in]  np   @p np
 * @param[in]  rSqr @p rSqr
 *
 * @return Error code
 *
 * @retval #UCL_INVALID_INPUT
 * @retval #UCL_STACK_ERROR
 * @retval #UCL_OK
 *
 * @ingroup MONTY
 * @internal
 */

int monty_inv(u32 *w, const u32 *x, const u32 *p, u32 s, u32 np,
              const u32 *rSqr);


/* ========================================================================== */
/** <b>Montgomery Exponentiation [Sliding Window - @f$(M, M^3)@f$ method]</b>.
 * @f$ (M, M^3)\ method@f$ @n
 * Let @a x and @a e be large numbers @n
 * Let @a s the precision @n
 * Let @a lenE the precision of @a e @n
 * Let @a r and @a rSqr such as @n
 * @f$ r = (2^{32})^s \bmod n @f$ @n
 * @f$ rSqr = r^2 \bmod n @f$ @n
 * @n
 * If preconditions are satisfied then @n
 * @f$ x = x^e \bmod n @f$
 *
 * @param[out] w The pointer to @a w, the result of the exponentiation
 * @param[in] x The pointer to @a x
 * @param[in] e The pointer to @a e
 * @param[in] rSqr The pointer to @f$ r^{2}\ \bmod n @f$
 * @param[in] r The pointer to @f$ r\ \bmod n @f$
 * @param[in] n The pointer to @a n
 * @param[in] np The first word of @a n'
 * @param[in] s The precision
 * @param[in] lenE The precision of @a e
 *
 * @warning No management of error
 *
 * @ingroup MONTY
 */
int monty_expMM3(u32 *w, u32 *x, u32 *e, u32 *rSqr, u32 *r, u32 *n, u32 np, u32 s, u32 lenE);


/* ========================================================================== */
/** <b>Calculate and return n0'</b>.
 * @f$ x = r \times r' - n \times n' = \gcd(r, n) = 1 @f$ @n
 * @f$ r' = r^{-1} \bmod n@f$ @n
 *
 * @param[in] n0 The value of @a n0
 *
 * @return The least significant word of @a n'
 *
 * @ingroup MONTY
 */
u32 monty_calcNp(u32 n0);


/* ========================================================================== */
/** <b>Initialisation for montgomery exponentiation</b>.
 * @f$ r = (2^{32})^s \ mod\ n @f$ @n
 * @f$ rSqr = r^2 \ mod\ n @f$
 *
 * @param[out] r  The pointer to @a r
 * @param[out] rSqr The pointer to @a rSqr
 * @param[in] n  The pointer to @a n
 * @param[in]  s  The precision
 *
 * @return Error code
 *
 * @ingroup MONTY
 */
int monty_initR(u32 *r, u32 *rSqr, u32 *n, u32 s);


#endif //_MONTY_H_
