/*============================================================================
 *
 * bignum/fpa.h
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
 * Purpose : Fixed-Precision Primary Operations
 *
 *==========================================================================*/
#ifndef _BIGNUM_FPA_H_
#define _BIGNUM_FPA_H_


/*============================================================================*/
/** <b>Large integer copy</b>.
 * @f$ w = x @f$
 *
 * @param[out] w Pointer to @a w
 * @param[in] x Pointer to @a x
 * @param[in] s The precision
 *
 * @ingroup FPA
 */
int fpa_cpy(u32 *w, u32 *x, u32 s);


/*============================================================================*/
/** Large integer incrementation.
 * @f$ w = w + 1 @f$
 *
 * @param[in,out] w Pointer to @a w
 * @param[in]  s The precision
 *
 * @return Carry
 *
 * @ingroup FPA
 */
int fpa_inc(u32 *w, u32 s);


/*============================================================================*/
/** Addition of large integer.
 * @f$ w = x + y @f$
 *
 * @param[out] w Pointer to the result of the addition
 * @param[in] x Pointer to @a x
 * @param[in] y Pointer to @a y
 * @param[in] s The precision
 *
 * @return Carry
 *
 * @ingroup FPA
 */
int fpa_add(u32 *w, u32 *x, u32 *y, u32 s);


/*============================================================================*/
/** Substraction of large integer.
 * @f$ w = x - y @f$
 *
 * @param[out] w Pointer to the result of the substraction
 * @param[in] x Pointer to @a x
 * @param[in] y Pointer to @a y
 * @param[in] s The precision
 *
 * @return Carry
 *
 * @ingroup FPA
 */
int fpa_sub(u32 *w, u32 *x, u32 *y, u32 s);


#endif // _BIGNUM_FPA_H_
