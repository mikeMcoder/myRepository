/*============================================================================
 *
 * umpa.h
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
#ifndef _UMPA_H_
#define _UMPA_H_

/* ========================================================================== */
/** <b>Multiple-Precision Unsigned Multiplication</b>.
 * @f$ w = x \times y @f$
 *
 * Let @a x be an unsigned large number of precision @p sX @n
 * Let @a y be an unsigned large number of precision @p sY @n
 *
 * @pre @f$ sW \geq sX + sY @f$
 *
 * @param[out] w Pointer to the result of the multiplication
 * @param[in] x Pointer to @a x
 * @param[in] sX The length of @a x
 * @param[in] y Pointer to @a y
 * @param[in] sY The length of @a y
 *
 * @ingroup MPA
 */
void umpa_mult(u32 *w, u32 *x, u32 sX, u32 *y, u32 sY);


#endif //_UMPA_H_
