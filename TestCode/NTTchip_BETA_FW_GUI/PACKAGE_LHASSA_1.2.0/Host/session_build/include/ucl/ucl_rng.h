/*===========================================================================
 *
 * ucl_rng.h
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
 * Purpose: Random Number Generator Interface
 *
 *==========================================================================*/
#ifndef UCL_RNG_H_
#define UCL_RNG_H_

int __API__ ucl_rng_attach(int (*rng)(u8* rand, u32 rand_byteLen, int option));

int __API__ ucl_rng_detach(void);

void * __API__ ucl_rng_getpt(void);

int __API__ ucl_rng_read(u8* rand, u32 rand_byteLen, int option);

#endif /*UCL_RNG_H_*/
