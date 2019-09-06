/*============================================================================
 *
 * rsa.h
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
 * Purpose : RSA
 *
 *==========================================================================*/
#ifndef _RSA_H_
#define _RSA_H_

#include <ucl/ucl_rsa.h>


struct rsa_public_ctx
{
    /** The public exponent @p e. */
    u8 e[UCL_RSA_PUBLIC_EXPONENT_MAXSIZE];
    /** The modulus @p n. */
    u8 n[UCL_RSA_KEY_MAXSIZE];
    /** The modulus byte length. */
    u32 s;
    /** The public exponent byte length. */
    u32 sE;
};


struct rsa_private_ctx
{
    /** The private exponent @p d. */
    u8 d[UCL_RSA_KEY_MAXSIZE];
    /** The modulus @p n. */
    u8 n[UCL_RSA_KEY_MAXSIZE];
    /** The modulus byte length. */
    u32 s;
};

struct rsa_crt_ctx
{
    /** @f$ d_p = d \bmod (p-1) @f$. */
    u8 dp[UCL_RSA_KEY_MAXSIZE/2];
    /** @f$ d_q = d \bmod (q-1) @f$. */
    u8 dq[UCL_RSA_KEY_MAXSIZE/2];
    /** @a p. */
    u8 p[UCL_RSA_KEY_MAXSIZE/2];
    /** @a q. */
    u8 q[UCL_RSA_KEY_MAXSIZE/2];
    /** @f$ q^{-1} \bmod p @f$ */
    u8 qInv[UCL_RSA_KEY_MAXSIZE/2];
    /** The public exponent @p e. */
    u8 e[UCL_RSA_PUBLIC_EXPONENT_MAXSIZE];
    /** The public exponent byte length. */
    u32 sE;
    /** The modulus byte length. */
    u32 s;
};

int ucl_rsa_decrypt(u32 *dst, u32 *src, const struct rsa_public_ctx *key);

int ucl_rsa_crt_decrypt(u32 *dst, u32 *src, const struct rsa_crt_ctx *key);

int ucl_rsa_encrypt(u32 *dst, u32 *src, const struct rsa_private_ctx *key);


/*==============================================================================
 * RSA
 *============================================================================*/
/*============================================================================*/
/** <b>RSA Key max precision</b>.
 * @ingroup UCL_RSA
 */
#define UCL_RSA_KEY_MAXPRE (UCL_RSA_KEY_MAXSIZE/4)
/** <b>RSA Public exponent max precision</b>.
 * @ingroup UCL_RSA
 */
#define UCL_RSA_PUBLIC_EXPONENT_MAXPRE (UCL_RSA_PUBLIC_EXPONENT_MAXSIZE/4)


#endif /* _RSA_H_ */
