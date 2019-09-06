/*============================================================================
 *
 *	ucl_pkcs1_mgf1_sha1.h
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright (c) 2002-2006 Innova Card. All rights reserved. Do not disclose.
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
 * Purpose : PKCS#1 V2.1 MGF1 with SHA1
 *
 *==========================================================================*/
#ifndef _UCL_MGF1_SHA1_H_
#define _UCL_MGF1_SHA1_H_

/** @file ucl_pkcs1_mgf1_sha1.h 
 * @defgroup UCL_MGF1_SHA1 MGF1-SHA1
 * Mask Generation Function based on the hash function SHA1.
 * 
 * @par Header:
 * @link ucl_pkcs1_mgf1_sha1.h ucl_pkcs1_mgf1_sha1.h @endlink
 *
 * @ingroup UCL_MGF1
 */


/*============================================================================*/
/** <b>MGF1-SHA1</b>.
 * Generate a @p mask using @p mgf_seed.
 *
 * @param[out]	mask 			Pointer to generated mask
 * @param[in]	mask_length		Mask byte length
 * @param[in]	mgf_seed		Pointer to a seed
 * @param[in]	mgf_seed_length	Seed byte length
 *
 * @return	Error code
 *
 * @retval	#UCL_OK				if no error occurred
 * @retval	#UCL_INVALID_OUTPUT	if the output is the pointer #NULL
 * @retval	#UCL_NOP				if the mask length is null
 * @retval	#UCL_INVALID_ARG		if the mask length is out of range
 *
 * @see #UCL_RSA_KEY_MAXSIZE
 * @see UCL_SHA1
 *
 * @ingroup UCL_MGF1_SHA1
 */
int ucl_pkcs1_mgf1_sha1(u8 *mask, u32 mask_length, u8 *mgf_seed, 
	u32 mgf_seed_length);


#endif //_UCL_MGF1_SHA1_H_
