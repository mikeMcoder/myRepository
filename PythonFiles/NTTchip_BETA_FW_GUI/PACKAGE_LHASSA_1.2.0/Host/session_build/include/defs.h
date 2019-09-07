/*============================================================================
 *
 * _ucl_defs.h
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
 * Purpose : Definitions
 *
 *==========================================================================*/
#ifndef _DEFS_H_
#define _DEFS_H_

#include "ucl/ucl_config.h"
#include "ucl/ucl_types.h"
#include "ucl/ucl_defs.h"
#include "ucl/ucl_retdefs.h"

/** Number probably prime.
 * @ingroup UCL_FPA
 */
#define UCL_IS_PRIME UCL_TRUE
/** Number composite.
 * @ingroup UCL_FPA
 */
#define UCL_ISNOT_PRIME  UCL_FALSE

#if __mips16e
#define __nomips16__ __attribute__((nomips16))
#else
#define __nomips16__
#endif

#endif /* _DEFS_H_ */
