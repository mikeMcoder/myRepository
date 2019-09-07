/*============================================================================
 *
 * ucl_config.h
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
#ifndef _UCL_CONFIG_H_
#define _UCL_CONFIG_H_

#if __mips

#define __API__

//#elif __i386 /* __mips */
#else

#if __MINGW32__

#ifdef BUILD_DLL
#define __API__ __declspec(dllexport)
#else
#define __API__ __declspec(dllimport)
#endif /* BUILD_DLL */

#else /* __MINGW32__ */

#define __API__

#endif /* __MINGW32__ */

#endif /* __i386 */

/** <b>UCL Stack default size</b>.
 * 8 Ko.
 * @ingroup UCL_CONFIG */
#define UCL_STACK_SIZE 1024

/** <b>UCL RSA key max size</b>.
 * 512 bytes: 4096 bits.
 * @ingroup UCL_CONFIG
 */
#define UCL_RSA_KEY_MAXSIZE 512

/** <b>UCL RSA public exponent max size</b>.
 * 4 bytes: 32 bits.
 * @ingroup UCL_CONFIG */
#define UCL_RSA_PUBLIC_EXPONENT_MAXSIZE 4

/** <b>UCL ECC Precision</b>.
 * @ingroup UCL_CONFIG */
#define UCL_ECC_PRECISION 17

#endif /*_UCL_CONFIG_H_*/
