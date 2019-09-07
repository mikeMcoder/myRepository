// ----------------------------------------------------------------------------
// Copyright (c) 2009-2013, Maxim Integrated Products
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//     * Neither the name of the <organization> nor the
//       names of its contributors may be used to endorse or promote products
//       derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY MAXIM INTEGRATED PRODUCTS ''AS IS'' AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL MAXIM INTEGRATED PRODUCTS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// ----------------------------------------------------------------------------
//
// Created on: Aug, 2013
// Author: D. RIOTTE
#ifndef _MXIM_SESSION_BUILD_INCLUDE
#define _MXIM_SESSION_BUILD_INCLUDE

#include "scp_definitions.h"


#ifdef _MXIM_HSM
//------------------------
//-- MXIMUCLI LIBRARY 
//------------------------
#include "MXIMUCL.h"

//------------------------
//-- MXIMNCIPHER LIBRARY 
//------------------------
#include "MXIMHSMCLI.h"
using namespace MXIM::HSM::nCipher;

#endif//MXIM_HSM

//-----------------------
// CONSTANTS
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#define INIFILE		 ".\\session_build.ini"
#define MAJV		3
#define MINV		7
#define ZVER		9
#define BUILD		1


#ifdef _MXIM_HSM
#define _MXIM_UCL_LIBRARY_PATH						 ".\\libucl.dll"
#endif//MXIM_HSM

#define _MXIM_MAX_STRING			255

#define TRUE						1
#define FALSE						0
	
	
#define MAX_PARAMS 4
#define MAXLINE	35000
#define MAX_TAB	100
#define MAX_FLASH_MB 1023
#define MAX_CHUNK_SIZE (15*1024)
#define MAXQ1852_CHUNK_SIZE 32
#define ERROR	1
#define OK	0
#define YES	1
#define NOT	0
#define ERR_INVAL UCL_ERROR
#define ERR_NO	UCL_OK
	
#define CHAR_TIMEOUT_UART_TARGET	'0'
#define CHAR_TIMEOUT_USB_TARGET		'U'
#define CHAR_TIMEOUT_VBUS_TARGET	'V'


#define TIMEOUT_UART_TARGET			0x00
#define TIMEOUT_USB_TARGET			0x55
#define TIMEOUT_VBUS_TARGET			0x56

//------------------------------//
//-- Cryptography information --//
//------------------------------//

#define MAX_RSA						256

//byte length of the CRK public exponent
#define RSA_MODULUS_LEN				256
#define RSA_PUBLIC_EXPONENT_LEN		4
#define SIGNATURE_LEN				RSA_MODULUS_LEN


//ECDSA256 so signature is 2*32=64 bytes
#define MAX_ECDSA					64

//byte length of the CRK public exponent
#define ECDSA_MODULUS_LEN			32
	
#define ECDSA_SIGNATURE_LEN			(2*ECDSA_MODULUS_LEN)

//----------------------------------------------------------------------------------------------//


//--------------------------------//
//-- MXIM Devices - information --//
//--------------------------------//


#define MAX32550 7
#define MAXQ1852 6
#define JIBE	5
#define IC400D	4
#define IC400ABC 1
#define IC300	2
#define IC200	3

#define SECTOR_MAX 35
#define SECTOR_SIZE 4096

#define USN_LEN	16
#define USN_FLORA_LEN	13
#define USN_ANGELA_LEN	13

//----------------------------------------------------------------------------------------------//

//---------------------------------------//
//-- MXIM Devices - device life cycles --//
//---------------------------------------//

#define P3		3
#define P4		4
#define P5		5
#define P6		6
#define P6A		0x6a
#define P7		7
#define P8		8

//----------------------------------------------------------------------------------------------//



///////////////////////
// GLOBAL VARIABLES
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef _MXIM_HSM
MXIMUcl g_objMXIMUCLLibrary(_MXIM_UCL_LIBRARY_PATH);
CMXHSMCLI		g_objMXHSMCLI;
#endif//MXIM_HSM

char			g_tcHSMRSALabelKey[_MXIM_MAX_STRING];
char			g_tcHSMECDSALabelKey[_MXIM_MAX_STRING];
	
char			g_tcQuorum_K[_MXIM_MAX_STRING];
char			g_tcQuorum_N[_MXIM_MAX_STRING];

