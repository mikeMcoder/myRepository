/*============================================================================
 *
 * ucl_sys.h
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
#ifndef _UCL_SYS_H_
#define _UCL_SYS_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/** @file ucl_sys.h
 * @defgroup UCL_SYSTEM UCL System
 * UCL System Functions.
 *
 * @par Header:
 * @link ucl_sys.h ucl_sys.h @endlink
 *
 */

/** <b>UCL Init</b>.
 * USIP&reg; Cryptographic Library Initialisation.
 *
 * Initialisation of stack and hardware interface (if available).
 *
 * @return #UCL_OK or Error vector
 * 
 * @retval The error vector is a combination of:
 *     @li 0x001: UCL Stack error
 *     @li 0x010: USIP(R) AES not available
 *     @li 0x020: USIP(R) AES Corrrupted
 *     @li 0x100: USIP(R) TRNG not available
 *     @li 0x200: USIP(R) TRNG Corrupted
 *
 * @ingroup UCL_SYSTEM
 */
int __API__ ucl_init(u32 *buffer, u32 bufferlen);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /* _UCL_SYS_H_ */
