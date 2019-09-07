/*============================================================================
 *
 * ucl_3des.h
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
 * Purpose : The Triple Data Encryption Standard (DES)
 *
 *==========================================================================*/
#ifndef _UCL_3DES_H_
#define _UCL_3DES_H_

#include "ucl/ucl_des.h"

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */


/** @file ucl_3des.h
 * @defgroup UCL_3DES 3DES
 * The Triple DES, see FIPS 46-3 and NIST SP 800-67.
 *
 * @par Header:
 * @link ucl_3des.h ucl_3des.h @endlink
 *
 * <b>3DES Descriptor:</b>
 * @li Length of Input/Output Block: 64 bits
 * @li Length of Key: 192 (24 parity bits) (see note).
 *
 * @note A Triple des key @p K is the concatenation of three DES key: @p K0,
 * @p K1 and @p K2. K is a 128-bit Triple des key if @p K0 = @p K2.
 *
 * @n
 * For messages longer than 64 bits use an Operation mode.@n
 * @n
 *
 * @see UCL_OPERATION_MODES
 * @ingroup UCL_BLOCK_CIPHER
 */


/*============================================================================*/
/** <b> 3DES Block Size</b>.
 * The byte length of the DES core data block.
 */
#define UCL_3DES_BLOCKSIZE 8
/** <b> 3DES Key size</b>.
 * Number of DES key for a 3DES.
 *
 * @ingroup UCL_3DES
 */
#define UCL_3DES_KEYNUMBER 3
/** <b> 3DES Key length</b>.
 * The byte length of the DES key.
 */
#define UCL_3DES_KEYSIZE (8*UCL_3DES_KEYNUMBER)


/** <b>3DES Context</b>.
 * This structure is involved in the operation modes.
 * @see UCL_OPERATION_MODES
 *
 * @ingroup UCL_3DES
 */
struct ucl_3des_ctx
{
    
    int mode;       /**< Ciphering Mode.*/
    u8 memory[8];   /**< Intermediate state.*/
    u32 index;      /**< index.*/
    u32 subKeys[UCL_3DES_KEYNUMBER*UCL_DES_NB_SUBKEYS*2]; /**< 3DES Sub-keys.
                                                            * @see UCL_3DES_KEYNUMBER
                                                            * @see UCL_DES_NB_SUBKEYS
                                                            */
};

/** <b>3DES Context</b>.
 * @ingroup UCL_3DES
 */
typedef struct ucl_3des_ctx ucl_3des_ctx_t;


/*============================================================================*/
/** <b>3DES for Single Block</b>.
 * The complete 3DES for only one block.
 *
 * @param[out] dst  Output Block (encrypted/decrypted).
 * @param[in]  src  Input Block to encrypt/decrypt.
 * @param[in]  key  A 3DES key.
 * @param[in]  mode The 3DES mode (Encryption/Decryption).
 *
 * @return Error code
 *
 * @retval #UCL_OK             if no error occurred
 * @retval #UCL_INVALID_INPUT  if one of the input is the pointer #NULL
 * @retval #UCL_INVALID_OUTPUT if one of the output is the pointer #NULL
 * @retval #UCL_INVALID_MODE   if the mode is not one of those described
 *
 * @note For more than one block use an @link UCL_OPERATION_MODES
 *    Operation Modes @endlink.
 *
 * @ingroup UCL_3DES
 */
int __API__ ucl_3des(u8 *dst, u8 *src, u8 *key, int mode);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /* _UCL_3DES_H_ */
