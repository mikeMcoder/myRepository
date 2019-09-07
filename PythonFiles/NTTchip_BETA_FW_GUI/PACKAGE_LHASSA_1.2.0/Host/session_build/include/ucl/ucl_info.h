/*============================================================================
 *
 *  ucl_info.h
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
 * Purpose : Library information
 *
 *==========================================================================*/
#ifndef ucl_INFO_H_
#define ucl_INFO_H_

#define VERSION_STRING "2.0.0-trunk@1175 build 269840a5 - development"

#define OPTIONS_STRING "smartmips"

const char* ucl_get_version(void);

const char *ucl_get_copyright(void);

const char *ucl_get_build_date(void);

const char *ucl_get_options(void);

#endif /* ucl_INFO_H_ */
