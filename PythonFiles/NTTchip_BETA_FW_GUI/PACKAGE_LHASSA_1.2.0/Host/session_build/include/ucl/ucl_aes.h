/*============================================================================
 *
 * ucl_aes.h [14-mar-06]
 *
 *==========================================================================*/
/*============================================================================
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
/*============================================================================
 *
 * Purpose :
 *
 *==========================================================================*/
#ifndef _UCL_AES_H_
#define _UCL_AES_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/** @file ucl_aes.h
 * @defgroup UCL_AES AES
 * The AES, see FIPS-197.
 *
 * @par Header:
 * @link ucl_aes.h ucl_aes.h @endlink
 *
 * <b>AES Descriptor:</b>
 * @li Length of Input/Output Block: 128 bits
 * @li Length of Key: 128, 192 or 256 bits
 *
 * For messages longer than 128 bits use an Operation mode.@n
 * @n
 *
 * @see UCL_OPERATION_MODES
 * @ingroup UCL_BLOCK_CIPHER */


/*============================================================================*/
/** <b>AES Block Size</b>.
 * The byte length of the DES core data block.
 * @ingroup UCL_AES */
#define UCL_AES_BLOCKSIZE 16

/** <b>128-bits AES Key byte length</b>.
 * @ingroup UCL_AES */
#define UCL_AES_KEYLEN_128 16
/** <b>192-bits AES Key byte length</b>.
 * @ingroup UCL_AES */
#define UCL_AES_KEYLEN_192 24
/** <b>256-bits AES Key byte length</b>.
 * @ingroup UCL_AES */
#define UCL_AES_KEYLEN_256 32

/** <b>AES maximum round number</b>.
 * @ingroup UCL_AES */
#define UCL_AES_MAXNR   14


/*============================================================================*/
/** <b>AES Key</b>.
 * @ingroup UCL_AES */
struct ucl_aes_key
{
    
    u32 rd_key[4 *(UCL_AES_MAXNR + 1)]; /**< Round key.        */
    int rounds;                         /**< Number of rounds. */
};

/** <b>AES Key</b>.
 * @ingroup UCL_AES */
typedef struct ucl_aes_key ucl_aes_key_t;

/** <b>AES Context</b>.
 * This structure is involved in the operation modes.
 * @see UCL_OPERATION_MODES
 *
 * @ingroup UCL_AES */
struct ucl_aes_ctx
{
    int mode;                     /**< Ciphering Mode.    */
    u8 memory[UCL_AES_BLOCKSIZE]; /**< Intermediate state.*/
    u32 index;                    /**< index.             */
    ucl_aes_key_t key;            /**< AES Sub-keys.      */
};

/** <b>AES Context</b>.
 * @ingroup UCL_AES */
typedef struct ucl_aes_ctx ucl_aes_ctx_t;


/*============================================================================*/
/** <b>AES for Single Block</b>.
 * The complete AES for only one block.
 *
 * @param[out] dst    Output Block (encrypted/decrypted)
 * @param[in]  src    Input Block to encrypt/decrypt
 * @param[in]  key    An AES key
 * @param[in]  keylen AES key byte length
 * @param[in]  mode   The AES mode (Encryption/Decryption)
 *
 * @return Error code
 *
 * @retval #UCL_OK             No error occurred
 * @retval #UCL_INVALID_INPUT  One of the input is the pointer #NULL
 * @retval #UCL_INVALID_OUTPUT One of the output is the pointer #NULL
 * @retval #UCL_INVALID_MODE   The mode is not one of those described
 *
 * @note For more than one block use an @link UCL_OPERATION_MODES
 *       Operation Modes @endlink.
 *
 * @ingroup UCL_AES
 */
int __API__ ucl_aes(u8 *dst, u8 *src, u8 *key, u32 keylen, int mode);

#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /*_UCL_AES_H_*/
