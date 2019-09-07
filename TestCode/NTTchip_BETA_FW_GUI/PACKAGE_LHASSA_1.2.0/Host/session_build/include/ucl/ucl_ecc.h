/*============================================================================
 *
 *    ucl_ecc.h
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
#ifndef UCL_ECC_H_
#define UCL_ECC_H_

#ifdef _cplusplus
extern "C" {
#endif /* _ cplusplus  */

/** @file ucl_ecc.h
 * @defgroup UCL_ECC ECC
 * Elliptic Curve Cryptography.
 *
 * @par Header:
 * @link ucl_ecc.h ucl_ecc.h @endlink
 * @n
 * Elliptic curves have been studied by mathematicians for more than a century.
 * A rich theory have been developed around them, and cryptography have taken
 * the advantage to find a way to use it in practice.
 * Elliptic curve public key cryptosystems were proposed independently by
 * Victor Miller and Neil Koblitz in the mid-eighties. After many attempts to
 * make a cryptographic protocol with an high level of confidence,
 * the first commercial implementation is appearing in the last ten years.
 * The security of the ECC is based on difficulty of the discret logarithm
 * problem.@n
 * @n
 * <b>Principle:</b>@n
 * @n
 * An elliptic curve can be defined as an equation of the form :@n
 * @f$ E ~:~ y^{2} + a_{1}xy + a_{3}y ~=~ x^{3} + a_{2}x^{2} + a_{4}x + a_{6}} @f$ @n
 * For cryptographic purpose @a E is defined on GF(p) or GF(2^m).
 * @n
 * If the characteristic of the curve is different from 2 or 3, then an
 * admissible change of variable transforms the equation to :@n
 * @f$ E ~:~ y^{2}~=~x^3+a.x+b @f$ @n
 * If the characteristic of the curve is  2 then an
 * admissible change of variable transforms the equation to :@n
 * @f$ E ~:~ y^{2} + x.y ~=~x^3+ a.x^2 + b @f$ @n
 * @n
 * A point of the curve is a couple @f$ (x,y) @f$  verifying the equation @a E. @n
 * @n
 * It exists an addition on @a E such as @a E is a group.
 * If @a P is point of @a E, then we note @f$ Q = k.P @f$ the result of @p k 
 * successive additions. @n
 * The discrete logarithm problem is the problem which consists to find @p k 
 * from @p Q and @p P.
 *
 * @ingroup UCL_PKC
 */

/* ========================================================================== */


/** @defgroup UCL_ECC_FLAGS ECC Curve Flags.
 * Elliptic Curve Flags.
 * 
 * This module regroups the flag options defining a curve:@n
 *  @li UCL_ECC_CURVE_GF_* : Field of the curve.
 *  @li UCL_ECC_CURVE_T_* : Type of the curve.
 *  @li UCL_ECC_CURVE_A_* : Type of the parameter @p a.
 *  
 * The flag of a curve is a combination of those three group:
 * flag = UCL_ECC_CURVE_GF_X | UCL_ECC_CURVE_T_Y | UCL_ECC_CURVE_A_Z
 * 
 * @ingroup UCL_ECC
 */

/** <b>Prime Field Curve (@f$ GF(q) @f$)</b>.
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_GF_Q      (0x00)

/** <b>Binary Curve (@f$ GF(2^m) @f$)</b>.
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_GF_2M     (0x01)


/** <b>Random Curve</b>. 
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_T_RAND    (0x00)

/** <b>NIST Curve</b>. 
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_T_NIST    (0x04)

/** <b>Koblitz Curve</b>. 
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_T_KOB     (0x08)

/** <b>NIST Koblitz Curve</b>. 
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_T_NKOB    (0x0C)


/** <b>Random @p a coefficient</b>. 
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_A_RAND    (0x00)

/** <b>Special @p a coefficient</b>.
 * @ingroup UCL_ECC_FLAGS
 */
#define UCL_ECC_CURVE_A_SPEC    (0x10)

    
/* ========================================================================== */
  
    
/** <b>Elliptic point</b>.
 * Three coordinates structure for affine & projective points.
 *
 * @ingroup UCL_ECC
 */
