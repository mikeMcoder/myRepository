
/*============================================================================
 *
 * memory.h [17-mar-06]
 *
 *==========================================================================*/
/*============================================================================
 *
 * Copyright © 2009 Innova Card. All Rights Reserved. Do not disclose.
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
#ifndef _MEMORY_H_
#define _MEMORY_H_

typedef struct bignum_stack
{
    u32 *pt;
    int index;
    int size;
    u32 s;
}

bignum_stack_t;

typedef struct bignum
{
    bignum_stack_t *stack;
    u32 *pt;
    int index;
}

bignum_t;


int bignum_stack_init(bignum_stack_t *stack, u32 s, u32 *pt, u32 size);

int bignum_free(bignum_t *x);

int bignum_alloc(bignum_t *x, bignum_stack_t *stack);

#endif /*MEMORY_H_*/
