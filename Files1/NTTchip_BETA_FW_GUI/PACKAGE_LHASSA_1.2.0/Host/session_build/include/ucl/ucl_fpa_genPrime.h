/*============================================================================
 *
 *	ucl_fpa_genPrime.h
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright (c) 2002-2006 Innova Card.
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
#ifndef _UCL_FPA_GENPRIME_H_
#define _UCL_FPA_GENPRIME_H_


/*============================================================================*/
/** <b>Prime Generation using IEEE 1363 Annex A.16.11</b>.
 *
 * Generate a prime number @a p between @a pMax and @a pMin for which @p p-1
 * is relatively prime to @a f.
 *
 * @param[out]	prime	The prime
 * @param[in]	f 		A large number
 * @param[in]	pMin 	A large number
 * @param[in]	pMax 	A large number
 * @param[in]	t		Number of trials for Miller-Rabin Test
 * @param[in]	s 		The precision
 *
 * @ingroup UCL_FPA_PRIME
 */
int fpa_gen_prime(u32 *p, u32 *f, u32 *pMin, u32 *pMax, u32 s);


/*============================================================================*/
/** <b>RSA Paramaters Generation</b>.
 * Generate two primes @a p & @q and calculate @f$ n = p \times q@f$ .
 *
 * @param[out]	n	The pointer to @a n
 * @param[out]	d	The pointer to @a d
 * @param[in]	e	The pointer to @a e
 * @param[in]	t	The length of @p e
 * @param[in]	s	The precision
 *
 * @ingroup UCL_FPA_PRIME
 */
int ucl_rsa_param_gen(u32 *n, u32 *p, u32 *q, u32 *d, u32 *e,
	u32 t, u32 s);


/*============================================================================*/
/** <b>RSA CRT Parameters Generation</b>.
 * Generate two primes @a p & @q and calculate @f$ n = p \times q@f$ .
 *
 * @param[out]	n		The pointer to @a n
 * @param[out]	p		The pointer to @a p
 * @param[out]	q		The pointer to @a q
 * @param[out]	dp		The pointer to @a dp
 * @param[out]	dq		The pointer to @a dq
 * @param[in]	qInv	The pointer to @a qInv
 * @param[in]	e		The pointer to @a e
 * @param[in]	t		The length of @p e
 * @param[in]	s		The precision of @a n
 *
 * @ingroup UCL_FPA_PRIME
 */
int ucl_rsa_crt_param_gen(u32 *n,u32 *p, u32 *q, u32 *dp, u32 *dq,
	u32 *qInv, u32 *e, u32 t, u32 s);


#endif //_UCL_FPA_GENPRIME_H_