struct ucl_ecc_point_s
{
    u32 *x;    /**< x coordinate (affine)     */
    u32 *y;    /**< y coordinate (affine)     */
    u32 *z;    /**< z coordinate (projective) */
} ;

/** <b>Point</b>.
 * Point of a curve.
 * 
 * @ingroup UCL_ECC
 */
typedef struct ucl_ecc_point_s ucl_ecc_point_st;


/** <b>Extended point</b>.
 * Point of a curve with extended coordinates.
 *
 * @ingroup UCL_ECC
 */
struct ucl_ecc_point_ext_s
{
    u32 *x;    /**< x coordinate (affine)               */
    u32 *y;    /**< y coordinate (affine)               */
    u32 *z;    /**< z coordinate (projective)           */
    u32 *az;   /**< az coordinate (extended projective) */
};

/** <b>Extended point</b>.
 * @ingroup UCL_ECC
 */
typedef struct ucl_ecc_point_ext_s ucl_ecc_point_ext_st;

struct ucl_ecc_mult_s
{
    int type;
    int options;
    ucl_ecc_point_st **mP;
};

typedef struct ucl_ecc_mult_s ucl_ecc_mult_t;

/** <b>Elliptic Curve</b>.
 * Elliptic curve structure.
 *
 * @ingroup UCL_ECC
 */
struct ucl_ecc_curve_s
{
    u32 flags;											   /**< Flags defining the curve.                                */
    u32 field;
    u32 options;                                           /**< Options                                                  */
    u32 *q;                                                /**< @p q is the prime order or the irreducible polynom.      */
    u32 s;                                                 /**< Precision of @p q                                        */
    u32 param1;                                            /**< Parameter 1                                              */
    u32 *param2;                                           /**< Parameter 2                                              */
    int(*mult)(u32 *, u32 *, u32 *, u32, u32);             /**< Field multilication.                                     */
    int(*inv)(u32 *, u32 *, u32 *, u32, u32, u32 *);       /**< Field inversion.                                         */
    u32 *seed;                                             /**< If the curve has been randomly generated, the seed used. */
    u32 *a;                                                /**< Coefficient a. (could be NULL)                           */
    u32 *b;                                                /**< Coefficient b.                                           */
    ucl_ecc_point_st *P;                                   /**< The base point in affine coordinate.                     */
    u32 *n;                                                /**< The base point order                                     */
    u32 h;                                                 /**< The cofactor (the order of the curve).                   */
    int(*add_loop)(void *, void *, void *, void *, u32 *); /**< Add in loop                                              */
    int(*sub_loop)(void *, void *, void *, void *, u32 *); /**< Sub in loop                                              */
    int(*neg)(void *, void *);                             /**< Negation in projective coordinate.                       */
    int(*add)(void *, void *, void *, void *, u32 *);      /**< Add in projective coordinate.                            */
    int(*kdbl)(void *, void *, void *, u32, u32 *);        /**< Double in projective coordinate.                         */
    int(*kconv)(void *, void *, u32);                      /**< Conversion from projective to affine coordinate.         */
    int(*begin)(void *, void *);                           /**< Prepare a point to be used on this field.                */
    int(*finish)(void *, void *);                          /**< To recover a point from calculus on this field.          */
    ucl_ecc_mult_t ecc_mult;
};

/** <b>Elliptic Curve</b>.
 * 
 * @ingroup UCL_ECC
 */

typedef struct ucl_ecc_curve_s ucl_ecc_curve_st;


/* ========================================================================== */


/* ========================================================================== */
/** <b>Elliptic Curve Initialization</b>.
 * Init an elliptic curve.
 *
 * @param[in,out] e The curve to initialize.
 *
 * @return Error code
 *
 * @retval #UCL_OK            No error occurred
 * @retval #UCL_INVALID_INPUT The input curve contains a #NULL pointer forbidden
 * @retval #UCL_STACK_ERROR   UCL Stack error
 * @retval #UCL_ERROR         Invalid curve flags
 * 
 * @warning It is mandatory to initialize a curve before to use it.
 *
 * @ingroup UCL_ECC
 */
int __API__ ucl_ecc_init(ucl_ecc_curve_st *e);


#ifdef _cplusplus
}
#endif /* _ cplusplus  */

#endif /*UCL_ECC_H_*/
