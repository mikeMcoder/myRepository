/*============================================================================
 *
 * ucl_rsa_genprime.h
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright (c) 2002-2007 Innova Card.
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
#ifndef UCL_RSA_GENPRIME_H_
#define UCL_RSA_GENPRIME_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/*============================================================================*/
/** <b>RSA Paramaters Generation</b>.
 * Generate two primes @a p & @q and calculate @f$ n = p \times q@f$ .
 *
 * @param[out] n The pointer to @a n
 * @param[out] d The pointer to @a d
 * @param[in]  e The pointer to @a e
 * @param[in]  t The length of @p e
 * @param[in]  s The precision
 *
 * @ingroup UCL_FPA_PRIME
 */
int __API__ ucl_rsa_param_gen(u32 *n, u32 *p, u32 *q, u32 *d, u32 *e,
                      u32 t, u32 s);


/*============================================================================*/
/** <b>RSA CRT Parameters Generation</b>.
 * Generate two primes @a p & @q and calculate @f$ n = p \times q@f$ .
 *
 * @param[out] n    The pointer to @a n
 * @param[out] p    The pointer to @a p
 * @param[out] q    The pointer to @a q
 * @param[out] dp   The pointer to @a dp
 * @param[out] dq   The pointer to @a dq
 * @param[in]  qInv The pointer to @a qInv
 * @param[in]  e    The pointer to @a e
 * @param[in]  t    The length of @p e
 * @param[in]  s    The precision of @a n
 *
 * @ingroup UCL_FPA_PRIME
 */
int __API__ ucl_rsa_crt_param_gen(u32 *n, u32 *p, u32 *q, u32 *dp, u32 *dq,
                          u32 *qInv, u32 *e, u32 t, u32 s);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /* UCL_RSA_GENPRIME_H_ */
