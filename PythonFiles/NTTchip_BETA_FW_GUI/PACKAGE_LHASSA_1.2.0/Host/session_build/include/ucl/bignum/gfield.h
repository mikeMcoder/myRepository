/*============================================================================
 *
 * bignum/gfield.h
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright (c) 2002-2006 Innova Card.
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
 * Purpose : Generic structure for Galois Field Operations
 *     over Montgomery arithmetic
 *
 *==========================================================================*/
#ifndef GFIELD_H_
#define GFIELD_H_

struct field_ctx
{
    // Modulus (n prime or n representative of an irreducible polynomial)
    u32 *n;
    // r^2 with r used in Montgomery reduction
    u32 *rs;
    // Extra variable using in DH
    u32 *g;
    // n' = -(n[0])^-1 mod 2^32
    u32 np;
    // Length
    u32 s;
};

typedef struct field_ctx field_ctx_t;


#endif /*GFIELD_H_*/