typedef struct _type_config
{
  u8 cpu;
  u8 life_cycle;
  u8 usn[USN_LEN];
  int usn_len;
  u8 mka[UCL_AES_BLOCKSIZE];
  u8 mkc[UCL_AES_BLOCKSIZE];
  u8 mks[UCL_AES_BLOCKSIZE];
  u8 tka[UCL_AES_BLOCKSIZE];
  u8 tkc[UCL_AES_BLOCKSIZE];
  u8 tks[UCL_AES_BLOCKSIZE];
  u8 pka[UCL_AES_BLOCKSIZE];
  u8 pkc[UCL_AES_BLOCKSIZE];
  u8 pks[UCL_AES_BLOCKSIZE];
  u8 fka[UCL_AES_BLOCKSIZE];
  u8 fkc[UCL_AES_BLOCKSIZE];
  u8 fks[UCL_AES_BLOCKSIZE];
  u8 sblpk[UCL_AES_BLOCKSIZE];
  u8 rsa[RSA_MODULUS_LEN];
  u8 rsa_privexp[RSA_MODULUS_LEN];
  u8 rsa_pubexp[RSA_MODULUS_LEN];
  int rsa_len;
  int rsa_explen;
  int rsa_privexplen;
  int ecdsa_len;
  u8 ecdsa_privkey[ECDSA_MODULUS_LEN];
  u8 ecdsa_pubkey_x[ECDSA_MODULUS_LEN];
  u8 ecdsa_pubkey_y[ECDSA_MODULUS_LEN];
  u8 already_diversified;
  u8 pp;
  //this parameter represents the size, in MB, of the flash
  //targeted for the file programming (write-file)
  int flash_mb;
} type_config_struct;

type_config_struct	config_struct;

u8 crk_rsa_modulus[RSA_MODULUS_LEN];
u8 crk_rsa_pubexp[RSA_MODULUS_LEN];
u8 mrk_signature[RSA_MODULUS_LEN];

u8 crk_ecdsa_x[ECDSA_MODULUS_LEN];
u8 crk_ecdsa_y[ECDSA_MODULUS_LEN];
u8 mrk_ecdsa_r[ECDSA_MODULUS_LEN];
u8 mrk_ecdsa_s[ECDSA_MODULUS_LEN];
//max_data_size is used to control read data are not too large vs *data allocated size
int max_data_size;
u32 init_buffer[2048];
char*	source[2]={"host","bl"};

	

char idf_ctl[MAX_IDF][MAX_STRING];
char idf_scp_cmd[MAX_SCP_COMMAND][MAX_STRING];
int mode[MAX_SCP_COMMAND];
int list_ctl[MAX_IDF];
char idf_cmd[MAX_IDF][MAX_STRING];
int list_cmd[MAX_IDF];
char idf_pp[MAX_IDF][MAX_STRING];
int list_pp[MAX_IDF];
u8 hello_req_const[MAX_TAB];
u8 hello_rep_const[MAX_TAB];
u8 hello_off_req_const[MAX_TAB];
u8 hello_off_rep_const[MAX_TAB];
u8 hello_scp_req_const[MAX_TAB];
u8 hello_scp_rep_const[MAX_TAB];
 
//use keys
u8 keya[UCL_AES_BLOCKSIZE];
u8 keyc[UCL_AES_BLOCKSIZE];
u8 keys[UCL_AES_BLOCKSIZE];
u8 random_chlg[UCL_AES_BLOCKSIZE];

int seq,ch_id,tr_id;

u8 frame[MAX_FRAME];
u8 payload[MAX_FRAME];
u8 random_number[UCL_AES_BLOCKSIZE];
u8 response[UCL_AES_BLOCKSIZE];

int iframe;
int ipayload;
u8 who;

u8 session_mode;

int start_addr;
int end_addr;

u8* data;
int data_len;
int last_packet_len;
int* addr;
	
char	message[MAX_STRING];
char	output_file[MAX_STRING];
char	session_string[MAX_STRING];
char	name_file[MAX_STRING];
char	output_name[MAX_STRING];
char	s19file[MAX_STRING];
char	script_file[MAX_STRING];

char	rsafile[MAX_STRING];
char	ecdsafile[MAX_STRING];

u8 blpk[UCL_AES_BLOCKSIZE];
u8 fak[UCL_AES_BLOCKSIZE];
u8 aes_key[UCL_AES_BLOCKSIZE];
u8 aes_data[UCL_AES_BLOCKSIZE];
char	params[MAX_PARAMS][MAX_STRING];
int nb_params;
int compteur;
	
int address_offset;
int trid;
int chunk_size=0;


//for hex files in maxq1852
int hex_extended_address;



FILE*	fp;
u8 verbose;
int found;


#endif// _MXIM_SESSION_BUILD_INCLUDE
