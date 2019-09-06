/*===========================================================================
 *
 * ucl_ecdsa.h
 *
 *==========================================================================*/
/*===========================================================================
 *
 * Copyright (c) 2002-2007 Innova Card. All Rights Reserved. Do not disclose.
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
/*===========================================================================
 *
 * Purpose: Elliptic Curve Digital Signature Algorithm
 *
 *==========================================================================*/
#ifndef UCL_ECDSA_H_
#define UCL_ECDSA_H_

#ifdef _cplusplus
extern "C"
{
#endif /* _ cplusplus  */


/* ========================================================================== */

    
#define SIZEOF_ECDSA_BUFFER(s) (sizeof(ucl_ecc_curve_st) + (7*(s)*4) + \
                                    sizeof(ucl_ecc_point_st))


/* ========================================================================== */


/** <b>Elliptic Curve Domain Parameters</b>.
 * Octect strings.
 * @see X9.62
 * @ingroup UCL_ECDSA */
struct ucl_ecdsa_domain_s {
    u8 *q;      /**< q                                   */
    u8 *seed;   /**< Seed                                */
    u8 *a;      /**< a                                   */
    u8 *b;      /**< b                                   */
    u8 *G;      /**< Base point                          */
    u32 glen;   /**< Size of the base point octet string */
    u8 *n;      /**< Order                               */
    u8 *h;      /**< Cofactor                            */
    u32 type;   /**< Curve type                          */
    u32 field;  /**< Field type                          */
    u32 bsize;  /**< bit size of field element           */
};

/** Type EC Domain Parameters.
 * @ingroup UCL_ECDSA */
typedef struct ucl_ecdsa_domain_s ucl_ecdsa_domain_st;

/** <b>ECDSA Signature</b>.
 * Octect strings.
 * @see X9.62
 * @ingroup UCL_ECDSA */
struct ucl_ecdsa_signature_s {
    u8 *r; /**< */
    u8 *s; /**< */
};

/** Type ECDSA Signature.
 * @ingroup UCL_ECDSA */
typedef struct ucl_ecdsa_signature_s ucl_ecdsa_signature_st;

/** <b>ECDSA Public Key </b>.
 * Octect strings.
 * @see X9.62
 * @ingroup UCL_ECDSA */
typedef unsigned char ucl_ecdsa_pubkey_t;

/** <b>ECDSA Private Key </b>.
 * Octect strings.
 * @see X9.62
 * @ingroup UCL_ECDSA */
typedef unsigned char ucl_ecdsa_prkey_t;

/* ========================================================================== */


/** <b>Valid EC Domain Parameters</b>.
 * 
 * @param[in]   domain  EC Domain parameters
 * 
 * @return Error code
 * 
 * @retval #UCL_OK      Domain is valid
 * @retval #UCL_ERROR   Domain is unvalid
 * 
 * @ingroup UCL_ECDSA */
int __API__ ucl_ecdsa_valid_domain(ucl_ecdsa_domain_st *domain);


/** <b>Initialize context buffer</b>.
 * Initialize a context for ECC computation.
 * If initialization successes @p *ctx = @p buffer.
 * 
 * @param[out]  ctx     Context buffer
 * @param[in]   domain  EC Domain parameters
 * @param[in]   options Options
 * @param[in]   buffer  Work buffer
 * @param[in]   len     Buffer length
 * 
 * @return Error code
 * 
 * @retval #UCL_OK No error occurred
 * 
 * @ingroup UCL_ECDSA */
int __API__ ucl_ecdsa_init(void **ctx, const ucl_ecdsa_domain_st *domain, 
        u32 options, u8 *buffer, u32 len);


/** <b>ECDSA Key Generation</b>.
 * Generate a private and a public key for the domain.
 * 
 * @pre The context must initialized first.
 * 
 * @param[out] pubkey  The public key (octet string)
 * @param[in]  publen  Size of @p pubkey
 * @param[out] prkey   The private key (octet string)
 * @param[in]  prlen   Size of @p prkey
 * @param[in]  opt     Point representation option:
 *                         @li #UCL_ECC_POINT_OS_COMP
 *                         @li #UCL_ECC_POINT_OS_UNCOMP
 *                         @li #UCL_ECC_POINT_OS_HYBRID
 * @param[in]  ctx     Context
 * 
 * @return Error code
 * 
 * @retval #UCL_OK No error occurred
 * 
 * @ingroup UCL_ECDSA */
int __API__ ucl_ecdsa_keygen(ucl_ecdsa_pubkey_t *pubkey, u32 publen, 
        ucl_ecdsa_prkey_t *prkey, u32 prlen, int opt, void *ctx);


/** <b>ECDSA Signature Generation</b>.
 * Generate an ECDSA signature.
 * 
 * @pre The context must initialized first.
 * 
 * @param[out] signature Signature
 * @param[in]  message   Message
 * @param[in]  len       Message length
 * @param[in]  key       ECDSA Private Key
 * @param[in]  klen      Key byte length
 * @param[in]  ctx       Context buffer
 * 
 * @return Error code
 * 
 * @retval #UCL_OK              No error occurred
 * @retval #UCL_ECC_CTX_ERROR   Context invalid
 * 
 * @ingroup UCL_ECDSA */
int __API__ ucl_ecdsa_sign(ucl_ecdsa_signature_st *signature, const u8 *message,
        u32 len, const ucl_ecdsa_prkey_t *key, u32 klen, void *ctx);


/** <b>ECDSA Signature Verification</b>.
 * 
 * @pre The context must initialized first.
 *
 * @param[in] signature Signature
 * @param[in] message   Message
 * @param[in] len       Message length
 * @param[in] key       ECDSA Private Key
 * @param[in] klen      Key byte length
 * @param[in] ctx       Context buffer
 * 
 * @return Error code
 * 
 * @retval #UCL_OK              No error occurred
 * @retval #UCL_ECC_CTX_ERROR   Context invalid
 * 
 * @ingroup UCL_ECDSA */
int __API__ ucl_ecdsa_verify(const ucl_ecdsa_signature_st *signature,
        const u8 *message, u32 len, const ucl_ecdsa_pubkey_t *key, u32 klen,
        void *ctx);


/* ========================================================================== */

#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /*UCL_ECDSA_H_*/
