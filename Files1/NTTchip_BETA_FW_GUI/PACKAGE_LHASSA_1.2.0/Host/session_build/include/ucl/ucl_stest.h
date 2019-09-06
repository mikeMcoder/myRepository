/*===========================================================================
 *
 *  ucl_stest.h
 *
 *==========================================================================*/
/*===========================================================================
 *
 * Copyright (c) 2002-2007 Innova Card.
 * All Rights Reserved.
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
 * Purpose:
 *
 *==========================================================================*/
#ifndef UCL_STEST_H_
#define UCL_STEST_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/** @file ucl_stest.h
 * @defgroup UCL_STEST Self Tests
 * Integrity Tests.
 *
 * @par Header:
 * @link ucl_stest.h ucl_stest.h @endlink
 *
 * This module provides functions to test UCL primitives.
 * Those functions must be used in the case of self tests are necessary.
 *
 * @ingroup UCL_MISC
 */


/** <b>DES Primitive self test</b>.
 * Test DES.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_cipher_des_stest(void);


/** <b>3DES Primitive self test</b>.
 * Test 3DES.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_cipher_3des_stest(void);


/** <b>AES Primitive self test</b>.
 * Test AES 128/192/256 bits key length.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_cipher_aes_stest(void);


/* ========================================================================== */

/** <b>RSA Primitive self test</b>.
 * Test RSA encryption, decryption and CRT decryption.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_pkc_rsa_stest(void);


/* ========================================================================== */


/** <b>HDES self test</b>.
 * Test HDES hash function.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_hash_hdes_stest(void);


/** <b>SHA256 self test</b>.
 * Test SHA256 hash function.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_hash_sha256_stest(void);


/** <b>SHA1 self test</b>.
 * Test SHA1 hash function.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_hash_sha1_stest(void);


/** <b>MD5 self test</b>.
 * Test MD5 hash function.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 */
int __API__ ucl_hash_md5_stest(void);


/** <b>RIPEMD160 self test</b>.
 * Test RIPEMD160 hash function.
 *
 * @return Error code
 *
 * @retval UCL_OK    Test passed
 * @retval UCL_ERROR Test failed
 *
 * @ingroup UCL_STEST
 */
int __API__ ucl_hash_ripemd160_stest(void);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /*UCL_STEST_H_*/
