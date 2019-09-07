/*============================================================================
 *
 * ucl_rsa.h
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
 * Purpose : RSA
 *
 *==========================================================================*/
#ifndef _UCL_RSA_H_
#define _UCL_RSA_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/** @file ucl_rsa.h
 * @defgroup UCL_RSA RSA
 * The RSA cryptosystem.
 *
 * @par Header:
 * @link ucl_rsa.h ucl_rsa.h @endlink
 *
 * It named after its inventors R. Rivest, A. Shamir, and L. Adleman, is the
 * most widely used public-key cryptosystem. It may be used to provide both
 * secrecy and digital signatures and its security is based on the
 * dificulty of the integer factorization problem.@n
 * @n
 * <b>Principle:</b>@n
 * @n
 * Let @a e a small integer (in general @a 3 or @f$ 2^{16}+1 @f$), the public
 * exponent.@n
 * Let @f$ n = p \times q @f$, the modulus, such as @a p and @a q are two large primes, and
 * @f$ \gcd(\phi(n), e) = 1 @f$ where @f$ \phi(n) = (p-1) \times (q-1) @f$.@n
 * Let @f$ d = e^{-1} \mod \phi(n) @f$, the private exponent.@n
 * @n
 * (@a n, @a e) is named the public key and (@a n, @a d) the private key.@n
 * @n
 * Encryption/Decryption primitives:@n
 * If @f$ 0 < m < n @f$ is a message, then the ciphetext is @f$ c = m^e \mod n @f$
 * and @f$ m = c^d \mod n @f$.@n
 * @n
 * Signature/Verification primitives:@n
 * If @f$ 0 < m < n @f$ is a message, then the signature is @f$ S = m^d \mod n @f$ @n
 * To check a @a S' signature, calculate @f$ m' = S'^d \mod n @f$ and compare with @a m.@n
 * @n
 * <b>CRT</b>:
 * In order to speed up the RSA calculation, the CRT can be applied.@n
 * @n
 * @note This section contains the RSA primitives compliants with
 *    @ref PKCS1 "PKCS #1 V2.1".
 *
 * @ingroup UCL_PKC
 */


/** <b>RSA Public Key Structure</b>.
 * Let @f$ n = p \times q @f$ and @a e the public exponent.
 *
 * @ingroup UCL_RSA
 */

struct ucl_rsa_public_key
{
    /** The public exponent @p e. */
    u8 public_exponent[UCL_RSA_PUBLIC_EXPONENT_MAXSIZE];
    /** The modulus @p n. */
    u8 modulus[UCL_RSA_KEY_MAXSIZE];
    /** The modulus byte length. */
    u32 modulus_length;
    /** The public exponent byte length. */
    u32 public_exponent_length;
};


/** <b>RSA Public Key</b>.
 * @ingroup UCL_RSA
 */

typedef struct ucl_rsa_public_key ucl_rsa_public_key_t;


/** <b>RSA Private Key Structure</b>.
 * Let @f$ n = p \times q @f$ and @a d the private exponent.
 *
 * @ingroup UCL_RSA
 */

struct ucl_rsa_private_key
{
    /** The private exponent @p d. */
    u8 private_exponent[UCL_RSA_KEY_MAXSIZE];
    /** The modulus @p n. */
    u8 modulus[UCL_RSA_KEY_MAXSIZE];
    /** The modulus byte length. */
    u32 modulus_length;
};

/** <b>RSA Private Key</b>.
 * @ingroup UCL_RSA
 */

typedef struct ucl_rsa_private_key ucl_rsa_private_key_t;


/** <b>RSA CRT Private Key Structure</b>.
 *
 * Let @f$ n = p \times q @f$ and @a d the private exponent.
 * @ingroup UCL_RSA
 */

struct ucl_rsa_crt_private_key
{
    /** @f$ d_p = d \mod (p-1) @f$. */
    u8 exponent1[UCL_RSA_KEY_MAXSIZE/2];
    /** @f$ d_q = d \mod (q-1) @f$. */
    u8 exponent2[UCL_RSA_KEY_MAXSIZE/2];
    /** @a p. */
    u8 prime1[UCL_RSA_KEY_MAXSIZE/2];
    /** @a q. */
    u8 prime2[UCL_RSA_KEY_MAXSIZE/2];
    /** @f$ q^{-1} \mod p @f$ */
    u8 coefficient[UCL_RSA_KEY_MAXSIZE/2];
    /** The public exponent @p e. */
    u8 public_exponent[UCL_RSA_PUBLIC_EXPONENT_MAXSIZE];
    /** The public exponent byte length. */
    u32 public_exponent_length;
    /** The modulus byte length. */
    u32 modulus_length;
};

/** <b>RSA CRT Private Key</b>.
 *
 * @ingroup UCL_RSA
 */

typedef struct ucl_rsa_crt_private_key ucl_rsa_crt_private_key_t;


/* ========================================================================== */


/** <b>RSA Paramaters Generation</b>.
 * Generate @a p, @a q, @a n and @a d such as:@n
 * @f$ n = p \times q@f$ @n
 * @f$ e \times d = 1 \mod (p-1)(q-1)@f$ @n
 *
 * @param[out]  n   The pointer to @a n
 * @param[out]  p   The pointer to @a p
 * @param[out]  q   The pointer to @a q
 * @param[out]  d   The pointer to @a d
 * @param[in]   e   The pointer to @a e
 * @param[in]   t   The length of @p e
 * @param[in]   s   The precision
 *
 * @return Error code
 *
 * @retval #UCL_OK
 *
 * @ingroup UCL_RSA
 */
int __API__ ucl_rsa_param_gen(u32 *n, u32 *p, u32 *q, u32 *d, u32 *e, u32 t, u32 s);


/** <b> RSA CRT Paramaters Generation</b>.
 * Generate @a p, @a q, @a n , @a dp, @a dq and @a qInv such as: @n
 * @f$ n = p \times q@f$ @n
 * @f$ e \times dp = 1 \mod (p-1)@f$ @n
 * @f$ e \times dq = 1 \mod (q-1)@f$ @n
 * @f$ q \times qInv = 1 \mod p @f$ @n
 *
 * @param[out]  n       The pointer to @a n
 * @param[out]  p       The pointer to @a p
 * @param[out]  q       The pointer to @a q
 * @param[out]  dp      The pointer to @a dp
 * @param[out]  dq      The pointer to @a dp
 * @param[out]  qInv    The pointer to @a qInv
 * @param[in]   e       The pointer to @a e
 * @param[in]   t       The length of @p e
 * @param[in]   s       The precision
 *
 * @return Error code
 *
 * @retval #UCL_OK
 *
 * @ingroup UCL_RSA
 */
int __API__ ucl_rsa_crt_param_gen(u32 *n, u32 *p, u32 *q, u32 *dp, u32 *dq, u32 *qInv,
                          u32 *e, u32 t, u32 s);


/*============================================================================*/
/** <b>RSA Primitive - Decryption</b>.
 * It's equivalent to generate a signature.
 *
 * @param[out] dst The result of decryption
 * @param[in] src The ciphertext
 * @param[in] d Private exponent
 * @param[in] n The modulus
 * @param[in] s The precision
 *
 * @return Error code
 *
 * @retval #UCL_OK     if no error occurred
 * @retval #UCL_INVALID_OUTPUT  if the output is the pointer #NULL
 * @retval #UCL_INVALID_INPUT  if one of the input is the pointer #NULL
 * @retval #UCL_INVALID_PRECISION if @p s is out of range
 * @retval #UCL_RSA_INVALID_INPUT if @f$ src > n @f$
 *
 * @note This primitive is compliant with RSADP and RSAVP1 from @ref PKCS1
 *    "PKCS #1 V2.1"
 *
 * @ingroup UCL_RSA
 */
int __API__ ucl_rsa_decryptBlock(u32 *dst, u32 *src, u32 *d, u32 *n, u32 s);


/*============================================================================*/
/** <b>RSA Primitive - Decryption with CRT</b>.
 * It's equivalent to generate a signature.
 *
 * @param[out] dst  The result of decryption
 * @param[in] src  The ciphertext
 * @param[in] dp  Private exponent 1
 * @param[in] dq  Private exponent 2
 * @param[in] p  Private factor 1
 * @param[in] q  Private factor 2
 * @param[in] qInv Inverse of q mod p
 * @param[in] e  Public exponent
 * @param[in] sE  Precision of the public exponent
 * @param[in] n  The modulus
 * @param[in] s  The precision
 *
 * @return Error code
 *
 * @retval #UCL_OK     if no error occurred
 * @retval #UCL_INVALID_OUTPUT  if the output is the pointer #NULL
 * @retval #UCL_INVALID_INPUT  if one of the input is the pointer #NULL
 * @retval #UCL_INVALID_PRECISION if @p s is out of range
 * @retval #UCL_RSA_INVALID_INPUT if @f$ input > n @f$
 *
 * @note This primitive is compliant with RSADP and RSAVP1 from @ref PKCS1
 *    "PKCS #1 V2.1"
 *
 * @ingroup UCL_RSA
 */
int __API__ ucl_rsa_crt_decryptBlock(u32 *dst, u32 *src, u32 *dp, u32 *dq, u32 *p,
                             u32 *q, u32 *qInv, u32 *e, u32 sE, u32 *n, u32 s);


/*============================================================================*/
/** <b>RSA Primitive - Encryption</b>.
 * It's equivalent to check a signature.
 *
 * @param[out] dst The result of encryption
 * @param[in] src The plaintext
 * @param[in] e Public exponent
 * @param[in] sE Precision of the public exponent
 * @param[in] n The modulus
 * @param[in] s The precision
 *
 * @return Error code
 *
 * @retval #UCL_OK     if no error occurred
 * @retval #UCL_INVALID_OUTPUT  if the output is the pointer #NULL
 * @retval #UCL_INVALID_INPUT  if one of the input is the pointer #NULL
 * @retval #UCL_INVALID_PRECISION if @p s or @p sE is out of range
 * @retval #UCL_RSA_INVALID_INPUT if @f$ input > n @f$
 *
 * @note This primitive is compliant with RSAEP and RSASP1 from @ref PKCS1
 *    "PKCS #1 V2.1"
 *
 * @ingroup UCL_RSA
 */
int __API__ ucl_rsa_encryptBlock(u32 *dst, u32 *src, u32 *e, u32 sE, u32 *n, u32 s);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /* _UCL_RSA_H_ */
