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
// Created on: Feb, 2010
// Author: Y.LOISEL
//
// ---- Subversion keywords (need to set the keyword property)
// $Rev::               $:  Revision of last commit
// $Author::            $:  Author of last commit
// $Date::              $:  Date of last commit
// SCP session build
// this tool creates scp sessions packets
// for jibe, londa and maxq1852

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <defs.h>
#include <string.h>


#ifdef WIN32
#define __API__
#endif

#ifdef __cplusplus
extern "C"
{
#endif


#include <ucl/ucl_data_conv.h>
#include <ucl/ucl_stack.h>

#include <ucl/ucl_rng.h>
#include <ucl/ucl_config.h>
#include <ucl/ucl_defs.h>
#include <ucl/ucl_retdefs.h>
#include <ucl/ucl_types.h>

#include <ucl/ucl_sys.h>
#include <ucl/ucl_trng.h>
#include <ucl/ucl_des_ecb.h>
#include <ucl/ucl_3des_ecb.h>
#include <ucl/ucl_des_cbc.h>
#include <ucl/ucl_des_cbc_mac.h>
#include <ucl/ucl_tdes_cbc_mac.h>
#include <ucl/ucl_3des_cbc.h>
#include <ucl/ucl_des_ofb.h>
#include <ucl/ucl_3des_ofb.h>
#include <ucl/ucl_des_cfb.h>
#include <ucl/ucl_3des_cfb.h>
#include <ucl/ucl_pkcs1_ssa_pss_sha1.h>
#include <ucl/ucl_pkcs1_ssa_pss_sha256.h>
#include <ucl/ucl_info.h>
#include <ucl/ucl_aes.h>
#include <ucl/ucl_aes_ecb.h>
#include <ucl/ucl_uaes.h>
#include <ucl/ucl_uaes_ecb.h>
#include <ucl/ucl_uaes_cbc.h>
#include <ucl/ucl_rsa.h>
#ifndef _MXIM_HSM
	#include <ucl/ecdsa_generic_api.h>
#endif
#include <ucl/ucl_sha1.h>
#include <ucl/ucl_sha256.h>

#ifdef __cplusplus
}
#endif

#include "session_build.h"

//1100: modification on hello reply and challenge including protection profile
//modification for display bin (wb instead of w)
//1110: modification on adding response length in generic response
//modification on chlg combination with pp (on rn0 and not rn15)
// this version contains:
//-support for IC400D
//-RCS commands management
//1120 .packet for binaries frames extension
//1130 tr_id incremented after each response
//1140 crypto_aes_cmac embedded to avoid dependance to libicrypto.a
//1150 CHUNK_SIZE increased to 3KB
//1160 decimal field in file name extended to 7 digits
//     session size in write_mem_payload and verify_data_payload on 2 bytes..
//1170 verify_file added in script
//1180 mem_mapping_payload was not called by mem_mapping, but read_conf...
//     CHUNK_SIZE=15KB
//     2bugs in write_file: the chunk_len was incremented too early (before using chunk_len=0), so
//     the 1st byte was always zero
//     other bug: the internal loop was performed without checking i vs data_len, which leads to an error on end of file
//1191 bug 1601 & 1597: hello reply corrected
//     disconnection_request & reply used with incorrect seq number (not incremented from previous command)
//1201 management of scripts
//1211 only one process_script function; fixed-random-number mode supported
//1221 bug #1623 (bad transaction-id) corrected
//     bug #1622 incorrect blpk (and fak!) values
//1231 bug # ?? : transaction id (tr_id) was never incremented (and not checked by the bootloader)
//1241 file size normalized to multiple of 16
//1251 MAX_SCP_COMMAND increased (buffer overflow)
//1261 MAX_SCP COMMAND increased (buffer overflow: bug 1749); compilation warnings removed
//1271 issue on parameters process (config file loading fgets_correction not used every time)
//1301 bug #1757 correction; support s20 format
//1302 correction s20 nbbytes, seq is modulo 16
//1312 verbosity reduced; #1748 correction
//1321 bug #1767 correction: supported flash is now only limited to 1023MB (because of 32-bit int)
//1331 implements feature #1560: DEL-MEM and WRITE-MEM have same level of admin, so codes have been changed
//2001 implements SCP for flora (specific commands; compliant with SPEC22T02 rev 0.2.0); two modes: SCP__FLORA_RSA and SCP__FLORA_AES
//2101 implements modified write-timeout, following SPEC22T02 rev 0.2.1 modification
//2111 EXECUTE CODE command added for FLORA profile
//2121 chunk_size=4KB
//2131 pp=RSA forced when SCP__FLORA_RSA
//2141 write-crk len corrected (2 extrabytes)
//2151 errors returns codes from commands processing exploited
//2201 support of write-file-only and erase-file
//2211 support of flora 13-byte USN
//2221 control of RSA lengths to avoid bug #2031
//2231 hardcoded value of hello-reply configuration was wrong (0x01); it has been changed into jtag+rwk enabled: 0xC0
//2241 write-otp command format help was wrong; offset set as 1st parameter
//2301 #bug 2061: SCP bootloader for PCI-Linux shall use SHA256 and not SHA1
//2311 #bug 2064: timeout uart target issue
//2321 warning about secure keys handling
//2331 #bug2128
//2341 #bugs 2130, #2203, #feature 2212; timeout packet length+1 (write-timeout-payload) (and added ptr_address_offset for an optional use of address_offset; but not finished);
//CAUTION: write-mem-config is not implemented
//2351 SCP_FLORA_RSA full support
//2361 bug 2252 (incorrect file size for verify-file); also corrected on write-file and write-only
//2371 the chunk_size for write-data corresponds to the whole packet length and not the data payload only
//3001 implements secure protocol for MAXQ1852 (ECDSA256)
//3101 added transaction id field for 1852 (msp specs rev 0.93)
//3201 added verify-crk, activate-crk commands, generate-application-startup-certificate, verify-application-startup-certificate, renamed load crk, change response ASP into AGP (msp specs rev 1.0)
// renamed SCP_MAXQ1852 into MSP_MAXQ1852
//3301 MSP_MAXQ1852: SCOFFSET removed from  host packets (incorrect); size recomputed accurately (incl. ecdsa signature size) and handled for the signature; ipayload reduced by 3 as not including the header
//3401 SCOFFSET removed from target packets (misunderstanding of the spec); signature is include lsB first in payload for MSP
//3501 xq,yq is lsB in load-crk and in verify-crk (it is preferred to reverse it within the application and to keep it msB in the script file)
//3511 correction of bug #2982; ecdsafile and rsa parameters renamed in ecdsa_file and rsa_file; rsamod, public_exponent and private_exponent retrieved from the possible parameters list (as the rsa key is loaded now via the rsa_file parameter)
//3521 support of load-file hex for maxq1852
//3701 support for hsm
//3711 support for (lighthouse) angela SCP for test keys.
//3721 rsa file format frozen to modulus|privexp|pubexp (consistent with crk_sign 1.2.1 and ca_sign 1.2.9); ecdsa signature storage in payload corrected
//3731 read crk file was not supporting ecdsa format (angela ecdsa)
//3741 ANGELA ECDSA PROFILE inserted in the HELLO-REQ
//3751 data len in write-crk ecdsa angela incorrect
//3761 generic response for angela ecdsa includes an incorrect aes cmac
//3771 MAXQ1852 load-file improved
//3781 #3747: rewrite-crk added for angela and lhassa
//3791 #3780: vbus detect support
#define UNUSED_PARAMETER(x) (void)(x)   // optimized away by compiler

int test_hex(char c1,char c2)
{
  int value;
  int ok1,ok2;
  value=0;
  ok1=ok2=0;
  if(c1>='A' && c1<='F')
    {
      value=(c1-'A'+10);
      ok1=1;
    }
  if(c1>='a' && c1<='f')
    {
    value=(c1-'a'+10);
      ok1=1;
    }
  if(c1>='0' && c1<='9')
    {
    value=(c1-'0');
      ok1=1;
    }
  value*=16;
  if(c2>='A' && c2<='F')
    {
    value+=(c2-'A'+10);
      ok2=1;
    }
  if(c2>='a' && c2<='f')
    {
    value+=(c2-'a'+10);
      ok2=1;
    }
  if(c2>='0' && c2<='9')
    {
    value+=(c2-'0');
      ok2=1;
    }
  if(ok1==0 || ok2==0)
    return(EXIT_FAILURE);
  return(EXIT_SUCCESS);
}

int hex(char c1,char c2)
{
  int value;
  value=0;
  if(c1>='A' && c1<='F')
    value=(c1-'A'+10);
  if(c1>='a' && c1<='f')
    value=(c1-'a'+10);
  if(c1>='0' && c1<='9')
    value=(c1-'0');
  value*=16;
  if(c2>='A' && c2<='F')
    value+=(c2-'A'+10);
  if(c2>='a' && c2<='f')
    value+=(c2-'a'+10);
  if(c2>='0' && c2<='9')
    value+=(c2-'0');
  return(value);
}

void define_const(void)
{
  hello_req_const[0]=0x48;
  hello_req_const[1]=0x49;
  hello_req_const[2]=0x2D;
  hello_req_const[3]=0x55;
  hello_req_const[4]=0x53;
  hello_req_const[5]=0x49;
  // to be corrected
  hello_req_const[6]=0x50;
  hello_req_const[7]=0x00;

  hello_rep_const[0]=0x48;
  hello_rep_const[1]=0x49;
  hello_rep_const[2]=0x2D;
  hello_rep_const[3]=0x55;
  hello_rep_const[4]=0x53;
  hello_rep_const[5]=0x49;
  hello_rep_const[6]=0x50;

  hello_scp_req_const[0]='H';
  hello_scp_req_const[1]='E';
  hello_scp_req_const[2]='L';
  hello_scp_req_const[3]='L';
  hello_scp_req_const[4]='O';
  hello_scp_req_const[5]=' ';
  hello_scp_req_const[6]='B';
  hello_scp_req_const[7]='L';
  hello_scp_req_const[8]=0x00;

  hello_scp_rep_const[0]='H';
  hello_scp_rep_const[1]='E';
  hello_scp_rep_const[2]='L';
  hello_scp_rep_const[3]='L';
  hello_scp_rep_const[4]='O';
  hello_scp_rep_const[5]=' ';
  hello_scp_rep_const[6]='H';
  hello_scp_rep_const[7]='O';
  hello_scp_rep_const[8]='S';
  hello_scp_rep_const[9]='T';


  hello_off_req_const[0]=0x48;
  hello_off_req_const[1]=0x4F;
  hello_off_req_const[2]=0x2D;
  hello_off_req_const[3]=0x55;
  hello_off_req_const[4]=0x53;
  hello_off_req_const[5]=0x49;
  // to be corrected
  hello_off_req_const[6]=0x50;
  hello_off_req_const[7]=0x00;

  hello_off_rep_const[0]=0x48;
  hello_off_rep_const[1]=0x49;
  hello_off_rep_const[2]=0x2D;
  hello_off_rep_const[3]=0x55;
  hello_off_rep_const[4]=0x53;
  hello_off_rep_const[5]=0x49;
  hello_off_rep_const[6]=0x50;

}

void define_ctl(void)
{
  int i;
  for(i=0;i<MAX_IDF;i++)
    list_ctl[i]=0;
  list_ctl[1]=list_ctl[2]=list_ctl[3]=list_ctl[4]=list_ctl[5]=list_ctl[6]=list_ctl[0xB]=list_ctl[0xC]=list_ctl[7]=list_ctl[0x17]=list_ctl[0x27]=list_ctl[0x37]=list_ctl[0x47]=list_ctl[0x57]=list_ctl[0x67]=list_ctl[0x77]=list_ctl[0x87]=list_ctl[0x08]=list_ctl[0x09]=1;
  strcpy(idf_ctl[1],"CON_REQ");
  strcpy(idf_ctl[2],"CON_REP");
  strcpy(idf_ctl[0x09],"CON_REF");
  strcpy(idf_ctl[3],"DISC_REQ");
  strcpy(idf_ctl[4],"DISC_REP");
  strcpy(idf_ctl[DATA_TRANSFER],"DATA_TRANSFER");
  strcpy(idf_ctl[6],"ACK");
  strcpy(idf_ctl[0xB],"ECHO_REQ");
  strcpy(idf_ctl[0xC],"ECHO_REP");
  strcpy(idf_ctl[7],"CHG_SP_0");
  strcpy(idf_ctl[0x17],"CHG_SP_1");
  strcpy(idf_ctl[0x27],"CHG_SP_2");
  strcpy(idf_ctl[0x37],"CHG_SP_3");
  strcpy(idf_ctl[0x47],"CHG_SP_4");
  strcpy(idf_ctl[0x57],"CHG_SP_5");
  strcpy(idf_ctl[0x67],"CHG_SP_6");
  strcpy(idf_ctl[0x77],"CHG_SP_7");
  strcpy(idf_ctl[0x87],"CHG_SP_8");
  strcpy(idf_ctl[8],"CHG_SP_REP");
}

void define_cmd(void)
{
  int i;
  for(i=0;i<MAX_IDF;i++)
    list_cmd[i]=0;
  list_cmd[1]=list_cmd[2]=list_cmd[7]=list_cmd[3]=list_cmd[4]=list_cmd[5]=list_cmd[8]=list_cmd[9]=1;
  strcpy(idf_cmd[1],"HELLO");
  strcpy(idf_cmd[2],"HELLO_REP");
  strcpy(idf_cmd[7],"CHLG");
  strcpy(idf_cmd[3],"SUCCESS");
  strcpy(idf_cmd[4],"FAILURE");
  strcpy(idf_cmd[5],"DATA");
  strcpy(idf_cmd[8],"HELLO_OFF");
  strcpy(idf_cmd[9],"HELLO_OFF_REP");
}

void define_scp_cmd(void)
{
  strcpy(idf_scp_cmd[COMMAND_UNKNOWN],"unknown-command");
  strcpy(idf_scp_cmd[COMMAND_HELP],"help");
  strcpy(idf_scp_cmd[COMMAND_WRITE_FILE],"write-file");
  strcpy(idf_scp_cmd[COMMAND_WRITE_ONLY],"write-only");
  strcpy(idf_scp_cmd[COMMAND_ERASE_DATA],"erase-data");
  strcpy(idf_scp_cmd[COMMAND_VERIFY_FILE],"verify-file");
  strcpy(idf_scp_cmd[COMMAND_WRITE_BLPK],"write-blpk");
  strcpy(idf_scp_cmd[COMMAND_WRITE_FAK],"write-fak");
  strcpy(idf_scp_cmd[COMMAND_READ_CONFIGURATION],"read-configuration");
  strcpy(idf_scp_cmd[COMMAND_READ_MEMORY_MAPPING],"read-memory-mapping");
  strcpy(idf_scp_cmd[COMMAND_WRITE_CRK],"write-crk");
  strcpy(idf_scp_cmd[COMMAND_REWRITE_CRK],"renew-crk");
  strcpy(idf_scp_cmd[COMMAND_WRITE_BPK],"write-bpk");
  strcpy(idf_scp_cmd[COMMAND_WRITE_OTP],"write-otp");
  strcpy(idf_scp_cmd[COMMAND_WRITE_TIMEOUT],"write-timeout");
  strcpy(idf_scp_cmd[COMMAND_KILL_CHIP],"kill-chip");
  strcpy(idf_scp_cmd[COMMAND_EXECUTE_CODE],"execute-code");
  strcpy(idf_scp_cmd[COMMAND_WRITE_CONFIGURATION],"write-configuration");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY],"load-customer-key");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA],"erase-code-flash-area");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS],"erase-all-flash-areas");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CODE],"load-code");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_LOAD_FILE],"load-file");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_FILE],"verify-1852-file");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_LOAD_DATA],"load-data");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CODE],"verify-code");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_DATA],"verify-data");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_WRITE_REGISTER],"write-register");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_READ_REGISTER],"read-register");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_ENGAGE_PLLO],"engage-pllo");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY],"verify-customer-key");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY],"activate-customer-key");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE],"generate-application-startup-signature");
  strcpy(idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE],"verify-application-startup-signature");
  mode[COMMAND_HELP]=SCP_RSA+SCP_FLORA_RSA;
  mode[COMMAND_WRITE_FILE]=SCP_RSA+SCP_FLORA_RSA;
  mode[COMMAND_WRITE_ONLY]=SCP_RSA+SCP_FLORA_RSA;
  mode[COMMAND_ERASE_DATA]=SCP_RSA+SCP_FLORA_RSA;
  mode[COMMAND_VERIFY_FILE]=SCP_RSA+SCP_FLORA_RSA;
  mode[COMMAND_WRITE_BLPK]=SCP_RSA;
  mode[COMMAND_WRITE_FAK]=SCP_RSA;
  mode[COMMAND_READ_CONFIGURATION]=SCP_RSA;
  mode[COMMAND_WRITE_CONFIGURATION]=SCP_RSA;
  mode[COMMAND_READ_MEMORY_MAPPING]=SCP_RSA;
  mode[COMMAND_WRITE_CRK]=SCP_FLORA_RSA;
  mode[COMMAND_REWRITE_CRK]=SCP_FLORA_RSA;
  mode[COMMAND_WRITE_BPK]=SCP_FLORA_RSA;
  mode[COMMAND_WRITE_OTP]=SCP_FLORA_RSA;
  mode[COMMAND_WRITE_TIMEOUT]=SCP_FLORA_RSA;
  mode[COMMAND_KILL_CHIP]=SCP_FLORA_RSA;
  mode[COMMAND_EXECUTE_CODE]=SCP_FLORA_RSA;
  mode[COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_LOAD_CODE]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_LOAD_FILE]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_LOAD_DATA]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_VERIFY_FILE]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_VERIFY_CODE]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_VERIFY_DATA]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_WRITE_REGISTER]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_READ_REGISTER]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_ENGAGE_PLLO]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE]=MSP_MAXQ1852_ECDSA;
  mode[COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE]=MSP_MAXQ1852_ECDSA;
}

void define_pp(void)
{
  int i;
  for(i=0;i<MAX_IDF;i++)
    list_pp[i]=0;
  list_pp[SCP_PP_CLEAR]=list_pp[SCP_PP_RMAC]=list_pp[SCP_PP_E_RMAC]=list_pp[SCP_PP_CMAC]=list_pp[SCP_PP_E_CMAC]=1;
  strcpy(idf_pp[SCP_PP_CLEAR],"CLEAR");
  strcpy(idf_pp[SCP_PP_RMAC],"RMAC");
  strcpy(idf_pp[SCP_PP_E_RMAC],"ENC-RMAC");
  strcpy(idf_pp[SCP_PP_CMAC],"CMAC");
  strcpy(idf_pp[SCP_PP_E_CMAC],"ENC-CMAC");
  strcpy(idf_pp[SCP_PP_RSA],"RSA");
  strcpy(idf_pp[SCP_PP_ECDSA],"ECDSA");
}

int included(int value,int *list)
{
  if(value<MAX_IDF)
    {
      if(list[value]==0)
	return(ERROR);
      else
	return(OK);
    }
  else
    return(ERROR);
}


int init_keys(void)
{
  int i;
  memcpy(keya,config_struct.fka,16);
  memcpy(keyc,config_struct.fkc,16);
  memcpy(keys,config_struct.fks,16);
  if(TRUE==verbose)
    {
      puts("");
      printf("----------\n");
      printf("KA:");
      for(i=0;i<16;i++)
	printf("%02x",keya[i]);
      printf("\n");
      printf("KC:");
      for(i=0;i<16;i++)
	printf("%02x",keyc[i]);
      printf("\n");
      printf("KS:");
      for(i=0;i<16;i++)
	printf("%02x",keys[i]);
      printf("\n");
      printf("----------\n");
      printf("USN:");
      for(i=0;i<16;i++)
	printf("%02x",config_struct.usn[i]);
      printf("\n");
    }
  return(OK);
}

int ecdsa_sign_payload(void)
{
  unsigned char a[]={0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC};
    //  unsigned char b[]={0x5A,0xC6,0x35,0xD8,0xAA,0x3A,0x93,0xE7,0xB3,0xEB,0xBD,0x55,0x76,0x98,0x86,0xBC,0x65,0x1D,0x06,0xB0,0xCC,0x53,0xB0,0xF6,0x3B,0xCE,0x3C,0x3E,0x27,0xD2,0x60,0x4B};
  unsigned char xg[]={0x6B,0x17,0xD1,0xF2,0xE1,0x2C,0x42,0x47,0xF8,0xBC,0xE6,0xE5,0x63,0xA4,0x40,0xF2,0x77,0x03,0x7D,0x81,0x2D,0xEB,0x33,0xA0,0xF4,0xA1,0x39,0x45,0xD8,0x98,0xC2,0x96};
  unsigned char yg[]={0x4F,0xE3,0x42,0xE2,0xFE,0x1A,0x7F,0x9B,0x8E,0xE7,0xEB,0x4A,0x7C,0x0F,0x9E,0x16,0x2B,0xCE,0x33,0x57,0x6B,0x31,0x5E,0xCE,0xCB,0xB6,0x40,0x68,0x37,0xBF,0x51,0xF5};
  unsigned char n[]={0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xBC,0xE6,0xFA,0xAD,0xA7,0x17,0x9E,0x84,0xF3,0xB9,0xCA,0xC2,0xFC,0x63,0x25,0x51};

  unsigned char p[]={0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};

  //RFC4754 test vector
  //secret key
  unsigned char d3[]={0xDC,0x51,0xD3,0x86,0x6A,0x15,0xBA,0xCD,0xE3,0x3D,0x96,0xF9,0x92,0xFC,0xA9,0x9D,0xA7,0xE6,0xEF,0x09,0x34,0xE7,0x09,0x75,0x59,0xC2,0x7F,0x16,0x14,0xC8,0x8A,0x7F};
  //message
  unsigned char msg3[]={'a','b','c'};
   //public key
 unsigned char xq3[]={0x24,0x42,0xA5,0xCC,0x0E,0xCD,0x01,0x5F,0xA3,0xCA,0x31,0xDC,0x8E,0x2B,0xBC,0x70,0xBF,0x42,0xD6,0x0C,0xBC,0xA2,0x00,0x85,0xE0,0x82,0x2C,0xB0,0x42,0x35,0xE9,0x70};
 unsigned char yq3[]={0x6F,0xC9,0x8B,0xD7,0xE5,0x02,0x11,0xA4,0xA2,0x71,0x02,0xFA,0x35,0x49,0xDF,0x79,0xEB,0xCB,0x4B,0xF2,0x46,0xB8,0x09,0x45,0xCD,0xDF,0xE7,0xD5,0x09,0xBB,0xFD,0x7D};
  //signature for the message above
 unsigned char r3[]={0xCB,0x28,0xE0,0x99,0x9B,0x9C,0x77,0x15,0xFD,0x0A,0x80,0xD8,0xE4,0x7A,0x77,0x07,0x97,0x16,0xCB,0xBF,0x91,0x7D,0xD7,0x2E,0x97,0x56,0x6E,0xA1,0xC0,0x66,0x95,0x7C};
 unsigned char s3[]={0x86,0xFA,0x3B,0xB4,0xE2,0x6C,0xAD,0x5B,0xF9,0x0B,0x7F,0x81,0x89,0x92,0x56,0xCE,0x75,0x94,0xBB,0x1E,0xA0,0xC8,0x92,0x12,0x74,0x8B,0xFF,0x3B,0x3D,0x5B,0x03,0x15};

  u8 input[MAX_STRING];
  int inputsize;

  int i;
  int resu;
  //verify the KAT

#ifdef _MXIM_HSM
  	u8 signature[UCL_RSA_KEY_MAXSIZE];
	int l_iSignatureLength=UCL_RSA_KEY_MAXSIZE;
	unsigned long l_ulAttributeKeyType = CKA_LABEL;
	unsigned long l_ulHSMLabelKeyLength = strlen(g_tcHSMECDSALabelKey);
#endif	

#ifdef _MXIM_HSM
  resu=g_objMXIMUCLLibrary.ECDSAVerifyP256r1Sha256(32,xg,yg,xq3,yq3,r3,s3,a,n,p,msg3,sizeof(msg3));
#else
  resu=ucl_ecdsa_verify_p256r1_sha256(32,xg,yg,xq3,yq3,r3,s3,a,n,p,msg3,sizeof(msg3));
#endif

  if(TRUE==verbose)
    {
      if(resu==UCL_OK)
	printf("KAT ECDSA-P256r1-SHA256 SIGNATURE VERIFICATION TEST-1 OK\n");
      else
	printf("KAT ECDSA-P256r1-SHA256 SIGNATURE VERIFICATION TEST-1 NOK %d \n",resu);
    }
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    d3[i]=config_struct.ecdsa_privkey[i];
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    xq3[i]=config_struct.ecdsa_pubkey_x[i];
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
  yq3[i]=config_struct.ecdsa_pubkey_y[i];
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      inputsize=ipayload-4;
      memcpy(input,&(payload[4]),inputsize);
    }
  else
    if(MSP_MAXQ1852_ECDSA==session_mode)
    {
      inputsize=ipayload;
      memcpy(input,payload,inputsize);
    }
    else
      return(EXIT_FAILURE);
#ifdef _MXIM_HSM

  resu=MXIMHSMSHA256ECDSASign(	&g_objMXHSMCLI,
				(PUCHAR)input,
				(PULONG)&inputsize,
				&l_ulAttributeKeyType,
				(PUCHAR)g_tcHSMECDSALabelKey,
				&l_ulHSMLabelKeyLength,
				(PUCHAR)signature, 
				(PULONG)&l_iSignatureLength);
  if(resu!=UCL_OK)
    {
      printf("ERROR on ECDSA sha256 sign (%d)\n",resu);
      return(EXIT_FAILURE);
    }	
  for(i=0;i<64;i++)
    {	
      if(i<32)
	{
	  r3[i] = signature[i];
	}
      else
	{
	  s3[i-32] = signature[i];
	}
    }

#else
  resu=ucl_ecdsa_sign_p256r1_sha256(32,xg,yg,xq3,yq3,r3,s3,a,n,p,d3,input,inputsize);
#endif

  if(resu!=UCL_OK)
    {
      printf("ECDSA-P256r1-SHA256 SIGNATURE COMPUTATION TEST-1 NOK %d \n",resu);
      exit(0);
    }
#ifdef _MXIM_HSM
  
  resu = MXIMHSMSHA256ECDSAVerify(	&g_objMXHSMCLI,
					(PUCHAR)input,
					(PULONG)&inputsize,
					&l_ulAttributeKeyType,
					(PUCHAR)g_tcHSMECDSALabelKey,
					&l_ulHSMLabelKeyLength,
					(PUCHAR)signature, 
					(ULONG)l_iSignatureLength);
  if(resu!=UCL_OK)
    {
      printf("ERROR on ECDSA sha256 verify (%d)\n",resu);
      return(EXIT_FAILURE);
    }
#else
  resu=ucl_ecdsa_verify_p256r1_sha256(32,xg,yg,xq3,yq3,r3,s3,a,n,p,input,inputsize);
#endif
  if(resu!=UCL_OK)
    {
      printf("ECDSA-P256r1-SHA256 SIGNATURE VERIFICATION TEST-1 NOK %d \n",resu);
      exit(0);
    }
  else
    if(TRUE==verbose)
      printf("ECDSA-P256r1-SHA256 SIGNATURE VERIFICATION TEST-1 OK %d \n",resu);
  //adding computed signature to the payload
  if(TRUE==verbose)
    {
      printf("payload(%d):",inputsize);
      for(i=0;i<inputsize;i++)
	printf("%02x",input[i]);
      printf("\n");
      printf("r3:");
      for(i=0;i<32;i++)
	printf("%02x",r3[i]);
      printf("\n");
      printf("s3:");
      for(i=0;i<32;i++)
	printf("%02x",s3[i]);
      printf("\n");
    }
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      //3.7.2
      for(i=0;i<ECDSA_MODULUS_LEN;i++)
	payload[ipayload++]=r3[i];
      //3.7.2
      for(i=0;i<ECDSA_MODULUS_LEN;i++)
	payload[ipayload++]=s3[i];
    }
  if(MSP_MAXQ1852_ECDSA==session_mode)
    {
      for(i=0;i<ECDSA_MODULUS_LEN;i++)
	payload[ipayload++]=r3[ECDSA_MODULUS_LEN-1-i];
      for(i=0;i<ECDSA_MODULUS_LEN;i++)
	payload[ipayload++]=s3[ECDSA_MODULUS_LEN-1-i];
    }
  if(TRUE==verbose)
    {
      printf("payload+signature:");
      for(i=0;i<ipayload;i++)
	printf("%02x",payload[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}
  
int aes_checksum(u8 *crc,u8 *data,int size, int trunk)
{
  int i,j;
  u8 keynull[16];
  u8 h[16];
  int resu;
  u8 input[16];
  for(i=0;i<16;i++)
    h[i]=keynull[i]=0;
  for(i=0;i<size;i+=16)
    {
      for(j=0;j<16;j++)
	if(i+j<size)
	  input[j]=h[j]^data[i+j];
	else
	  {
	    //for SBL, for bytes out of size, stuffing is made with h
	    //	    if(SBL==session_mode)
	      input[j]=h[j];
	      //	    else
	      //for SCP, stuffing is made with 0 ? or not ? to be clarified...
	      //input[j]=0;
	  }

#ifdef _MXIM_HSM
	resu=g_objMXIMUCLLibrary.AESECB(h,input,16,keynull,16,UCL_CIPHER_ENCRYPT);
#else
      resu=ucl_aes_ecb(h,input,16,keynull,16,UCL_CIPHER_ENCRYPT);
#endif

      if(resu!=UCL_OK)
	{
	  printf("ERROR AES\n");
	  return(resu);
	}
    }
  for(i=0;i<trunk;i++)
    crc[i]=h[i];
  return(UCL_OK);
}

void init(void)
{
  int err=0;
  init_keys();
  define_ctl();
  define_cmd();
  define_pp();
  define_const();
  define_scp_cmd();

#ifdef _MXIM_HSM
  //-- DR COMMENT 13112014 1115 err=g_objMXIMUCLLibrary.Init(init_buffer, 2048,true);
  err=g_objMXIMUCLLibrary.Init(init_buffer, 2048);
  compteur=0;
  if(err!=UCL_OK)
    {
      printf("ERROR for ucl_init %d\n",err);
    }
  if(TRUE==verbose)
    printf("UCL Version: %s (%s)\n", (char *)g_objMXIMUCLLibrary.GetVersion(),(char *)g_objMXIMUCLLibrary.GetBuildDate());
#else
  err = ucl_init(init_buffer, 2048);
  compteur=0;
  if(err!=UCL_OK)
    {
      printf("ERROR for ucl_init %d\n",err);
    }
  if(TRUE==verbose)
    {
      printf("UCL Version: %s (%s)\n", (char *)ucl_get_version(),(char *)ucl_get_build_date());
    }
#endif//MXIM_HSM
}

void display_frame(void)
{
  int i;
  if(iframe!=0)
    {
      if(HOST==who)
	{
	  if(TRUE==verbose)
	    printf("<host>.%07d.%s\n",compteur,message);
	  fprintf(fp,"<host>.%07d.%s\n",compteur,message);
	}
      else
	{
	  if(TRUE==verbose)
	    printf("<chip>.%07d.%s\n",compteur,message);
	  fprintf(fp,"<chip>.%07d.%s\n",compteur,message);
	}
      if(TRUE==verbose)
	{
	  for(i=0;i<iframe;i++)
	    printf("%02x",frame[i]);
	  printf("\n");
	}
      for(i=0;i<iframe;i++)
	fprintf(fp,"%02x",frame[i]);
      fprintf(fp,"\n");
    }
}

void host(void)
{
  who=HOST;
}

//for historical reason, the chip is named USIP
//so, this function should be changed, because we now support JIBE, LONDA, MAXQ1852
//anyway, its purpose is mainly to say "not HOST" !
void usip(void)
{
  who=USIP;
}

int display_bin(void)
{
  FILE *fp;
  char name[MAX_STRING];
  int i;
  sprintf(name,"%s.%07d.%s.%s.packet",output_file,compteur,source[who],name_file);
  fp=fopen(name,"wb");
  if(NULL==fp)
    {
      printf("ERROR while opening <%s>\n",name);
      return(EXIT_FAILURE);
    }
  for(i=0;i<iframe;i++)
    fprintf(fp,"%c",frame[i]);
  (void)fclose(fp);
  if(TRUE==verbose)
    printf("<%s> created\n",name);
  return(EXIT_SUCCESS);
}

void send(void)
{
  compteur++;
  display_frame();
  display_bin();
}

void synchro(void)
{
  iframe=0;
  frame[iframe++]=SYNCH1;
  frame[iframe++]=SYNCH2;
  frame[iframe++]=SYNCH3;
}

int extension(char *ext,char *name)
{
  int i;
  char name1[MAXLINE];
  char ext1[MAXLINE];
  for(i=0;i<(int)strlen(ext);i++)
    ext1[i]=(char)toupper((int)ext[i]);
  ext1[strlen(ext)]='\0';
  for(i=0;i<(int)strlen(name);i++)
    name1[i]=(char)toupper((int)name[i]);
  name1[strlen(name)]='\0';
  if(strstr(name1,ext1)!=NULL)
    return(EXIT_SUCCESS);
  else
    return(EXIT_FAILURE);
}

int read_hex(char *hexfilename)
{
  FILE *fp;
  char line[MAXLINE];
  int nb_bytes;
  int i;
  int line_length;
  int line_addr;
  fp=fopen(hexfilename,"r");
  if(fp==NULL)
    {
      printf("ERROR: <%s> not found\n",hexfilename);
      return(EXIT_FAILURE);
    }
  nb_bytes=0;
  data_len=0;
  hex_extended_address=-1;
  while(fscanf(fp,"%s",line)!=EOF)
    {
      if(MAXLINE<strlen(line))
	{
	  printf("ERROR: line too long: %d chars, while limited to %d\n",strlen(line),MAXLINE);
	  return(EXIT_FAILURE);
	}
      if(line[0]==HEX_START_CHAR)
	{
	  //for each new line, check the record type is 00, so these are data
	  if('0'==line[HEX_RECORD_TYPE_POS1] && '0'==line[HEX_RECORD_TYPE_POS2])
	    {
	      //retrieve the address, stored in HEX_ADDRESS_START..HEX_ADDRESS_END
	      for(line_addr=0,i=HEX_ADDRESS_START;i<HEX_ADDRESS_END;i+=2)
		if(EXIT_SUCCESS==test_hex(line[i],line[i+1]))
		  line_addr=(line_addr<<8)+hex(line[i],line[i+1]);
		else
		  {
		    printf("ERROR: non hexa char detected in #%d <%c%c>\n",i,line[i],line[i+1]);
		    return(EXIT_FAILURE);
		  }
	      //	      printf("line address=%04x ",line_addr);
	      // *2 as a byte length and not a char length
	      if(EXIT_SUCCESS==test_hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]))
		line_length=hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2])*2;
	      else
		{
		  printf("ERROR: non hexa char detected in #%d <%c%c>\n",HEX_LINE_LEN_POS1,line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]);
		  return(EXIT_FAILURE);
		}
	      //	      printf("line length=%d\n ",line_length);
	      //read and store data bytes
	      //i is the position in the line, so expressed in char
	      if(TRUE==verbose)
		printf("\n@=%04x ",line_addr);
	      for(addr[data_len]=line_addr,i=0;i<line_length;i+=2,data_len++)
		{
		  if(EXIT_SUCCESS==test_hex(line[HEX_DATA_START+i],line[HEX_DATA_START+i+1]))
		    {
		      data[data_len]=hex(line[HEX_DATA_START+i],line[HEX_DATA_START+i+1]);
		      if(TRUE==verbose)
			printf("%02x",data[data_len]);
		    }
		  else
		    {
		      printf("ERROR: non hexa char detected in #%d <%c%c>\n",HEX_DATA_START+i,line[HEX_DATA_START+i],line[HEX_DATA_START+i+1]);
		      return(EXIT_FAILURE);
		    }
		  //		  printf("%02x (%04x)",data[data_len],addr[data_len]);
		  addr[data_len+1]=addr[data_len]+1;
		  if(data_len>=max_data_size)
		    {
		      printf("ERROR: hex file <%s> is too large (limited to %dMB)\n",hexfilename,config_struct.flash_mb);
		      return(EXIT_FAILURE);
		    }
		}
	      //	      printf("\n");
	      //compute total nb of bytes of data in the hex file
	      //not counting address and crc
	      if(EXIT_SUCCESS==test_hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]))
		nb_bytes+=hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]);
	      else
		{
		  printf("ERROR: non hexa char detected in #%d <%c%c>\n",HEX_LINE_LEN_POS1,line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]);
		  return(EXIT_FAILURE);
		}
	    }
	  else
	    //this is an extended address line
	    if('0'==line[HEX_RECORD_TYPE_POS1] && '4'==line[HEX_RECORD_TYPE_POS2])
	      {
		// *2 as a byte length and not a char length
		if(EXIT_SUCCESS==test_hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]))
		  line_length=hex(line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2])*2;
		else
		  {
		    printf("ERROR: non hexa char detected in #%d <%c%c>\n",HEX_LINE_LEN_POS1,line[HEX_LINE_LEN_POS1],line[HEX_LINE_LEN_POS2]);
		    return(EXIT_FAILURE);
		    //		    printf("line length (hex-digits)=%d\n",line_length);
		  }
		//retrieve the extended address from the data
		//i is the position in the line, so expressed in char
		for(hex_extended_address=0,i=0;i<line_length;i+=2)
		  {
		    if(EXIT_SUCCESS==test_hex(line[HEX_ADDRESS_START+i],line[HEX_ADDRESS_START+i+1]))
		      hex_extended_address=(hex_extended_address<<8)^(hex(line[HEX_ADDRESS_START+i],line[HEX_ADDRESS_START+i+1]));
		    else
		      {
			printf("ERROR: non hexa char detected in #%d <%c%c>\n",HEX_ADDRESS_START+i,line[HEX_ADDRESS_START+i],line[HEX_ADDRESS_START+i+1]);
			return(EXIT_FAILURE);
		      }
		  }
		printf("extended-address=%08x\n",hex_extended_address);
	      }
	}
      else
	{
	  printf("ERROR: unexpected char <%c>\n",line[HEX_START_CHAR]);
	  return(EXIT_FAILURE);
	}
    }
  if(-1==hex_extended_address)
    {
      printf("ERROR: extended address not initialized\n");
      hex_extended_address=0;
      return(EXIT_FAILURE);
    }
  fprintf(fp,"%d==%d bytes\n",data_len,nb_bytes);
  fprintf(fp,"nb of write-mem packets: %.0f\n",1.0*data_len/(chunk_size));
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

int read_s19(char *s19filename,char *ptr_address_offset)
{
  FILE *fp;
  char line[MAXLINE];
  int nb_bytes;
  int i;
  int line_length;
  int line_addr;
  UNUSED_PARAMETER(ptr_address_offset);
  fp=fopen(s19filename,"r");
  if(fp==NULL)
    {
      printf("ERROR: <%s> not found\n",s19filename);
      return(EXIT_FAILURE);
    }
  nb_bytes=0;
  data_len=0;
  while(fscanf(fp,"%s",line)!=EOF)
    {
      if(MAXLINE<strlen(line))
	{
	  printf("ERROR: line too long: %d chars, while limited to %d\n",strlen(line),MAXLINE);
	  return(EXIT_FAILURE);
	}
      if(line[0]==S19_WDATA_CHAR1 && line[1]==S19_WDATA_CHAR2)
	{
	  //for each new line, get the starting address of the line
	  //which may be different, non contiguous with the previous line
	  for(line_addr=0,i=S19_ADDRESS_START;i<S19_ADDRESS_START+2*S19_ADDRESS_LEN;i+=2)
	    if(EXIT_SUCCESS==test_hex(line[i],line[i+1]))
	      line_addr=(line_addr<<8)+hex(line[i],line[i+1]);
	    else
	      {
		printf("ERROR: non hexa char detected in #%d <%c%c>\n",i,line[i],line[i+1]);
		return(EXIT_FAILURE);
	      }
	  line_addr^=address_offset;
	  // *2 as a byte length and not a char length
	  if(EXIT_SUCCESS==test_hex(line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2]))
	    line_length=hex(line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2])*2;
	  else
	    {
	      printf("ERROR: non hexa char detected in #%d <%c%c>\n",S19_LINE_LEN_POS1,line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2]);
	      return(EXIT_FAILURE);
	    }
	  //read and store data bytes
	  //i is the position in the line, so expressed in char
	  for(addr[data_len]=line_addr,i=0;i<line_length-S19_ADDRESS_LEN*2-S19_CRC_LEN*2;i+=2,data_len++)
	    {
	      if(EXIT_SUCCESS==test_hex(line[S19_DATA_START+i],line[S19_DATA_START+i+1]))
		data[data_len]=hex(line[S19_DATA_START+i],line[S19_DATA_START+i+1]);
	      else
		{
		  printf("ERROR: non hexa char detected in #%d <%c%c>\n",S19_DATA_START+i,line[S19_DATA_START+i],line[S19_DATA_START+i+1]);
		  return(EXIT_FAILURE);
		}
	      addr[data_len+1]=addr[data_len]+1;
	      if(data_len>=max_data_size)
		{
		  printf("ERROR: s19 file <%s> is too large (limited to %dMB)\n",s19filename,config_struct.flash_mb);
		  return(EXIT_FAILURE);
		}
	    }
	      //compute total nb of bytes of data in the s19 file
	  //not counting address and crc
	  if(EXIT_SUCCESS==test_hex(line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2]))
	     nb_bytes+=hex(line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2])-S19_ADDRESS_LEN-S19_CRC_LEN;
	  else
	    {
	      printf("ERROR: non hexa char detected in #%d <%c%c>\n",S19_LINE_LEN_POS1,line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2]);
	      return(EXIT_FAILURE);
	    }
	}
    }
  if(TRUE==verbose)
    {
      last_packet_len=data_len % (chunk_size);
      last_packet_len=((last_packet_len/16)+1)*16;
      if(TRUE==verbose)
	{
	  printf("last packet:%d\n",last_packet_len);
	//  for(i=0;i<last_packet_len;i++)
	//    printf("%02x",data[i+(data_len/chunk_size)*chunk_size]);
	  printf("\n");
	  printf("%d==%d bytes\n",data_len,nb_bytes);
	  printf("nb of write-mem packets: %.0f\n",1.0*data_len/(chunk_size));
	}
  }
  fprintf(fp,"%d==%d bytes\n",data_len,nb_bytes);
  fprintf(fp,"nb of write-mem packets: %.0f\n",1.0*data_len/(chunk_size));
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

int read_s20(char *s20filename,char *ptr_start_address)
{
  FILE *fp;
  char line[MAXLINE];
  int nb_bytes;
  int i;
  int line_length;
  int line_addr;
  UNUSED_PARAMETER(ptr_start_address);
  fp=fopen(s20filename,"r");
  if(fp==NULL)
    {
      printf("ERROR: <%s> not found\n",s20filename);
      return(EXIT_FAILURE);
    }
  nb_bytes=0;
  data_len=0;
  while(fscanf(fp,"%s",line)!=EOF)
    {
      if(MAXLINE<strlen(line))
	{
	  printf("ERROR: line too long: %d chars, while limited to %d\n",strlen(line),MAXLINE);
	  return(EXIT_FAILURE);
	}
      if(line[0]==S20_WDATA_CHAR1 && line[1]==S20_WDATA_CHAR2)
	{
	  //for each new line, get the starting address of the line
	  //which may be different, non contiguous with the previous line
	  for(line_addr=0,i=S20_ADDRESS_START;i<S20_ADDRESS_START+2*S20_ADDRESS_LEN;i+=2)
	    if(EXIT_SUCCESS==test_hex(line[i],line[i+1]))
	      line_addr=(line_addr<<8)+hex(line[i],line[i+1]);
	    else
	      {
		printf("ERROR: non hexa char detected in #%d <%c%c>\n",i,line[i],line[i+1]);
		return(EXIT_FAILURE);
	      }
	  line_addr^=address_offset;
	  // *2 as a two-byte length (we are in s20) and not a char length
	  if(EXIT_SUCCESS==test_hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2])&& EXIT_SUCCESS==test_hex(line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4]))
	    line_length=(hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2])*256+hex(line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4]))*2;
	  else
	    {
	      printf("ERROR: non hexa char detected in <%c%c><%c%c>\n",line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2],line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4]);
	      return(EXIT_FAILURE);
	    }
	  //read and store data bytes
	  //i is the position in the line, so expressed in char
	  for(addr[data_len]=line_addr,i=0;i<line_length-S20_ADDRESS_LEN*2-S20_CRC_LEN*2;i+=2,data_len++)
	    {
	      if(EXIT_SUCCESS==test_hex(line[S20_DATA_START+i],line[S20_DATA_START+i+1]))
		data[data_len]=hex(line[S20_DATA_START+i],line[S20_DATA_START+i+1]);
	      else
		{
		  printf("ERROR: non hexa char detected in #%d <%c%c>\n",S20_DATA_START+i,line[S20_DATA_START+i],line[S20_DATA_START+i+1]);
		  return(EXIT_FAILURE);
		}
	      addr[data_len+1]=addr[data_len]+1;
	      if(data_len>=max_data_size)
		{
		  printf("ERROR: s20 file <%s> is too large (limited to %dMB)\n",s20filename,config_struct.flash_mb);
		  return(EXIT_FAILURE);
		}
	    }
	  //compute total nb of bytes of data in the s20 file
	  //not counting address and crc
	  if(EXIT_SUCCESS==test_hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2]) && EXIT_SUCCESS==test_hex(line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4]))
	    nb_bytes+=hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2])*256+hex(line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4])-S20_ADDRESS_LEN-S20_CRC_LEN;
	  else
	    {
	      printf("ERROR: non hexa char detected in <%c%c><%c%c>\n",line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2],line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4]);
	      return(EXIT_FAILURE);
	    }
	}
    }
  if(TRUE==verbose)
    {
      last_packet_len=data_len % (chunk_size);
      if(TRUE==verbose)
	printf("last packet:%d\n",last_packet_len);
      last_packet_len=((last_packet_len/16)+1)*16;
      if(TRUE==verbose)
	{
	  printf("last packet:%d\n",last_packet_len);
	  for(i=0;i<last_packet_len;i++)
	    printf("%02x",data[i+(data_len/chunk_size)*chunk_size]);
	  printf("\n");
	  printf("%d==%d bytes\n",data_len,nb_bytes);
	  printf("nb of write-mem packets: %.0f\n",1.0*data_len/(chunk_size));
	}
  }
  fprintf(fp,"%d==%d bytes\n",data_len,nb_bytes);
  fprintf(fp,"nb of write-mem packets: %.0f\n",1.0*data_len/(chunk_size));
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

void con_req(void)
{
  frame[iframe++]=CON_REQ;
}

void con_rep(void)
{
  frame[iframe++]=CON_REP;
}

void discon_req(void)
{
  frame[iframe++]=DISC_REQ;
}

void discon_rep(void)
{
  frame[iframe++]=DISC_REP;
}

void add_byte(u8 value)
{
  frame[iframe++]=value;
}

void add_channel_id_seq(void)
{
  frame[iframe++]=(ch_id<<4)+(seq&15);
}

void header_crc(void)
{
  u8 crc[16];
  aes_checksum(crc,frame,iframe,1);
  frame[iframe++]=crc[0];
}

int connection_request(void)
{
  sprintf(message,"%s",idf_ctl[1]);
  synchro();
  con_req();
  //len
  add_byte(0x00);
  add_byte(0x00);

  add_channel_id_seq();
  header_crc();
  sprintf(name_file,"connection_request");
  send();
  return(EXIT_SUCCESS);
}

int connection_reply(void)
{
  sprintf(message,"%s",idf_ctl[2]);
  synchro();
  con_rep();
  //len
  add_byte(0x00);
  add_byte(0x00);

  add_channel_id_seq();
  header_crc();
  sprintf(name_file,"connection_reply");
  send();
  return(EXIT_SUCCESS);
}

int disconnection_request(void)
{
  sprintf(message,"%s",idf_ctl[3]);
  seq++;
  synchro();
  discon_req();
  //len
  add_byte(0x00);
  add_byte(0x00);

  add_channel_id_seq();
  header_crc();
  sprintf(name_file,"disconnection_request");
  send();
  return(EXIT_SUCCESS);
}

int disconnection_reply(void)
{
  sprintf(message,"%s",idf_ctl[4]);
  synchro();
  discon_rep();
  //len
  add_byte(0x00);
  add_byte(0x00);

  add_channel_id_seq();
  header_crc();
  sprintf(name_file,"disconnection_reply");
  send();
  return(EXIT_SUCCESS);
}

void ack_code(void)
{
  frame[iframe++]=ACK;
}

int ack(void)
{
  sprintf(message,"%s",idf_ctl[6]);
  synchro();
  ack_code();
  //len
  add_byte(0x00);
  add_byte(0x00);

  add_channel_id_seq();
  header_crc();
  sprintf(name_file,"ack");
  send();
  return(EXIT_SUCCESS);
}

void data_code(void)
{
  frame[iframe++]=DATA_TRANSFER;
}

int crypto_aes_cmac(u8 *mac, u32 mac_byteLen,u8 *key,  u8 *dataIn, u32 byteLen)
{
  u8 null_data[UCL_AES_BLOCKSIZE];
  u8 resu[UCL_AES_BLOCKSIZE];
  u8 k1[16];
  u8 k2[16];
  u8 l[UCL_AES_BLOCKSIZE];
  u8 block[UCL_AES_BLOCKSIZE];
  u8 memory[UCL_AES_BLOCKSIZE];
  int i,j;
  if(mac==NULL || dataIn==NULL || key==NULL)
    return(UCL_INVALID_INPUT);
  if((byteLen%UCL_AES_BLOCKSIZE)!=0)
    return(UCL_INVALID_ARG);
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    null_data[i]=0;
  //subkeys computation
#ifdef _MXIM_HSM
  int* l_piRslt = (int*)resu;
  
  *l_piRslt=g_objMXIMUCLLibrary.AESECB(l,null_data,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#else
  ucl_aes_ecb(l,null_data,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#endif

  for(i=0;i<UCL_AES_BLOCKSIZE-1;i++)
    k1[i]=(l[i]<<1)^(l[i+1]>>7);
  k1[UCL_AES_BLOCKSIZE-1]=(l[UCL_AES_BLOCKSIZE-1]<<1)&0xFF;
  //xor with Rb
    if(l[0]>>7)
      k1[UCL_AES_BLOCKSIZE-1]^=0x87;
  for(i=0;i<UCL_AES_BLOCKSIZE-1;i++)
    k2[i]=(k1[i]<<1)^(k1[i+1]>>7);
  k2[UCL_AES_BLOCKSIZE-1]=(k1[UCL_AES_BLOCKSIZE-1]<<1)&0xFF;
  if(k1[0]>>7)
    k2[UCL_AES_BLOCKSIZE-1]^=0x87;
  //----------------------------------------
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    memory[i]=0;
  for(i=0;i<(int)(byteLen-UCL_AES_BLOCKSIZE);i+=UCL_AES_BLOCKSIZE)
    {
      for(j=0;j<UCL_AES_BLOCKSIZE;j++)
	block[j]=dataIn[j+i]^memory[j];

#ifdef _MXIM_HSM 
      l_piRslt = (int*)resu;
      *l_piRslt=g_objMXIMUCLLibrary.AESECB(resu,block,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#else
      ucl_aes_ecb(resu,block,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#endif
      for(j=0;j<UCL_AES_BLOCKSIZE;j++)
	memory[j]=resu[j];
    }
  for(j=0;j<UCL_AES_BLOCKSIZE;j++)
    block[j]=dataIn[byteLen-UCL_AES_BLOCKSIZE+j]^k1[j]^memory[j];

#ifdef _MXIM_HSM 
  l_piRslt = (int*)resu;
  *l_piRslt=g_objMXIMUCLLibrary.AESECB(resu,block,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#else
  ucl_aes_ecb(resu,block,UCL_AES_BLOCKSIZE,key,UCL_AES_BLOCKSIZE,UCL_CIPHER_ENCRYPT);
#endif

  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    mac[i]=0;
  for(i=0;i<(int)mac_byteLen;i++)
    mac[i]=resu[i];
  return(UCL_OK);
}

int hello_request_payload(void)
{
  int i;
  if(SBL==session_mode)
    {
      payload[ipayload++]=HELLO_REQ<<4;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x08;
      for(i=0;i<HELLO_REQ_CONST_LEN;i++)
	payload[ipayload++]=hello_req_const[i];
    }
  else
    {
      payload[ipayload++]=HELLO_REQ<<4;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x0A;
      for(i=0;i<HELLO_SCP_REQ_CONST_LEN;i++)
	payload[ipayload++]=hello_scp_req_const[i];
      //from the specs, the hello are the same for these two modes
      if(SCP_ON_AES==session_mode || SCP_FLORA_AES==session_mode)
	payload[ipayload-1]=0x00;
      if(SCP_OFF_AES==session_mode)
	payload[ipayload-1]=0x01;
      //from the specs, the hello are the same for these two modes
      if(SCP_RSA==session_mode || SCP_FLORA_RSA==session_mode)
	payload[ipayload-1]=0x02;
      if(SCP_ANGELA_ECDSA==session_mode)
	payload[ipayload-1]=0x03;
      //Admin mode
      //alway used for SCP_FLORA
      payload[ipayload++]=0x02;
    }
  return(EXIT_SUCCESS);
}

int hello_reply_payload(void)
{
  int i;
  if(SBL==session_mode)
    {
      payload[ipayload++]=HELLO_REP<<4;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x2E;
      for(i=0;i<HELLO_REP_CONST_LEN;i++)
	payload[ipayload++]=hello_rep_const[i];
      payload[ipayload++]=0x04;
      payload[ipayload++]=0x03;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x03;
      payload[ipayload++]=0x00;
      payload[ipayload++]=0x03;
      payload[ipayload++]=0x00;
      for(i=0;i<config_struct.usn_len;i++)
	payload[ipayload++]=config_struct.usn[i];
      for(i=0;i<16;i++)
	payload[ipayload++]=rand()&255;
    }
  else
    if(SCP_ON_AES==session_mode || SCP_FLORA_AES==session_mode)
      {
	payload[ipayload++]=HELLO_REP<<4;
	payload[ipayload++]=0x00;
	payload[ipayload++]=0x00;
	payload[ipayload++]=0x32;
	for(i=0;i<HELLO_SCP_REP_CONST_LEN;i++)
	  payload[ipayload++]=hello_scp_rep_const[i];
	if(SCP_FLORA_AES==session_mode)
	  {
	    //flora major version one byte
	    payload[ipayload++]=0x00;
	    //flora minor version one byte
	    payload[ipayload++]=0x00;
	    // 4 rfu bytes
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x00;
	    //0x00 byte
	    payload[ipayload++]=0x00;
	    //configuration
	    payload[ipayload++]=0x01;
	  }
	else
	  {
	    // bug #1621 correction
	    //major version number, on 4 bytes
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x01;
	    //rfu byte, 0x00
	    payload[ipayload++]=0x00;
	    //annex identifier
	    payload[ipayload++]=0x00;
	    payload[ipayload++]=0x01;
	    payload[ipayload++]=0x01;
	  }
	//usn
	for(i=0;i<config_struct.usn_len;i++)
	  payload[ipayload++]=config_struct.usn[i];
	//random number
	for(i=0;i<16;i++)
	  payload[ipayload++]=random_number[i];
      }
    else
      if(SCP_OFF_AES==session_mode || SCP_RSA==session_mode || SCP_FLORA_RSA==session_mode || SCP_ANGELA_ECDSA==session_mode)
	{
	  payload[ipayload++]=HELLO_REP<<4;
	  payload[ipayload++]=0x00;
	  payload[ipayload++]=0x00;
	  payload[ipayload++]=0x32;
	  for(i=0;i<HELLO_SCP_REP_CONST_LEN;i++)
	    payload[ipayload++]=hello_scp_rep_const[i];
	  if(SCP_FLORA_RSA==session_mode || SCP_ANGELA_ECDSA==session_mode)
	    {
	      //flora major version, one byte
	      payload[ipayload++]=0x01;
	      //flora minor version, one byte
	      payload[ipayload++]=0x00;
	      //four RFU bytes
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x00;
	      //0x00 byte
	      payload[ipayload++]=0x00;
	      //configuration byte
	      //jtag and rwk enabled
	      payload[ipayload++]=(1<<7)^(1<<6);
	    }
	  else
	    {
	      // bug #1621 correction
	      //major version number, on 4 bytes
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x01;
	      //rfu byte, 0x00
	      payload[ipayload++]=0x00;
	      //annex identifier
	      payload[ipayload++]=0x00;
	      payload[ipayload++]=0x01;
	      payload[ipayload++]=0x01;
	    }
	  //usn
	  for(i=0;i<config_struct.usn_len;i++)
	    payload[ipayload++]=config_struct.usn[i];
	  //for flora modes, pad with 0 up to 16 bytes
	  for(i=config_struct.usn_len;i<16;i++)
	    payload[ipayload++]=0;
	  //random number
	  for(i=0;i<16;i++)
	    payload[ipayload++]=0x00;
	}
      else
	printf("ERROR: session mode not supported yet\n");
  return(EXIT_SUCCESS);
}

void add_payload(void)
{
  int i;
  for(i=0;i<ipayload;i++)
    frame[iframe++]=payload[i];
}

void payload_crc(void)
{
  int i;
  u8 crc[16];
  int resu;
  resu=aes_checksum(crc,payload,ipayload,4);
  if(resu!=UCL_OK)
    printf("error: %d\n",resu);
  for(i=3;i>=0;i--)
    frame[iframe++]=crc[i];
}

int hello_request(void)
{
  ipayload=0;
  hello_request_payload();
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_cmd[1]);
  synchro();
  data_code();
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  header_crc();
  add_payload();
  payload_crc();
  sprintf(name_file,"hello_request");
  send();
  return(EXIT_SUCCESS);
}

int hello_reply(void)
{
  ipayload=0;
  seq++;
  hello_reply_payload();
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_cmd[2]);
  synchro();
  data_code();
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  header_crc();
  add_payload();
  payload_crc();
  sprintf(name_file,"hello_reply");
  send();
  return(EXIT_SUCCESS);
}

int challenge_payload(void)
{
  u8 fixed_random_number[]={0xdc,0xa3,0xae,0x5f,0x69,0x8f,0xb2,0xeb,0xcd,0x99,0x91,0x79,0x98,0x75,0xdd,0x78};
  int i;
  int resu;
  payload[ipayload++]=(CHALLENGE<<4)^config_struct.pp;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x10;
  if(SBL==session_mode)
    {
#ifdef _MXIM_HSM
		resu=g_objMXIMUCLLibrary.AESECB(response,random_number,16,keya,16,UCL_CIPHER_ENCRYPT);
#else
		resu=ucl_aes_ecb(response,random_number,16,keya,16,UCL_CIPHER_ENCRYPT);
#endif

      for(i=0;i<UCL_AES_BLOCKSIZE;i++)
	payload[ipayload++]=response[i];
    }
  else
    if(SCP_ON_AES==session_mode || SCP_FLORA_AES==session_mode)
      {
	// encrypted+cmac
	if(TRUE==verbose)
	  {
	    printf("rn:");
	    for(i=0;i<16;i++)
	      printf("%02x",random_number[i]);
	    printf("\n");
	  }
	random_number[0]=(fixed_random_number[0])^config_struct.pp;
	if(TRUE==verbose)
	  {
	    printf("rn^pp:");
	    for(i=0;i<16;i++)
	      printf("%02x",random_number[i]);
	    printf("\n");
	  }

#ifdef _MXIM_HSM
	resu=g_objMXIMUCLLibrary.AESECB(response,random_number,16,keya,16,UCL_CIPHER_ENCRYPT);
#else
	resu=ucl_aes_ecb(response,random_number,16,keya,16,UCL_CIPHER_ENCRYPT);
#endif

	if(TRUE==verbose)
	  {
	    printf("response:");
	    for(i=0;i<16;i++)
	      printf("%02x",response[i]);
	    printf("\n");
	  }
	for(i=0;i<UCL_AES_BLOCKSIZE;i++)
	  payload[ipayload++]=response[i];
      }
    else
      printf("ERROR: no challenge for this mode\n");
  return(EXIT_SUCCESS);
}

int challenge(void)
{
  ipayload=0;
  seq++;
  challenge_payload();
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_cmd[7]);
  synchro();
  data_code();
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  header_crc();
  add_payload();
  payload_crc();
  sprintf(name_file,"challenge");
  send();
  return(EXIT_SUCCESS);
}

int challenge_response_payload(void)
{
  payload[ipayload++]=SUCCESS<<4;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  return(EXIT_SUCCESS);
}

int challenge_response(void)
{
  ipayload=0;
  seq++;
  challenge_response_payload();
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_cmd[3]);
  synchro();
  data_code();
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  header_crc();
  add_payload();
  payload_crc();
  sprintf(name_file,"challenge_response");
  send();
  return(EXIT_SUCCESS);
}

int padding(int *size,u8 *input)
{
  int i;
  i=ipayload-4;
  while((i%16)!=0)
    input[i++]=0;
  (*size)=i;
  return(EXIT_SUCCESS);
}

int aes_encrypt_payload(void)
{
  int i;
  u8 output[MAX_STRING];
  u8 input[MAX_STRING];
  int inputsize;
  int resu;
  //copy payload
  memcpy(input,payload,ipayload);
  padding(&inputsize,input);
  if(TRUE==verbose)
    {
      printf("INFO: plain payload:");
      for(i=0;i<inputsize;i++)
	printf("%02x",input[i]);
      printf("\n");
    }
  //encrypt it with key-c
#ifdef _MXIM_HSM
  resu=g_objMXIMUCLLibrary.AESECB(output,input,16,keyc,inputsize,UCL_CIPHER_ENCRYPT);
#else
  resu=ucl_aes_ecb(output,input,16,keyc,inputsize,UCL_CIPHER_ENCRYPT);
#endif



  if(resu!=UCL_OK)
    {
      printf("ERROR during AES encryption\n");
      return(EXIT_FAILURE);
    }
  if(TRUE==verbose)
    {
      printf("INFO: encrypted payload:");
      for(i=0;i<inputsize;i++)
	printf("%02x",output[i]);
      printf("\n");
    }
  //replace padded plain payload by encrypted data
  ipayload=inputsize;
  for(i=0;i<ipayload;i++)
    payload[i]=output[i];
  return(EXIT_SUCCESS);
}

int aes_cmac_payload(void)
{
  u8 cmac[UCL_AES_BLOCKSIZE];
  int resu;
  int i;
  int j;
  u8 input[MAX_STRING];
  int inputsize;
  if(TRUE==verbose)
    printf("INFO:payload signed\n");
  //copy payload
  if(TRUE==verbose)
    {
      printf("INFO: payload:");
      for(i=0;i<ipayload;i++)
	printf("%02x",payload[i]);
      printf("\n");
    }
  for(j=0,i=4;i<ipayload;i++,j++)
    input[j]=payload[i];
  if(TRUE==verbose)
    {
      printf("INFO:input(%d):",ipayload-4);
      for(i=0;i<ipayload-4;i++)
	printf("%02x",input[i]);
      printf("\n");
    }
  padding(&inputsize,input);
  if(TRUE==verbose)
    {
      printf("INFO:padded input(%d):",inputsize);
      for(i=0;i<inputsize;i++)
	printf("%02x",input[i]);
      printf("\n");
    }
  if(TRUE==verbose)
    {
      printf("INFO:keys:");
      for(i=0;i<16;i++)
	printf("%02x",keys[i]);
      printf("\n");
    }
  resu=crypto_aes_cmac(cmac,UCL_AES_BLOCKSIZE,keys,input, inputsize);
  if(resu!=UCL_OK)
    {
      printf("ERROR during CMAC computation\n");
      return(EXIT_FAILURE);
    }
  if(TRUE==verbose)
    {
      printf("INFO:payload cmac:");
      for(i=0;i<inputsize;i++)
	printf("%02x",cmac[i]);
      printf("\n");
    }
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    payload[ipayload++]=cmac[i];
  return(EXIT_SUCCESS);
}

int rsa_sign_payload(void)
{
#ifndef _MXIM_HSM
	ucl_rsa_public_key_t keyPu;
	ucl_rsa_private_key_t keyPr;
#endif
	

  int sl=0;
  int j=0,i=0;
  int err=0;
  u8 signature[UCL_RSA_KEY_MAXSIZE];
#ifdef _MXIM_HSM
  int l_iSignatureLength=UCL_RSA_KEY_MAXSIZE;
#endif//MXIM_HSM
  u8 input[MAX_STRING];
  int inputsize=MAX_STRING;

#ifndef _MXIM_HSM
  //  printf("rsa len=%d bytes\n",config_struct.rsa_len);
  keyPr.modulus_length=config_struct.rsa_len;
  for(j=0;j<config_struct.rsa_len;j++)
    keyPr.modulus[j]=config_struct.rsa[j];
  for(j=0;j<(int)keyPr.modulus_length;j++)
    keyPr.private_exponent[j]=config_struct.rsa_privexp[j];
  keyPu.public_exponent_length=config_struct.rsa_explen;
  for(j=0;j<(int)keyPu.public_exponent_length;j++)
    keyPu.public_exponent[j]=config_struct.rsa_pubexp[j];
  keyPu.modulus_length=config_struct.rsa_len;
  for(j=0;j<(int)keyPu.modulus_length;j++)
    keyPu.modulus[j]=config_struct.rsa[j];
#else

  memset(input,0,inputsize);
  memset(signature,0,l_iSignatureLength);
#endif//MXIM_HSM

  sl=0;
  for(j=0,i=4;i<ipayload;i++,j++)
    input[j]=payload[i];
  inputsize=ipayload-4;
  if(TRUE==verbose)
    printf("inputsize=%d (%d)\n",inputsize,MAX_STRING);
  if(inputsize>MAX_STRING)
    printf("ERROR on inputsize (%d)\n",inputsize);
  if(SCP_FLORA_RSA==session_mode)
    {
#ifndef _MXIM_HSM
      err=ucl_pkcs1_ssa_pss_sha256_sign(signature,input,inputsize, &keyPr,sl);
      if(err!=UCL_OK)
	{
	  printf("ERROR on rsa pkcs1 sha256 sign (%d) %d %d\n",err,inputsize,sl);
	  return(EXIT_FAILURE);
	}
      err=ucl_pkcs1_ssa_pss_sha256_verify(signature,input,inputsize, &keyPu,sl);
      if(err!=UCL_OK)
	{
	  printf("ERROR in verify signature");
	  return(EXIT_FAILURE);
	}
#else
      l_iSignatureLength=UCL_RSA_KEY_MAXSIZE;
      unsigned long l_ulAttributeKeyType = CKA_LABEL;
      unsigned long l_ulHSMLabelKeyLength = strlen(g_tcHSMRSALabelKey);
      
      err=MXIMHSMSHA256Sign(	&g_objMXHSMCLI,
								(PUCHAR)input,
								(PULONG)&inputsize,
								&l_ulAttributeKeyType,
								(PUCHAR)g_tcHSMRSALabelKey,
								&l_ulHSMLabelKeyLength,
								CKM_RSA_X_509,
								(PUCHAR)signature, 
								(PULONG)&l_iSignatureLength);

		if(err!=UCL_OK)
		{
			printf("ERROR on rsa pkcs1 sha256 sign (%d) %d %d\n",err,inputsize,sl);
			return(EXIT_FAILURE);
		}

		
		printf("signature:");

		for(i=0;i<256;i++)
			printf("%02x",signature[i]);

		printf("\n");

#endif//MXIM_HSM
    }
  else
    {
#ifndef _MXIM_HSM
      err=ucl_pkcs1_ssa_pss_sha256_sign(signature,input,inputsize, &keyPr,sl);
      if(err!=UCL_OK)
	{
	  printf("ERROR on rsa pkcs1 sha256 sign (%d)\n",err);
	  return(EXIT_FAILURE);
	}
      err=ucl_pkcs1_ssa_pss_sha256_verify(signature,input,inputsize, &keyPu,sl);
      if(err!=UCL_OK)
	{
	  printf("ERROR in verify signature");
	  return(EXIT_FAILURE);
	}
    }
  for(i=0;i<config_struct.rsa_len;i++)
    payload[ipayload++]=signature[i];
#else
		l_iSignatureLength=UCL_RSA_KEY_MAXSIZE;
		unsigned long l_ulAttributeKeyType = CKA_LABEL;
		unsigned long l_ulHSMLabelKeyLength = strlen(g_tcHSMRSALabelKey);


		err=MXIMHSMSHA256Sign(&g_objMXHSMCLI,
						(PUCHAR)input,
						(PULONG)&inputsize,
						&l_ulAttributeKeyType,
						(PUCHAR)g_tcHSMRSALabelKey,
						&l_ulHSMLabelKeyLength,
						CKM_RSA_X_509,
						(PUCHAR)signature, 
						(PULONG)&l_iSignatureLength);


		if(err!=UCL_OK)
		{
			printf("ERROR in signature calculation");

			if(4 == err)
			{
				printf("\n HSM - THALES nshield edge - No module has been detected\n");
			}
			return(EXIT_FAILURE);
		}

    }

	memcpy(&payload[ipayload],signature,l_iSignatureLength);
	ipayload+=l_iSignatureLength;

#endif//MXIM_HSM
  return(EXIT_SUCCESS);
}

int read_configuration_payload(void)
{
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the response
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id
  payload[ipayload++]=2;
  payload[ipayload++]=READ_CONFIGURATION>>8;
  payload[ipayload++]=READ_CONFIGURATION&255;
  return(EXIT_SUCCESS);
}

//same for SCP and SCP FLORA
int read_configuration(void)
{
  int err;
  if(SBL==session_mode||SCP_FLORA_AES==session_mode || SCP_FLORA_RSA==session_mode || SCP_ANGELA_ECDSA==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_READ_CONFIGURATION]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  read_configuration_payload();
  if(SCP_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      if(TRUE==verbose)
	printf("payload signed\n");
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_READ_CONFIGURATION]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"read_configuration");
  send();
  return(EXIT_SUCCESS);
}

int mem_mapping_payload(void)
{
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the response is incremented after the response
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id
  payload[ipayload++]=2;
  payload[ipayload++]=MEM_MAPPING>>8;
  payload[ipayload++]=MEM_MAPPING&255;
  return(EXIT_SUCCESS);
}

//SCP only
int mem_mapping(void)
{
  int err;
  if(SBL==session_mode || SCP_FLORA_AES==session_mode || SCP_FLORA_RSA==session_mode|| SCP_ANGELA_ECDSA==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_READ_MEMORY_MAPPING]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  mem_mapping_payload();
  if(SCP_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      if(TRUE==verbose)
	printf("payload signed\n");
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-MEM-MAPPING",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"mem_mapping");
  send();
  return(EXIT_SUCCESS);
}

int generic_response_payload(void)
{
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //response size: 4 bytes for code
  payload[ipayload++]=4;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  return(EXIT_SUCCESS);
}

int generic_response(char *msg)
{
 if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  generic_response_payload();
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode||SCP_ANGELA_ECDSA==session_mode)
    {
      //nothing: no signature on response
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],msg);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"%s",msg);
  send();
  return(EXIT_SUCCESS);
}

int read_configuration_response_payload(void)
{
  int i;
  int start;
  int end;
  start=0;
  end=SECTOR_SIZE;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  tr_id=(tr_id+1)%256;
  // on la met ou non ??
  //  payload[ipayload++]=size>>8;
  //  payload[ipayload++]=size&255;
  for(i=start;i<end;i++)
    payload[ipayload++]=(u8)((i&15));
  //error code, on 4 bytes
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  return(EXIT_SUCCESS);
}

int read_configuration_response(void)
{
 if(SBL==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_READ_CONFIGURATION]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  read_configuration_response_payload();
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
      //nothing: no signature on response
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      if(TRUE==verbose)
	printf("payload signed\n");
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],"READ-CONFIG-RESPONSE");
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"read_config_response");
  send();
  return(EXIT_SUCCESS);
}

//le mapping renvoyé est bidon
int mem_mapping_response_payload(void)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  tr_id=(tr_id+1)%256;
  // on la met ou non ??
  //on met une size sur 4 bytes, en valeur 0x00-00-00-02
  payload[ipayload++]=00;
  payload[ipayload++]=00;
  payload[ipayload++]=00;
  //seulement 2 de longueur
  payload[ipayload++]=0x02;
  for(i=0;i<2;i++)
    payload[ipayload++]=i;
  //error code, on 4 bytes
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  return(EXIT_SUCCESS);
}

int mem_mapping_response(void)
{
 if(SBL==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_READ_MEMORY_MAPPING]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  mem_mapping_response_payload();
  if(SCP_RSA==session_mode)
    {
      //nothing: no signature on response
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      if(TRUE==verbose)
	printf("payload signed\n");
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],"mem_mapping_response");
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"mem_mapping_response");
  send();
  return(EXIT_SUCCESS);
}

//le mapping renvoyé est bidon
int aes_comp_response_payload(void)
{
  int i;
  int resu;
  u8 output[16];

#ifdef _MXIM_HSM
	resu=g_objMXIMUCLLibrary.AESECB(output,aes_data,16,aes_key,16,UCL_CIPHER_ENCRYPT);
#else
	resu=ucl_aes_ecb(output,aes_data,16,aes_key,16,UCL_CIPHER_ENCRYPT);
#endif

  if(UCL_OK!=resu)
    {
      printf("ERROR: AES code %d\n",resu);
      return(EXIT_FAILURE);
    }
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  tr_id=(tr_id+1)%256;
  for(i=0;i<16;i++)
    payload[ipayload++]=output[i];
  //error code, on 4 bytes
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  payload[ipayload++]=0;
  return(EXIT_SUCCESS);
}

int aes_comp_response(void)
{
 if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  mem_mapping_response_payload();
  if(SCP_RSA==session_mode)
    {
      //nothing: no signature on response
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      if(TRUE==verbose)
	printf("payload signed\n");
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],"AES-COMP-RESPONSE");
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"aes_comp_response");
  send();
  return(EXIT_SUCCESS);
}

int write_bpk_blpk_response(void)
{
  generic_response("write_bpk_blpk_response");
  return(EXIT_SUCCESS);
}

int write_bpk_fak_response(void)
{
  generic_response("write_bpk_fak_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_bpk_response(void)
{
  generic_response("write_bpk_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_otp_response(void)
{
  generic_response("write_otp_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_crk_response(void)
{
  generic_response("write_crk_response");
  return(EXIT_SUCCESS);
}

int rewrite_crk_response(void)
{
  generic_response("rewrite_crk_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_timeout_response(void)
{
  generic_response("write_timeout_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int kill_chip_response(void)
{
  generic_response("kill_chip_response");
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int execute_code_response(void)
{
  generic_response("execute_code_response");
  return(EXIT_SUCCESS);
}

int del_mem_response(void)
{
  generic_response("del_mem_response");
  return(EXIT_SUCCESS);
}

int verify_data_response(void)
{
  generic_response("verify_data_response");
  return(EXIT_SUCCESS);
}

int write_mem_response(void)
{
  generic_response("write_mem_response");
  return(EXIT_SUCCESS);
}

int del_mem_payload(void)
{
  int i;
  int range;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the response
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id, 4 bytes for start add, 2 bytes for length
  payload[ipayload++]=10;
  payload[ipayload++]=ERASE_MEM>>8;
  payload[ipayload++]=ERASE_MEM&255;
  //set up the start addr
  // on 4 bytes
  for(i=3;i>=0;i--)
    payload[ipayload++]=(start_addr>>(8*i))&255;
  //set up the length
  // on 4 bytes
  range=(end_addr-start_addr);
  if(TRUE==verbose)
    printf("payload for erase is: %d bytes\n",range);
  //need to be multiple of 16
  //#bug 2982
  if(range)
    range=((range/16)+1)*16;
  if(TRUE==verbose)
    printf("payload for erase is: %d bytes\n",range);
  for(i=3;i>=0;i--)
    payload[ipayload++]=((range)>>(8*i))&255;
  return(EXIT_SUCCESS);
}

int get_start_addr_and_length_s19(char *s19filename)
{
  FILE *fp;
  char line[MAXLINE];
  int i;
  int nb_bytes;
  fp=fopen(s19filename,"r");
  if(fp==NULL)
    {
      printf("ERROR: <%s> not found\n",s19filename);
      return(EXIT_FAILURE);
    }
  nb_bytes=0;
  start_addr=-1;
  while(fscanf(fp,"%s",line)!=EOF)
    {
      if(MAXLINE<strlen(line))
	{
	  printf("ERROR: line too long: %d chars, while limited to %d\n",strlen(line),MAXLINE);
	  return(EXIT_FAILURE);
	}
      if(line[0]==S19_WDATA_CHAR1 && line[1]==S19_WDATA_CHAR2)
	{
	  if(-1==start_addr)
	    {
	      for(i=S19_ADDRESS_START;i<S19_ADDRESS_START+2*S19_ADDRESS_LEN;i+=2)
		start_addr=(start_addr<<8)+hex(line[i],line[i+1]);
	      start_addr^=address_offset;
	      if(TRUE==verbose)
		printf("starting address=%08x\n",start_addr);
	    }
	  for(end_addr=0,i=S19_ADDRESS_START;i<S19_ADDRESS_START+2*S19_ADDRESS_LEN;i+=2)
	    {
	      end_addr=(end_addr<<8)+hex(line[i],line[i+1]);
	    }
	  //do not forget to add the length of the line in order to have the real last address
	  end_addr+=hex(line[2],line[3])-1;
	  end_addr^=address_offset;
	  //compute total nb of bytes of data in the s19 file
	  //not counting address and crc
	  nb_bytes+=hex(line[S19_LINE_LEN_POS1],line[S19_LINE_LEN_POS2])-S19_ADDRESS_LEN-S19_CRC_LEN;
	}
    }
  if(TRUE==verbose)
    {
      printf("end addr=%08x\n",end_addr);
      printf("file <%s> nb bytes: %d\n",s19filename,nb_bytes);
    }
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

int get_start_addr_and_length_s20(char *s20filename)
{
  FILE *fp;
  char line[MAXLINE];
  int i;
  int nb_bytes;
  fp=fopen(s20filename,"r");
  if(fp==NULL)
    {
      printf("ERROR: <%s> not found\n",s20filename);
      return(EXIT_FAILURE);
    }
  nb_bytes=0;
  start_addr=-1;
  while(fscanf(fp,"%s",line)!=EOF)
    {
      if(MAXLINE<strlen(line))
	{
	  printf("ERROR: line too long: %d chars, while limited to %d\n",strlen(line),MAXLINE);
	  return(EXIT_FAILURE);
	}
      if(line[0]==S20_WDATA_CHAR1 && line[1]==S20_WDATA_CHAR2)
	{
	  if(-1==start_addr)
	    {
	      for(i=S20_ADDRESS_START;i<S20_ADDRESS_START+2*S20_ADDRESS_LEN;i+=2)
		start_addr=(start_addr<<8)+hex(line[i],line[i+1]);
	      start_addr^=address_offset;
	      if(TRUE==verbose)
		printf("starting address=%08x\n",start_addr);
	    }
	  for(end_addr=0,i=S20_ADDRESS_START;i<S20_ADDRESS_START+2*S20_ADDRESS_LEN;i+=2)
	    end_addr=(end_addr<<8)+hex(line[i],line[i+1]);
	  //do not forget to add the length of the line in order to have the real last address
	  end_addr+=hex(line[2],line[3])-1;
	  end_addr^=address_offset;
	  //compute total nb of bytes of data in the s20 file
	  //not counting address and crc
	  //	  nb_bytes+=hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2])-S20_ADDRESS_LEN-S20_CRC_LEN;
	  nb_bytes+=hex(line[S20_LINE_LEN_POS1],line[S20_LINE_LEN_POS2])*256+hex(line[S20_LINE_LEN_POS3],line[S20_LINE_LEN_POS4])-S20_ADDRESS_LEN-S20_CRC_LEN;
	}
    }
  if(TRUE==verbose)
    {
      printf("end addr=%08x\n",end_addr);
      printf("file <%s> nb bytes: %d\n",s20filename,nb_bytes);
    }
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

//SCP and SCP FLORA shared command (named ERASE-DATA in FLORA)
int del_mem(char *sfilename,char *ptr_address_offset)
{
  int err;
  UNUSED_PARAMETER(ptr_address_offset);
  if(EXIT_SUCCESS==extension(".s19",sfilename))
    get_start_addr_and_length_s19(sfilename);
  else
    if(EXIT_SUCCESS==extension(".s20",sfilename))
      get_start_addr_and_length_s20(sfilename);
    else
      {
	printf("ERROR: <%s> file extension not supported (only .s19 and .s20)\n",sfilename);
	return(EXIT_FAILURE);
      }
  if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  del_mem_payload();
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-DEL_MEM",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"del_mem");
  send();
  return(EXIT_SUCCESS);
}

//SCP and SCP FLORA shared command (named ERASE-DATA in FLORA)
//this function issues a command for erasing an area defined by
//input strings, sstart_addr represents the area starting address, in hexa
//and slength represents the length (in bytes) of the area
//this function is directly used for the script command ERASE-DATA
int del_data(char *sstart_addr, char *slength)
{
  int length;
  int err;
  if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  if(0==sscanf(sstart_addr,"%x",&start_addr))
    {
      printf("ERROR: sstart_addr parameter <%s> incorrectly formatted as a number\n",sstart_addr);
      return(EXIT_FAILURE);
    }
  if(0==sscanf(slength,"%x",&length))
    {
      printf("ERROR: slength parameter <%s> incorrectly formatted as a number\n",slength);
      return(EXIT_FAILURE);
    }

  end_addr=start_addr+length;
  if(TRUE==verbose)
    printf("%s -> %x %s -> %x: end@:%x\n",sstart_addr,start_addr,slength,length,end_addr);
  ipayload=0;
  seq++;
  del_mem_payload();
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-DEL_MEM",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"del_data");
  send();
  return(EXIT_SUCCESS);
}

//SCP command for blpk key writing
int write_bpk_blpk_payload(char *bpk_char)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 18=2 bytes for command id and 16 for aes key
  payload[ipayload++]=18;
  payload[ipayload++]=WRITE_BLPK>>8;
  payload[ipayload++]=WRITE_BLPK&255;
  if(TRUE==verbose)
    {
      printf("BLPK:");
      for(i=0;i<UCL_AES_BLOCKSIZE;i++)
	printf("%02x",hex(bpk_char[i*2],bpk_char[i*2+1]));
      printf("\n");
    }
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    payload[ipayload++]=hex(bpk_char[i*2],bpk_char[i*2+1]);
  return(EXIT_SUCCESS);
}

//SCP pcilinux bootloader command only
//bug #1622 correction: the correc key was not used
int write_bpk_blpk(char *bpk_char)
{
  int err;
  if(SBL==session_mode || SCP_FLORA_AES==session_mode || SCP_FLORA_RSA==session_mode||SCP_ANGELA_ECDSA==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_BLPK]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_bpk_blpk_payload(bpk_char);
  if(SCP_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_BLPK]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_blpk");
  send();
  return(EXIT_SUCCESS);
}

int write_bpk_fak_payload(char *fak_char)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 18=2 bytes for command id and 16 for aes key
  payload[ipayload++]=18;
  payload[ipayload++]=WRITE_FAK>>8;
  payload[ipayload++]=WRITE_FAK&255;
  if(TRUE==verbose)
    {
      printf("FAK:");
      for(i=0;i<UCL_AES_BLOCKSIZE;i++)
	printf("%02x",hex(fak_char[i*2],fak_char[i*2+1]));
      printf("\n");
    }
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    payload[ipayload++]=hex(fak_char[i*2],fak_char[i*2+1]);
  return(EXIT_SUCCESS);
}

//SCP pcilinux bootloader command only
//bug #1622 correction: the correc key was not used
int write_bpk_fak(char *fak_char)
{
  int err;
  if(SBL==session_mode || SCP_FLORA_AES==session_mode || SCP_FLORA_RSA==session_mode||SCP_ANGELA_ECDSA==session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_FAK]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_bpk_fak_payload(fak_char);
  if(SCP_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_FAK]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_fak");
  send();
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_timeout_payload(char timeout_target_char,char *timeout_char)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id, 1 byte for target, 2 bytes for timeout value
  //+1 corrected in 2.3.4
  payload[ipayload++]=2+1+2;
  payload[ipayload++]=WRITE_TIMEOUT>>8;
  payload[ipayload++]=WRITE_TIMEOUT&255;
  if(CHAR_TIMEOUT_UART_TARGET==timeout_target_char)
    payload[ipayload++]=TIMEOUT_UART_TARGET;
  else
    if(CHAR_TIMEOUT_USB_TARGET==timeout_target_char)
      payload[ipayload++]=TIMEOUT_USB_TARGET;
  else
    if(CHAR_TIMEOUT_VBUS_TARGET==timeout_target_char)
      payload[ipayload++]=TIMEOUT_VBUS_TARGET;
  payload[ipayload++]=hex(timeout_char[0],timeout_char[1]);
  payload[ipayload++]=hex(timeout_char[2],timeout_char[3]);
  if(TRUE==verbose)
    {
      printf("timeout:");
      for(i=0;i<(int)strlen(timeout_char);i++)
	printf("%c",timeout_char[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_timeout(char timeout_target_char, char *timeout_char)
{
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_ANGELA_ECDSA!= session_mode && SCP_FLORA_AES!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_TIMEOUT]);
      return(EXIT_FAILURE);
    }
  if(timeout_target_char!=CHAR_TIMEOUT_UART_TARGET && timeout_target_char!=CHAR_TIMEOUT_USB_TARGET && timeout_target_char!=CHAR_TIMEOUT_VBUS_TARGET)
    {
      printf("ERROR: not allowed target: %c; only %c, %c and %c are allowed\n",timeout_target_char,CHAR_TIMEOUT_UART_TARGET, CHAR_TIMEOUT_USB_TARGET, CHAR_TIMEOUT_VBUS_TARGET);
      return(EXIT_FAILURE);
    }
  if(strlen(timeout_char)!=4)
    {
      printf("ERROR: timeout is not 2-byte long\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_timeout_payload(timeout_target_char,timeout_char);
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      err=ecdsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_TIMEOUT]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_timeout");
  send();
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int kill_chip_payload(void)
{
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id
  payload[ipayload++]=2;
  payload[ipayload++]=KILL_CHIP>>8;
  payload[ipayload++]=KILL_CHIP&255;
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int kill_chip(void)
{
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_FLORA_AES!=session_mode && SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_KILL_CHIP]);
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  kill_chip_payload();
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_KILL_CHIP]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"kill_chip");
  send();
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_bpk_payload(char *data_char,char *offset_char)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id, 2 bytes for data len, 2 bytes for offset and data value len
  //data value is a hexa string so, its data len is string len/2
  payload[ipayload++]=2+2+2+strlen(data_char)/2;
  payload[ipayload++]=WRITE_BPK>>8;
  payload[ipayload++]=WRITE_BPK&255;
  payload[ipayload++]=(2+strlen(data_char)/2)>>8;
  payload[ipayload++]=(2+strlen(data_char)/2)&255;
  payload[ipayload++]=hex(offset_char[0],offset_char[1]);
  payload[ipayload++]=hex(offset_char[2],offset_char[3]);
  if(TRUE==verbose)
    {
      printf("data:");
      for(i=0;i<(int)strlen(data_char);i++)
	printf("%c",data_char[i]);
      printf("\n");
      printf("offset:");
      for(i=0;i<(int)strlen(offset_char);i++)
	printf("%c",offset_char[i]);
      printf("\n");
    }
  for(i=0;i<(int)strlen(data_char)/2;i++)
    payload[ipayload++]=hex(data_char[i*2],data_char[i*2+1]);
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_bpk(char *offset_char,char *data_char)
{
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_FLORA_AES!=session_mode &&SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_BPK]);
      return(EXIT_FAILURE);
    }
  if((strlen(data_char)%2)!=0)
    {
      printf("ERROR: data are not byte-aligned\n");
      return(EXIT_FAILURE);
    }
  if(strlen(offset_char)!=4)
    {
      printf("ERROR: offset is not 2-byte long (%d)\n",strlen(offset_char));
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_bpk_payload(data_char,offset_char);
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_BPK]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_bpk");
  send();
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int execute_code_payload(char *address)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: address value len
  //address value is a hexa string so, its data len is string len/2
  //#bug 2202: missing 2 bytes in payload length
  payload[ipayload++]=(strlen(address)/2)+2;
  payload[ipayload++]=EXECUTE_CODE>>8;
  payload[ipayload++]=EXECUTE_CODE&255;
  //#2203: no data length parameter in the execute-code command
  //  payload[ipayload++]=(strlen(address)/2)>>8;
  //  payload[ipayload++]=(strlen(address)/2)&255;
  if(TRUE==verbose)
    {
      printf("address:");
      for(i=0;i<(int)strlen(address);i++)
	printf("%c",address[i]);
      printf("\n");
    }
  for(i=0;i<(int)strlen(address)/2;i++)
    payload[ipayload++]=hex(address[i*2],address[i*2+1]);
  return(EXIT_SUCCESS);
}

int execute_code(char *address)
{
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_FLORA_AES!=session_mode && SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_EXECUTE_CODE]);
      return(EXIT_FAILURE);
    }
  if((strlen(address)%2)!=0)
    {
      printf("ERROR: address is not byte-aligned\n");
      return(EXIT_FAILURE);
    }
  if(strlen(address)!=8)
    {
      printf("ERROR: address is not 4-byte long (%d)\n",strlen(address));
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  execute_code_payload(address);
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_EXECUTE_CODE]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"execute_code");
  send();
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_otp_payload(char *data_char,char *offset_char)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 2 bytes for command id, 2 bytes for data len, 2 bytes for offset and data value len
  //data value is a hexa string so, its data len is string len/2
  payload[ipayload++]=2+2+2+strlen(data_char)/2;
  payload[ipayload++]=WRITE_OTP>>8;
  payload[ipayload++]=WRITE_OTP&255;
  payload[ipayload++]=(2+strlen(data_char)/2)>>8;
  payload[ipayload++]=(2+strlen(data_char)/2)&255;
  payload[ipayload++]=hex(offset_char[0],offset_char[1]);
  payload[ipayload++]=hex(offset_char[2],offset_char[3]);
  if(TRUE==verbose)
    {
      printf("data:");
      for(i=0;i<(int)strlen(data_char);i++)
	printf("%c",data_char[i]);
      printf("\n");
      printf("offset:");
      for(i=0;i<(int)strlen(offset_char);i++)
	printf("%c",offset_char[i]);
      printf("\n");
    }
  for(i=0;i<(int)strlen(data_char)/2;i++)
    payload[ipayload++]=hex(data_char[i*2],data_char[i*2+1]);
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_otp(char *offset_char,char *data_char)
{
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_FLORA_AES!=session_mode && SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_OTP]);
      return(EXIT_FAILURE);
    }
  if((strlen(data_char)%2)!=0)
    {
      printf("ERROR: data are not byte-aligned\n");
      return(EXIT_FAILURE);
    }
  if(strlen(offset_char)!=4)
    {
      printf("ERROR: offset <%s> is not 2-byte long (%d)\n",offset_char, strlen(offset_char));
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_otp_payload(data_char,offset_char);
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_OTP]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_otp");
  send();
  return(EXIT_SUCCESS);
}

/*int read_file_ecdsa(u8 *puk_x,u8 *puk_y,u8 *privk,int size,char *filename)
{
  FILE *fp;
  int i;
  int resu;
  u8 d8;
  char line[MAXLINE];
    if(TRUE==verbose)
      printf("<read_file_ecdsa <%s>>\n",filename);
  fp=fopen(filename,"r");
  if(fp==NULL)
    {
      printf("ERROR on opening <%s>\n",filename);
      return(EXIT_FAILURE);
    }
  for(i=0;i<size;i++)
    privk[i]=0;
  for(i=0;i<size;i++)
    {
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
      privk[i]=d8;
    }
  for(i=0;i<size;i++)
    puk_x[i]=0;
  for(i=0;i<size;i++)
    {
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
      puk_x[i]=d8;
    }
  for(i=0;i<size;i++)
    puk_y[i]=0;
  for(i=0;i<size;i++)
    {
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
      puk_y[i]=d8;
    }
  if(TRUE==verbose)
    {
      for(i=0;i<size;i++)
	printf("%02x",puk_x[i]);
      printf("\n");
      for(i=0;i<size;i++)
	printf("%02x",puk_y[i]);
      printf("\n");
      for(i=0;i<size;i++)
	printf("%02x",privk[i]);
      printf("\n");
    }
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}	 */

//read signed rsa public key file
//contains: rsa modulus, public exponent and signature
//note: rsa modulus and signature have same length
int read_file_signed_rsa_publickey(u8 *puk,int size,u8 *pukexp,int expsize,u8 *signature,char *filename)
{
  FILE *fp;
  int i;
  int resu;
  char line[MAXLINE];
#ifndef _MXIM_HSM
  u8 d8=0x00;
#else
  u8 l_tcCharRead[4];
  memset(l_tcCharRead,0,4);
#endif//_MXIM_HSM

  if(TRUE==verbose)
    printf("<read_file_signed_rsa_puk <%s>>\n",filename);
  fp=fopen(filename,"r");
  if(NULL==fp)
    {
      printf("ERROR on opening <%s>\n",filename);
      return(EXIT_FAILURE);
    }
  memset(puk,0,size);
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      puk[i]=d8;
#else
      puk[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  for(i=0;i<expsize;i++)
    pukexp[i]=0;
  for(i=0;i<expsize;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      pukexp[i]=d8;
#else
      pukexp[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  for(i=0;i<size;i++)
    signature[i]=0;
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      signature[i]=d8;
#else
      signature[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  if(verbose==TRUE)
    {
      printf("puk:");
      for(i=0;i<size;i++)
	printf("%02x",puk[i]);
      printf("\n");
      printf("exp:");
      for(i=0;i<expsize;i++)
	printf("%02x",pukexp[i]);
      printf("\n");
      printf("signature:");
      for(i=0;i<size;i++)
	printf("%02x",signature[i]);
      printf("\n");
    }
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

//read signed ecdsa public key file
//contains: ecdsa public key (x&y)and signature
//note: public key and signature have same length
int read_file_signed_ecdsa_publickey(u8 *x,u8 *y,u8 *r,u8 *s,int size,char *filename)
{
  FILE *fp;
  int i;
  int resu;
  char line[MAXLINE];
#ifndef _MXIM_HSM
  u8 d8=0x00;
#else
  u8 l_tcCharRead[4];
  memset(l_tcCharRead,0,4);
#endif//_MXIM_HSM

  if(TRUE==verbose)
    printf("<read_file_signed_ecdsa_puk <%s>>\n",filename);
  fp=fopen(filename,"r");
  if(NULL==fp)
    {
      printf("ERROR on opening <%s>\n",filename);
      return(EXIT_FAILURE);
    }
  memset(x,0,size);
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      x[i]=d8;
#else
      x[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  for(i=0;i<size;i++)
    y[i]=0;
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      y[i]=d8;
#else
      y[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  for(i=0;i<size;i++)
    r[i]=0;
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      r[i]=d8;
#else
      r[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  for(i=0;i<size;i++)
    s[i]=0;
  for(i=0;i<size;i++)
    {
#ifndef _MXIM_HSM
      resu=fscanf(fp,"%02x",(unsigned int*)&d8);
#else
      memset(l_tcCharRead,0,4);
      resu = fscanf_s(fp,"%2X",&l_tcCharRead);
#endif//_MXIM_HSM
      if(resu!=1)
	{
	  printf("ERROR: unexpected size (%d-%d)\n",size, strlen(line)-1);
	  return(EXIT_FAILURE);
	}
#ifndef _MXIM_HSM
      s[i]=d8;
#else
      s[i]=l_tcCharRead[0];
#endif//_MXIM_HSM
    }
  if(verbose==TRUE)
    {
      printf("x:");
      for(i=0;i<size;i++)
	printf("%02x",x[i]);
      printf("\n");
      printf("y:");
      for(i=0;i<size;i++)
	printf("%02x",y[i]);
      printf("\n");
      printf("r:");
      for(i=0;i<size;i++)
	printf("%02x",r[i]);
      printf("\n");
      printf("s:");
      for(i=0;i<size;i++)
	printf("%02x",s[i]);
      printf("\n");
    }
  (void)fclose(fp);
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_crk_payload_rsa(u8 *rsa_modulus,int rsa_modulus_len,u8 *rsa_pubexp,int rsa_explen,u8 *mrk_signature)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  //command length: 2 bytes for command , 2 bytes for data len, 256 bytes for crk modulus, 4 bytes for pubexp, 256 bytes for mrk signature
  //data value is a hexa string so, its data len is string len/2
  payload[ipayload++]=(2+2+256+4+256)>>8;
  payload[ipayload++]=(2+2+256+4+256)&255;
  payload[ipayload++]=WRITE_CRK>>8;
  payload[ipayload++]=WRITE_CRK&255;
  payload[ipayload++]=(rsa_modulus_len*2+rsa_explen)>>8;
  payload[ipayload++]=(rsa_modulus_len*2+rsa_explen)&255;
  for(i=0;i<rsa_modulus_len;i++)
    payload[ipayload++]=rsa_modulus[i];
  for(i=0;i<rsa_explen;i++)
    payload[ipayload++]=rsa_pubexp[i];
  for(i=0;i<rsa_modulus_len;i++)
    payload[ipayload++]=mrk_signature[i];
  if(TRUE==verbose)
    {
      printf("CRK modulus:");
      for(i=0;i<rsa_modulus_len;i++)
	printf("%02x",rsa_modulus[i]);
      printf("\n");
      printf("CRK public exponent:");
      for(i=0;i<rsa_explen;i++)
	printf("%02x",rsa_pubexp[i]);
      printf("\n");
      printf("MRK signature:");
      for(i=0;i<rsa_modulus_len;i++)
	printf("%02x",mrk_signature[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

int write_crk_payload_ecdsa(u8 *x,u8 *y,u8 *r,u8 *s,int ecdsa_len)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  //command length: 2 bytes for command , 2 bytes for data len, 256 bytes for crk modulus, 4 bytes for pubexp, 256 bytes for mrk signature
  //data value is a hexa string so, its data len is string len/2
  payload[ipayload++]=(2+2+ecdsa_len*4)>>8;
  payload[ipayload++]=(2+2+ecdsa_len*4)&255;
  payload[ipayload++]=WRITE_CRK>>8;
  payload[ipayload++]=WRITE_CRK&255;
  payload[ipayload++]=(ecdsa_len*4)>>8;
  payload[ipayload++]=(ecdsa_len*4)&255;
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=x[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=y[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=r[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=s[i];
  if(TRUE==verbose)
    {
      printf("CRK public key\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",x[i]);
      printf("\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",y[i]);
      printf("\n");
      printf("MRK signature\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",r[i]);
      printf("\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",s[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

int rewrite_crk_payload_ecdsa(u8 *x,u8 *y,u8 *r,u8 *s,int ecdsa_len)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the payload
  //  tr_id=(tr_id+1)%256;
  //command length: 2 bytes for command , 2 bytes for data len, 256 bytes for crk modulus, 4 bytes for pubexp, 256 bytes for mrk signature
  //data value is a hexa string so, its data len is string len/2
  payload[ipayload++]=(2+2+ecdsa_len*4)>>8;
  payload[ipayload++]=(2+2+ecdsa_len*4)&255;
  payload[ipayload++]=REWRITE_CRK>>8;
  payload[ipayload++]=REWRITE_CRK&255;
  payload[ipayload++]=(ecdsa_len*4)>>8;
  payload[ipayload++]=(ecdsa_len*4)&255;
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=x[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=y[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=r[i];
  for(i=0;i<ecdsa_len;i++)
    payload[ipayload++]=s[i];
  if(TRUE==verbose)
    {
      printf("CRK public key\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",x[i]);
      printf("\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",y[i]);
      printf("\n");
      printf("MRK signature\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",r[i]);
      printf("\n");
      for(i=0;i<ecdsa_len;i++)
	printf("%02x",s[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

//SCP FLORA command
int write_crk(char *signaturefile)
{
  int rsa_len=RSA_MODULUS_LEN;
  int rsa_explen=RSA_PUBLIC_EXPONENT_LEN;
  int ecdsa_len=ECDSA_MODULUS_LEN;
  int err;
  if(SCP_FLORA_RSA!= session_mode && SCP_FLORA_AES!=session_mode && SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_WRITE_CRK]);
      return(EXIT_FAILURE);
    }
  if(SCP_ANGELA_ECDSA==session_mode)
    err=read_file_signed_ecdsa_publickey(crk_ecdsa_x,crk_ecdsa_y,mrk_ecdsa_r,mrk_ecdsa_s,ecdsa_len,signaturefile);
  else
    err=read_file_signed_rsa_publickey(crk_rsa_modulus,rsa_len,crk_rsa_pubexp,rsa_explen,mrk_signature,signaturefile);
  if(EXIT_SUCCESS!=err)
    {
      printf("ERROR in read_file_signature\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      write_crk_payload_ecdsa(crk_ecdsa_x,crk_ecdsa_y,mrk_ecdsa_r,mrk_ecdsa_s,ecdsa_len);
    }
  else
    write_crk_payload_rsa(crk_rsa_modulus,rsa_len,crk_rsa_pubexp,rsa_explen,mrk_signature);
  if(SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_WRITE_CRK]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_crk");
  send();
  return(EXIT_SUCCESS);
}

int rewrite_crk(char *signaturefile)
{
  int ecdsa_len=ECDSA_MODULUS_LEN;
  int err;
  if(SCP_ANGELA_ECDSA!=session_mode)
    {
      printf("ERROR: command <%s> not supported\n",idf_scp_cmd[COMMAND_REWRITE_CRK]);
      return(EXIT_FAILURE);
    }
  if(SCP_ANGELA_ECDSA==session_mode)
    err=read_file_signed_ecdsa_publickey(crk_ecdsa_x,crk_ecdsa_y,mrk_ecdsa_r,mrk_ecdsa_s,ecdsa_len,signaturefile);
  if(EXIT_SUCCESS!=err)
    {
      printf("ERROR in read_file_signature\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      rewrite_crk_payload_ecdsa(crk_ecdsa_x,crk_ecdsa_y,mrk_ecdsa_r,mrk_ecdsa_s,ecdsa_len);
    }
  if(SCP_ANGELA_ECDSA==session_mode)
    {
      err=ecdsa_sign_payload();
      if(EXIT_FAILURE==err)
	return(err);
    }
  sprintf(message,"%s-%s",idf_ctl[DATA_TRANSFER],idf_scp_cmd[COMMAND_REWRITE_CRK]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"rewrite_crk");
  send();
  return(EXIT_SUCCESS);
}

int aes_comp_payload(void)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the response
  //  tr_id=(tr_id+1)%256;
  payload[ipayload++]=0;
  //command length: 34=2 bytes for command id, 16 for aes key, 16 for aes data
  payload[ipayload++]=34;
  payload[ipayload++]=AES_COMP>>8;
  payload[ipayload++]=AES_COMP&255;
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    payload[ipayload++]=aes_key[i];
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    payload[ipayload++]=aes_data[i];
  return(EXIT_SUCCESS);
}

//SCP pcilinux bootloader command only
int aes_comp(void)
{
  int err;
  if(SBL==session_mode || SCP_FLORA_AES==session_mode || SCP_FLORA_RSA==session_mode || SCP_ANGELA_ECDSA==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  aes_comp_payload();
  if(SCP_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    {
      if(SCP_PP_E_CMAC==config_struct.pp)
	{
	  //encrypt plain payload
	  aes_encrypt_payload();
	  if(TRUE==verbose)
	    printf("payload encrypted\n");
	}
      //cmac performed on encrypted payload
      aes_cmac_payload();
    }
  sprintf(message,"%s-AES-COMP",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"aes_comp");
  send();
  return(EXIT_SUCCESS);
}

int write_mem_payload(u8 *data,int data_len,int data_addr)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the response
  //  tr_id=(tr_id+1)%256;
  // size in on 2 bytes !! especially important for long frames
  // made of 2 bytes for command id, 4 bytes for start @, 4 bytes for data len and then, the data themselves
  payload[ipayload++]=(2+4+4+data_len)>>8;
  payload[ipayload++]=(2+4+4+data_len)&255;
  payload[ipayload++]=WRITE_MEM>>8;
  payload[ipayload++]=WRITE_MEM&255;
  //set up the start addr
  // on 4 bytes
  for(i=3;i>=0;i--)
    payload[ipayload++]=(data_addr>>(8*i))&255;
  //set up the length
  for(i=3;i>=0;i--)
    {
      payload[ipayload]=(data_len>>(8*i))&255;
      ipayload++;
    }
  for(i=0;i<data_len;i++)
    payload[ipayload++]=data[i];
  return(EXIT_SUCCESS);
}

//SCP and SCP flora shared command (named WRITE-DATA for FLORA)
int write_mem(u8 *data,int data_len,int data_addr)
{
  int err;
  if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  write_mem_payload(data,data_len,data_addr);
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
	{
	  printf("ERROR: rsa-sign-payload\n");
	  return(err);
	}
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	if(TRUE==verbose)
	  printf("payload signed\n");
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-WRITE_MEM",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"write_mem");
  send();
  return(EXIT_SUCCESS);
}

int write_file(char *sfilename,char *ptr_address_offset)
{
  int i,j;
  u8 chunk[MAX_CHUNK_SIZE];
  int chunk_len;
  //this variable is used to have a whole packet with a length of chunk_size
  //meaning the data-only payload shall be reduced in order to have the whole packet length=chunk_size
  //i.e. header+command+data+signature+crc=chunk_size
  int new_chunk_size;
  int chunk_addr;
  int resu;
  //write-file includes automatic erasure of concerned area;
  //for data write only, use write-file-only
  del_mem(sfilename,ptr_address_offset);
  usip();
  ack();
  del_mem_response();
  host();
  ack();
  if(EXIT_SUCCESS==extension(".s19",sfilename))
    read_s19(sfilename,ptr_address_offset);
  else
  if(EXIT_SUCCESS==extension(".s20",sfilename))
    read_s20(sfilename,ptr_address_offset);
  else
    {
      printf("ERROR: <%s> file extension not supported (only .s19 and .s20)\n",sfilename);
      return(EXIT_FAILURE);
    }
  //10 is the write-data command len: 2 bytes for the command, 4 bytes for the data length, 4 bytes for the data address
  new_chunk_size=chunk_size-HEADER_LEN-CRC_LEN-COMMAND_LEN-10;
  //if the mode is RSA mode, the signature len shall also be taken into account
  if(SCP_FLORA_RSA==session_mode)
    new_chunk_size-=SIGNATURE_LEN;
  if(TRUE==verbose)
    printf("%d new chunk_size=%d\n",chunk_size,new_chunk_size);
  chunk_len=0;
  i=0;
  //parse data
  //grouping them by contiguous addresses, up to CHUNK-SIZE
  //meaning each time an address is not the next one than the previous one
  //or each time a block of CHUNK-SIZE data has been built,
  //a write-mem is issued
  //until the end.
  while(i<data_len)
    {
      chunk_len=0;
      chunk[chunk_len]=data[i];
      //the block starting address (needed for write-mem)
      chunk_addr=addr[i];
      chunk_len++;
      i++;
      //while consecutive addresses and not too big chunk
      //take into account the new_chunk_size
      while((addr[i]==addr[i-1]+1)&&(chunk_len<new_chunk_size)&&(i<data_len))
	{
	  //accumulate
	  chunk[chunk_len]=data[i];
	  chunk_len++;
	  i++;
	}
      //the last packet is filled up with FF if needed
      //2.3.6 (#2252): not filled up with FF anymore
      if(i==data_len)
	{
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	  //2.3.6 (#2252): not filled up with FF anymore
	  //	  new_chunk_len=((chunk_len/16)+1)*16;
	  //2.3.6 (#2252): not filled up with FF anymore
	  //for(j=chunk_len;j<new_chunk_len;j++)
	  //2.3.6 (#2252): not filled up with FF anymore
	  //chunk[j]=0xFF;
	  //2.3.6 (#2252): not filled up with FF anymore
	  //chunk_len=new_chunk_len;
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	  if(TRUE==verbose)
	    {
	      printf("last:");
	      for(j=0;j<chunk_len;j++)
		printf("%02x",chunk[j]);
	      printf("\n");
	    }
	}
      resu=write_mem(chunk,chunk_len,chunk_addr);
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR in write_mem\n");
	  return(EXIT_FAILURE);
	}
      usip();
      ack();
      write_mem_response();
      host();
      ack();
    }
  if(TRUE==verbose)
    {
      for(i=0;i<chunk_len;i++)
	printf("%02x",chunk[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

int write_only(char *sfilename,char *ptr_address_offset)
{
  int i;
  u8 chunk[MAX_CHUNK_SIZE];
  int chunk_len;
  int new_chunk_size;
  int chunk_addr;
  int resu;
  //  del_mem(sfilename);
  //  usip();
  //  ack();
  //  del_mem_response();
  //  host();
  //  ack();
  if(EXIT_SUCCESS==extension(".s19",sfilename))
    read_s19(sfilename,ptr_address_offset);
  else
  if(EXIT_SUCCESS==extension(".s20",sfilename))
    read_s20(sfilename,ptr_address_offset);
  else
    {
      printf("ERROR: <%s> file extension not supported (only .s19 and .s20)\n",sfilename);
      return(EXIT_FAILURE);
    }
  //10 is the write-data command len: 2 byte for the command, 4 bytes for the data length, 4 bytes for the data address
  new_chunk_size=chunk_size-HEADER_LEN-CRC_LEN-COMMAND_LEN-10;
  //if the mode is RSA mode, the signature len shall also be taken into account
  if(SCP_FLORA_RSA==session_mode)
    new_chunk_size-=SIGNATURE_LEN;
  chunk_len=0;
  i=0;
  //parse data
  //grouping them by contiguous addresses, up to CHUNK-SIZE
  //meaning each time an address is not the next one than the previous one
  //or each time a block of CHUNK-SIZE data has been built,
  //a write-mem is issued
  //until the end.
  while(i<data_len)
    {
      chunk_len=0;
      chunk[chunk_len]=data[i];
      //the block starting address (needed for write-mem)
      chunk_addr=addr[i];
      chunk_len++;
      i++;
      //while consecutive addresses and not too big chunk
      while((addr[i]==addr[i-1]+1)&&(chunk_len<new_chunk_size)&&(i<data_len))
	{
	  //accumulate
	  chunk[chunk_len]=data[i];
	  chunk_len++;
	  i++;
	}
      //the last packet is filled up with FF if needed
      //2.3.6 (#2252): not filled up with FF anymore
      if(i==data_len)
	{
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	  //2.3.6 (#2252): not filled up with FF anymore
	  //	  new_chunk_len=((chunk_len/16)+1)*16;
	  //	  for(j=chunk_len;j<new_chunk_len;j++)
	  //chunk[j]=0xFF;
	  //chunk_len=new_chunk_len;
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	}
      resu=write_mem(chunk,chunk_len,chunk_addr);
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR in write_mem\n");
	  return(EXIT_FAILURE);
	}
      usip();
      ack();
      write_mem_response();
      host();
      ack();
    }
  if(TRUE==verbose)
    {
      for(i=0;i<chunk_len;i++)
	printf("%02x",chunk[i]);
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

int verify_data_payload(u8 *data,int data_len,int data_addr)
{
  int i;
  payload[ipayload++]=(DATA<<4)^config_struct.pp;
  payload[ipayload++]=tr_id;
  //the tr-id is incremented after the response
  //  tr_id=(tr_id+1)%256;
  // size in on 2 bytes !! especially important for long frames
  payload[ipayload++]=(2+4+4+data_len)>>8;
  payload[ipayload++]=(2+4+4+data_len)&255;
  payload[ipayload++]=VERIFY_MEM>>8;
  payload[ipayload++]=VERIFY_MEM&255;
  //set up the start addr
  // on 4 bytes
  for(i=3;i>=0;i--)
    payload[ipayload++]=(data_addr>>(8*i))&255;
  //set up the length
  // on 4 bytes
  for(i=3;i>=0;i--)
    payload[ipayload++]=(data_len>>(8*i))&255;
  for(i=0;i<data_len;i++)
    payload[ipayload++]=data[i];
  return(EXIT_SUCCESS);
}

//SCP and SCP FLORA shared command (named COMPARE-DATA in FLORA)
int verify_data(u8 *data,int data_len,int data_addr)
{
  int err;
  if(SBL==session_mode)
    {
      printf("ERROR: command not supported\n");
      return(EXIT_FAILURE);
    }
  ipayload=0;
  seq++;
  verify_data_payload(data,data_len,data_addr);
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
      err=rsa_sign_payload();
      if(EXIT_FAILURE==err)
        return(err);
    }
  else
    if(SCP_ANGELA_ECDSA==session_mode)
      {
	err=ecdsa_sign_payload();
	if(EXIT_FAILURE==err)
	  return(err);
      }
    else
      {
	if(SCP_PP_E_CMAC==config_struct.pp)
	  {
	    //encrypt plain payload
	    aes_encrypt_payload();
	    if(TRUE==verbose)
	      printf("payload encrypted\n");
	  }
	if(TRUE==verbose)
	  printf("payload signed\n");
	//cmac performed on encrypted payload
	aes_cmac_payload();
      }
  sprintf(message,"%s-VERIFY-DATA",idf_ctl[DATA_TRANSFER]);
  synchro();
  data_code();
  //add payload size to header
  add_byte(ipayload>>8);
  add_byte(ipayload&255);
  add_channel_id_seq();
  //compute header crc (shall be done after payload size be known)
  header_crc();
  add_payload();
  //finally add payload crc
  payload_crc();
  sprintf(name_file,"verify_data");
  send();
  return(EXIT_SUCCESS);
}

int verify_file(char *sfilename,char *ptr_address_offset)
{
  int i;
  u8 chunk[MAX_CHUNK_SIZE];
  int chunk_len;
  int chunk_addr;
  if(EXIT_SUCCESS==extension(".s19",sfilename))
    read_s19(sfilename,ptr_address_offset);
  else
      if(EXIT_SUCCESS==extension(".s20",sfilename))
    read_s20(sfilename,ptr_address_offset);
  else
    {
      printf("ERROR: <%s> file extension not supported (only .s19 and .s20)\n",sfilename);
      return(EXIT_FAILURE);
    }

chunk_len=0;
  i=0;
  //parse data
  //grouping them by contiguous addresses, up to CHUNK-SIZE
  //meaning each time an address is not the next one than the previous one
  //or each time a block of CHUNK-SIZE data has been built,
  //a write-mem is issued
  //until the end.
  while(i<data_len)
    {
      chunk[chunk_len]=data[i];
      //the block starting address (needed for write-mem)
      chunk_addr=addr[i];
      chunk_len++;
      i++;
      while((addr[i]==addr[i-1]+1)&&(chunk_len<chunk_size)&&(i<data_len))
	{
	  chunk[chunk_len]=data[i];
	  chunk_len++;
	  i++;
	}
      //the last packet is filled up with FF if needed
      //2.3.6 (#2252): not filled up with FF anymore
      if(i==data_len)
	{
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	  //2.3.6 (#2252): not filled up with FF anymore
	  //	  new_chunk_len=((chunk_len/16)+1)*16;
	  //	  for(j=chunk_len;j<new_chunk_len;j++)
	  //	    chunk[j]=0xFF;
	  //	  chunk_len=new_chunk_len;
	  if(TRUE==verbose)
	    printf("last chunk (%d bytes):",chunk_len);
	}

      verify_data(chunk,chunk_len,chunk_addr);
      chunk_len=0;
      usip();
      ack();
      verify_data_response();
      host();
      ack();
    }
  return(EXIT_SUCCESS);
}

int help(void)
{
  int i;
  printf("supported commands:\n");
  for(i=0;i<MAX_SCP_COMMAND;i++)
    {
      printf("%s",idf_scp_cmd[i]);
      if(mode[i]==MSP_MAXQ1852_ECDSA)
	printf("MSP_MAXQ1852_ECDSA\n");
      else
	if((mode[i]&3)==SCP_RSA)
	  printf("\tSCP");
	else
	  printf("\t");
      if((mode[i]&4)==SCP_FLORA_RSA)
	printf("\tSCP-FLORA");
      printf("\n");
    }
  return(EXIT_SUCCESS);
}

int process_command(char *line)
{
  int i,j,k,l;
  int found;
  char loline[MAX_STRING];
  for(i=0;i<(int)strlen(line);i++)
    loline[i]=(char)tolower((int)line[i]);
  //parse every command
  for(found=0,i=0;i<MAX_SCP_COMMAND;i++)
    //if command found
    if(strstr(loline,idf_scp_cmd[i])!=NULL)
      {
	found=1;
	//process params, if any
	//1st skip the identifier string
	j=strlen(idf_scp_cmd[i]);
	//2nd, skip whitespaces
	nb_params=0;
	//while not eol
	while(j<(int)strlen(line)-1)
	  {
	    //while space, go on
	    while(' '==line[j])
	      j++;
	    //if not eol
	    if(j==(int)strlen(line)-1)
	      break;
	    else
	      {
		k=0;
		//while no space, retrieve param
		while(' '!=line[j] && j<(int)strlen(line)-1)
		  {
		    params[nb_params][k]=line[j];
		    k++;
		    j++;
		  }
		params[nb_params][k]='\0';
		k++;
		//display param
		if(TRUE==verbose)
		  {
		    printf("params[%d]:",nb_params);
		    for(l=0;l<k-1;l++)
		      printf("%c",params[nb_params][l]);
		    printf("\n");
		  }
		nb_params++;
		//go on
	      }
	  }
	break;
      }
  if(0==found)
    return(COMMAND_UNKNOWN);
  //return command identifier, even unknown command
  return(i);
}

void maxq1852_synchro(void)
{
  iframe=0;
  payload[ipayload++]=MAXQ1852_SCDESIGNATOR;
  //reserved 2 bytes for length, computed later
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
}

void maxq1852_add_trid()
{
  payload[ipayload++]=trid>>24;
  payload[ipayload++]=(trid>>16)&255;
  payload[ipayload++]=(trid>>8)&255;
  payload[ipayload++]=trid&255;
}

void maxq1852_add_seq()
{
  payload[ipayload++]=seq&255;
  payload[ipayload++]=seq>>8;
  seq=(seq+1)&0xffff;
}

void maxq1852_add_seq_noincr()
{
  payload[ipayload++]=seq&255;
  payload[ipayload++]=seq>>8;
  //  seq=(seq+1)&0xffff;
}
void maxq1852_response_synchro(void)
{
  iframe=0;
}

void maxq1852_generic_response(void)
{
  maxq1852_response_synchro();
  ipayload=0;
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]='A';
  payload[ipayload++]='G';
  payload[ipayload++]='P';
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=MAXQ1852_SCPROMPT;
}

void maxq1852_agf_response(void)
{
  maxq1852_response_synchro();
  ipayload=0;
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]='A';
  payload[ipayload++]='G';
  payload[ipayload++]='F';
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=0x00;
  payload[ipayload++]=MAXQ1852_SCPROMPT;
}

void engage_pllo_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"engage_pllo_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_ENGAGE_PLLO]);
  send();
}

void engage_pllo_payload(void)
{

  payload[ipayload++]='P';
  payload[ipayload++]='L';
  payload[ipayload++]='L';
  payload[ipayload++]='O';
}

int engage_pllo(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_ENGAGE_PLLO;

  engage_pllo_payload();
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"engage_pllo");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_ENGAGE_PLLO]);
  send();
  return(EXIT_SUCCESS);
}

void load_customer_key_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"load_customer_key_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY]);
  send();
}

int load_customer_key_payload(char *pub_x,char *pub_y)
{
  int i;
  int one_byte;
  u8 xq[ECDSA_MODULUS_LEN];
  u8 yq[ECDSA_MODULUS_LEN];

  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_x[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_x parameter <%s> incorrectly formatted as a number\n",pub_x);
	  return(EXIT_FAILURE);
	}
      //      payload[ipayload++]=one_byte;
      //3.5.0
      xq[i]=one_byte;
    }
  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_y[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_y parameter <%s> incorrectly formatted as a number\n",pub_y);
	  return(EXIT_FAILURE);
	}
      //      payload[ipayload++]=one_byte;
      yq[i]=one_byte;
    }
  //3.5.0
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    payload[ipayload++]=xq[ECDSA_MODULUS_LEN-1-i];
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    payload[ipayload++]=yq[ECDSA_MODULUS_LEN-1-i];
  return(EXIT_SUCCESS);
}

int load_customer_key(char *pub_x,char *pub_y)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_LOAD_CUSTOMER_KEY;

  load_customer_key_payload(pub_x,pub_y);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"load_customer_key");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY]);
  send();
  return(EXIT_SUCCESS);
}

void verify_customer_key_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"verify_customer_key_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY]);
  send();
}

//3.5.0
int verify_customer_key_payload(char *pub_x,char *pub_y)
{
  int i;
  int one_byte;
  u8 xq[ECDSA_MODULUS_LEN];
  u8 yq[ECDSA_MODULUS_LEN];

  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_x[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_x parameter <%s> incorrectly formatted as a number\n",pub_x);
	  return(EXIT_FAILURE);
	}
      //      payload[ipayload++]=one_byte;
      //3.5.0
      xq[i]=one_byte;
    }
  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_y[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_y parameter <%s> incorrectly formatted as a number\n",pub_y);
	  return(EXIT_FAILURE);
	}
      //      payload[ipayload++]=one_byte;
      yq[i]=one_byte;
    }
  //3.5.0
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    payload[ipayload++]=xq[ECDSA_MODULUS_LEN-1-i];
  for(i=0;i<ECDSA_MODULUS_LEN;i++)
    payload[ipayload++]=yq[ECDSA_MODULUS_LEN-1-i];
  return(EXIT_SUCCESS);
}

/*int verify_customer_key_payload(char *pub_x,char *pub_y)
{
  int i;
  int one_byte;
  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_x[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_x parameter <%s> incorrectly formatted as a number\n",pub_x);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<config_struct.ecdsa_len;i++)
    {
      if(0==sscanf(&(pub_y[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: pub_y parameter <%s> incorrectly formatted as a number\n",pub_y);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
  }*/

int verify_customer_key(char *pub_x,char *pub_y)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_VERIFY_CUSTOMER_KEY;

  verify_customer_key_payload(pub_x,pub_y);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"verify_customer_key");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY]);
  send();
  return(EXIT_SUCCESS);
}

void activate_customer_key_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"activate_customer_key_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY]);
  send();
}

int activate_customer_key(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_ACTIVATE_CUSTOMER_KEY;

  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"activate_customer_key");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY]);
  send();
  return(EXIT_SUCCESS);
}

void generate_application_startup_signature_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"generate_application_startup_signature_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE]);
  send();
}

int generate_application_startup_signature(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE;

  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"generate_application_startup_signature");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE]);
  send();
  return(EXIT_SUCCESS);
}

void verify_application_startup_signature_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"verify_application_startup_signature_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE]);
  send();
}

int verify_application_startup_signature(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE;

  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"verify_application_startup_signature");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE]);
  send();
  return(EXIT_SUCCESS);
}

void write_register_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"write_register_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_WRITE_REGISTER]);
  send();
}
int write_register_payload(char *reg,char *value)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(reg[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: reg parameter <%s> incorrectly formatted as a number\n",reg);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(value[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: value parameter <%s> incorrectly formatted as a number\n",value);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int write_register(char *reg,char *value)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_WRITE_REGISTER;

  write_register_payload(reg,value);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"write_register");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_WRITE_REGISTER]);
  send();
  return(EXIT_SUCCESS);
}

void read_register_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"read_register_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_READ_REGISTER]);
  send();
}
int read_register_payload(char *reg)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(reg[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: reg parameter <%s> incorrectly formatted as a number\n",reg);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int read_register(char *reg)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_READ_REGISTER;

  read_register_payload(reg);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"read_register");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_READ_REGISTER]);
  send();
  return(EXIT_SUCCESS);
}
void load_code_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"load_code_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CODE]);
  send();
}

int load_code_payload(char *addr,char *code)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(addr[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: addr parameter <%s> incorrectly formatted as a number\n",addr);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<(int)strlen(code);i+=2)
    {
      if(0==sscanf(&(code[i]),"%02x",&one_byte))
	{
	  printf("ERROR: code parameter <%s> incorrectly formatted as a number\n",code);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int load_code(char *addr,char *code)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_LOAD_CODE;

  load_code_payload(addr,code);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"load_code");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_CODE]);
  send();
  return(EXIT_SUCCESS);
}

int load_file(char *hexfilename)
{
  int i,k;
  int last_index;
  u8 *dataloc;
  char schunk_addr[10];
  char schunk[2000];
  char schunk_tmp[2000];
  int allff;
  u8 ad1,ad2,ad3,ad4;
  u32 ad;
  //  int hex_chunk_size=MAXQ1852_CHUNK_SIZE;
  int hex_chunk_size=64;
  int resu;
  dataloc=(u8*)malloc(sizeof(u8)*1024*1024);
  if(NULL==data)
    {
      printf("ERROR: <data> allocation is not possible (%dMB requested)\n",config_struct.flash_mb);
      return(EXIT_FAILURE);
    }
  if(EXIT_SUCCESS==extension(".hex",hexfilename))
    read_hex(hexfilename);
  else
    {
      printf("ERROR: <%s> file extension not supported (only .hex)\n",hexfilename);
      return(EXIT_FAILURE);
    }
  for(i=0;i<1024*1024;i++)
    dataloc[i]=0xff;
  for(i=0;i<data_len;i++)
    dataloc[addr[i]]=data[i];
  last_index=addr[data_len-1];
  for(i=0;i<last_index;i+=hex_chunk_size)
    {
      ad=(hex_extended_address<<16)^(i);
      ad1=ad>>24;
      ad2=(ad>>16)&255;
      ad3=(ad>>8)&255;
      ad4=(ad&255);
      sprintf(schunk_addr,"%08x",(ad4<<24)^(ad3<<16)^(ad2<<8)^(ad1));

      sprintf(schunk_tmp,"");
      for(allff=1,k=0;k<hex_chunk_size;k++)
	{
	  if(0xff!=dataloc[i+k])
	    {
	      allff=0;
	    }
	  sprintf(schunk,"%s%02x",schunk_tmp,dataloc[i+k]);
	  sprintf(schunk_tmp,"%s",schunk);
	}
      //load-code only if not ff    
      if(0==allff)
	{
	  resu=load_code(schunk_addr,schunk);
	  if(EXIT_SUCCESS!=resu)
	    {
	      printf("ERROR in write_mem\n");
	      free(dataloc);
	      return(EXIT_FAILURE);
	    }
	  usip();
	  load_code_response();
	  host();
	}
    }
  free(dataloc);
  return(EXIT_SUCCESS);
}

void verify_code_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"verify_code_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CODE]);
  send();
}
int verify_code_payload(char *addr,char *code)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(addr[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: addr parameter <%s> incorrectly formatted as a number\n",addr);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<(int)strlen(code);i+=2)
    {
      if(0==sscanf(&(code[i]),"%02x",&one_byte))
	{
	  printf("ERROR: code parameter <%s> incorrectly formatted as a number\n",code);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int verify_code(char *addr,char *code)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_VERIFY_CODE;

  verify_code_payload(addr,code);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"verify_code");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_CODE]);
  send();
  return(EXIT_SUCCESS);
}

int verify_code_file(char *hexfilename)
{
  int i,k;
  int last_index;
  u8 *dataloc;
  char schunk_addr[10];
  char schunk[2000];
  char schunk_tmp[2000];
  int allff;
  u8 ad1,ad2,ad3,ad4;
  u32 ad;
  //  int hex_chunk_size=MAXQ1852_CHUNK_SIZE;
  int hex_chunk_size=64;
  int resu;
  dataloc=(u8*)malloc(sizeof(u8)*1024*1024);
  if(NULL==data)
    {
      printf("ERROR: <data> allocation is not possible (%dMB requested)\n",config_struct.flash_mb);
      return(EXIT_FAILURE);
    }
  if(EXIT_SUCCESS==extension(".hex",hexfilename))
    read_hex(hexfilename);
  else
    {
      printf("ERROR: <%s> file extension not supported (only .hex)\n",hexfilename);
      return(EXIT_FAILURE);
    }
  for(i=0;i<1024*1024;i++)
    dataloc[i]=0xff;
  for(i=0;i<data_len;i++)
    dataloc[addr[i]]=data[i];
  last_index=addr[data_len-1];
  for(i=0;i<last_index;i+=hex_chunk_size)
    {
      ad=(hex_extended_address<<16)^(i);
      ad1=ad>>24;
      ad2=(ad>>16)&255;
      ad3=(ad>>8)&255;
      ad4=(ad&255);
      sprintf(schunk_addr,"%08x",(ad4<<24)^(ad3<<16)^(ad2<<8)^(ad1));

      sprintf(schunk_tmp,"");
      for(allff=1,k=0;k<hex_chunk_size;k++)
	{
	  if(0xff!=dataloc[i+k])
	    {
	      allff=0;
	    }
	  sprintf(schunk,"%s%02x",schunk_tmp,dataloc[i+k]);
	  sprintf(schunk_tmp,"%s",schunk);
	}
      //load-code only if not ff    
      if(0==allff)
	{
	  resu=verify_code(schunk_addr,schunk);
	  if(EXIT_SUCCESS!=resu)
	    {
	      printf("ERROR in write_mem\n");
	      free(dataloc);
	      return(EXIT_FAILURE);
	    }
	  usip();
	  verify_code_response();
	  host();
	}
    }
  free(dataloc);
  return(EXIT_SUCCESS);
}

void load_data_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"load_data_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_DATA]);
  send();
}
int load_data_payload(char *addr,char *data)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(addr[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: addr parameter <%s> incorrectly formatted as a number\n",addr);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<(int)strlen(data);i+=2)
    {
      if(0==sscanf(&(data[i]),"%02x",&one_byte))
	{
	  printf("ERROR: data parameter <%s> incorrectly formatted as a number\n",data);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int load_data(char *addr,char *data)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_LOAD_DATA;

  load_data_payload(addr,data);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"load_data");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_LOAD_DATA]);
  send();
  return(EXIT_SUCCESS);
}

void verify_maxq1852_data_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"verify_data_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_DATA]);
  send();
}
int verify_maxq1852_data_payload(char *addr,char *data)
{
  int i;
  int one_byte;
  for(i=0;i<4;i++)
    {
      if(0==sscanf(&(addr[i*2]),"%02x",&one_byte))
	{
	  printf("ERROR: addr parameter <%s> incorrectly formatted as a number\n",addr);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  for(i=0;i<(int)strlen(data);i+=2)
    {
      if(0==sscanf(&(data[i]),"%02x",&one_byte))
	{
	  printf("ERROR: data parameter <%s> incorrectly formatted as a number\n",data);
	  return(EXIT_FAILURE);
	}
      payload[ipayload++]=one_byte;
    }
  return(EXIT_SUCCESS);
}

int verify_maxq1852_data(char *addr,char *data)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_VERIFY_DATA;

  verify_maxq1852_data_payload(addr,data);
  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"verify_data");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_VERIFY_DATA]);
  send();
  return(EXIT_SUCCESS);
}

void erase_code_flash_area_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"erase_code_flash_area_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA]);
  send();
}
int erase_code_flash_area(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_ERASE_CODE_FLASH_AREA;

  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  ecdsa_sign_payload();
  sprintf(name_file,"erase_code_flash_area");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA]);
  send();
  return(EXIT_SUCCESS);
}

void erase_all_flash_areas_response(void)
{
  maxq1852_generic_response();
  sprintf(name_file,"erase_all_flash_areas_response");
  add_payload();
  sprintf(message,"%s-response",idf_scp_cmd[COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS]);
  send();
}
int erase_all_flash_areas(void)
{
  int length;
  ipayload=0;
  maxq1852_synchro();
  //  payload[ipayload++]=MAXQ1852_SCOFFSET;
  payload[ipayload++]=MAXQ1852_ERASE_ALL_FLASH_AREAS;

  maxq1852_add_trid();
  maxq1852_add_seq();

  //now, we can update the 2 length bytes
  //  payload[MAXQ1852_SC_LEN_BYTE1]=ipayload&255;
  //  payload[MAXQ1852_SC_LEN_BYTE2]=ipayload>>8;
  length=ipayload+ECDSA_SIGNATURE_LEN-3;
  payload[MAXQ1852_SC_LEN_BYTE1]=length&255;
  payload[MAXQ1852_SC_LEN_BYTE2]=length>>8;
  printf("len=%02x\n",length);
  ecdsa_sign_payload();
  printf("hello\n");
  sprintf(name_file,"erase_all_flash_areas");
  add_payload();
  sprintf(message,"%s",idf_scp_cmd[COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS]);
  send();
  return(EXIT_SUCCESS);
}

//this function processes the commands listed in the script file "script_file"
//the ECDSA mode is managed out of the commands list
//these commands are closed to the SCP commands, but some include some abstraction
//e.g. the write-file, which writes the whole file, instead of write-data, which writes only one line
//the session opening is out of the script commands process
int process_script_maxq1852_ecdsa(void)
{

  char line[MAX_STRING];
  int command;
  FILE *fpscript;
  fpscript=fopen(script_file,"r");
  if(NULL==fpscript)
    {
      printf("ERROR: impossible to open <%s>\n",script_file);
      return(EXIT_FAILURE);
    }
  //initialize seq & ch id
  seq=1;
  host();
  while(fgets(line,MAX_STRING,fpscript)!=NULL)
    {
      if(TRUE==verbose)
	printf("<%s>",line);
      //if 1st char is a #, then considered as a comment and skip to next line
      if('#'==line[0])
	continue;
      //look for the command
      command=process_command(line);
      if(TRUE==verbose)
	printf("command=%s\n",idf_scp_cmd[command]);
      if(COMMAND_UNKNOWN==command)
	{
	  printf("ERROR: the command <%s> is unknown or not supported; check the script file <%s>\n",line,script_file);
	  return(EXIT_FAILURE);
	}
      switch (command) {
      case COMMAND_HELP:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=help())
	      {
		printf("ERROR: help\n");
		return(EXIT_FAILURE);
	      }
	  }
	else
	  {
	    printf("ERROR for help command\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_ENGAGE_PLLO:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=engage_pllo())
	      {
		printf("ERROR: engage-pllo\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    engage_pllo_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for engage-pllo command: engage-pllo\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=erase_code_flash_area())
	      {
		printf("ERROR: erase-code-flash-area\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    erase_code_flash_area_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for erase-code-flash-area command: erase-code-flash-area\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=erase_all_flash_areas())
	      {
		printf("ERROR: erase-all-flash-areas\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    erase_all_flash_areas_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for erase-all-flash-areas command: erase-all-flash-areas\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=activate_customer_key())
	      {
		printf("ERROR: activate-customer-key\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    activate_customer_key_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for activate-customer-key command: activate-customer-key\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=generate_application_startup_signature())
	      {
		printf("ERROR: generate-application-startup-signature\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    generate_application_startup_signature_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for generate-application-startup-signature command: generate-application-startup-signature\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE:
	if(0==nb_params)
	  {
	    if(EXIT_SUCCESS!=verify_application_startup_signature())
	      {
		printf("ERROR: verify-application-startup-signature\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    verify_application_startup_signature_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for verify-application-startup-signature command: verify-application-startup-signature\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=load_customer_key(params[0],params[1]))
	      {
		printf("ERROR: load-customer-key\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    load_customer_key_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for load-customer-key command: load-customer-key <pub-x> <pub-y>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=verify_customer_key(params[0],params[1]))
	      {
		printf("ERROR: verify-customer-key\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    verify_customer_key_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for verify-customer-key command: verify-customer-key <pub-x> <pub-y>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_WRITE_REGISTER:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=write_register(params[0],params[1]))
	      {
		printf("ERROR: write-register\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    write_register_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for write-register: write-register <register> <value>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_READ_REGISTER:
	if(1==nb_params)
	  {
	    if(EXIT_SUCCESS!=read_register(params[0]))
	      {
		printf("ERROR: read-register\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    read_register_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for write-register: read-register <register>\n");
	    return(EXIT_FAILURE);
	  }
	break;
	    //write-only-file is an abstraction for write-data, used in scp and scp-flora
      case COMMAND_MAXQ1852_LOAD_FILE:
	if(1==nb_params)
	  {
	    if(EXIT_SUCCESS!=load_file(params[0]))
	      {
		printf("ERROR: load-file\n");
		return(EXIT_FAILURE);
	      }
	  }
	else
	  if(2==nb_params)
	    {
	      if(EXIT_SUCCESS!=load_file(params[0]))
		{
		  printf("ERROR: load-file\n");
		  return(EXIT_FAILURE);
		}
	    }
	  else
	    {
	      printf("ERROR: incorrect format for WRITE-ONLY command: write-file-only <s19file> <address-offset:optional>\n");
	      return(EXIT_FAILURE);
	    }
	break;
      case COMMAND_MAXQ1852_LOAD_CODE:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=load_code(params[0],params[1]))
	      {
		printf("ERROR: load-code\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    load_code_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for load-code: load-code <address> <code>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_VERIFY_FILE:
	if(1==nb_params)
	  {
	    if(EXIT_SUCCESS!=verify_code_file(params[0]))
	      {
		printf("ERROR: verify-file\n");
		return(EXIT_FAILURE);
	      }
	  }
	else
	  if(2==nb_params)
	    {
	      if(EXIT_SUCCESS!=verify_code_file(params[0]))
		{
		  printf("ERROR: verify-file\n");
		  return(EXIT_FAILURE);
		}
	    }
	  else
	    {
	      printf("ERROR: incorrect format for WRITE-ONLY command: verify-code-file-only <s19file> <address-offset:optional>\n");
	      return(EXIT_FAILURE);
	    }
	break;
      case COMMAND_MAXQ1852_VERIFY_CODE:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=verify_code(params[0],params[1]))
	      {
		printf("ERROR: verify-code\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    verify_code_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for verify-code: verify-code <address> <code>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_LOAD_DATA:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=load_data(params[0],params[1]))
	      {
		printf("ERROR: load-data\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    load_data_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for load-data: load-data <address> <data>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      case COMMAND_MAXQ1852_VERIFY_DATA:
	if(2==nb_params)
	  {
	    if(EXIT_SUCCESS!=verify_maxq1852_data(params[0],params[1]))
	      {
		printf("ERROR: verify-data\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    verify_maxq1852_data_response();
	    host();
	  }
	else
	  {
	    printf("ERROR: incorrect format for verify-data: verify-data <address> <code>\n");
	    return(EXIT_FAILURE);
	  }
	break;
      default:
	printf("ERROR: the command <%s> is not supported\n",line);
	return(EXIT_FAILURE);
      }
    }
  (void)fclose(fpscript);
  return(EXIT_SUCCESS);
}

//this function processes the commands listed in the script file "script_file"
//the AES or RSA mode is managed out of the commands list
//these commands are closed to the SCP commands, but some include some abstraction
//e.g. the write-file, which writes the whole file, instead of write-data, which writes only one line
//the session opening is out of the script commands process
int process_script(void)
{
  char line[MAX_STRING];
  int command;
  FILE *fpscript;
  //check if requested size is not too large compared to what supported (i.e. MAX_FLASH_MB), because of int coding)
  if(config_struct.flash_mb>MAX_FLASH_MB)
    {
      printf("ERROR: requested flash size is too large (%dMB) while limited to %dMB\n",config_struct.flash_mb,MAX_FLASH_MB);
      return(EXIT_FAILURE);
    }
  //dynamic allocation of *data, which contains the meaningful binary file bytes, synchronized
  data=(u8*)malloc(sizeof(u8)*1024*1024*config_struct.flash_mb);
  if(NULL==data)
    {
      printf("ERROR: <data> allocation is not possible (%dMB requested)\n",config_struct.flash_mb);
      return(EXIT_FAILURE);
    }
  //dynamic allocation of *addr, which contains the addresses of meaningful binary file bytes
  addr=(int*)malloc(sizeof(int)*1024*1024*config_struct.flash_mb);
  if(NULL==addr)
    {
      printf("ERROR: <addr> allocation is not possible (%dMB requested)\n",config_struct.flash_mb);
      return(EXIT_FAILURE);
    }
  max_data_size=1024*1024*config_struct.flash_mb;
  if(MSP_MAXQ1852_ECDSA==session_mode)
    {
      if(TRUE==verbose)
	printf("<session MSP-MAXQ1852-ECDSA>\n");
      fprintf(fp,"<session MSP-MAXQ1852-ECDSA>\n");
      process_script_maxq1852_ecdsa();
    }
  else
    {
      if(SCP_RSA==session_mode)
	{
	  if(TRUE==verbose)
	    printf("<session SCP-RSA>\n");
	  fprintf(fp,"<session SCP-RSA>\n");
	}
      if(SCP_FLORA_RSA==session_mode)
	{
	  if(TRUE==verbose)
	    printf("<session SCP-FLORA-RSA>\n");
	  fprintf(fp,"<session SCP-FLORA-RSA>\n");
	}
      if(SCP_ANGELA_ECDSA==session_mode)
	{
	  if(TRUE==verbose)
	    printf("<session SCP-ANGELA-ECDSA>\n");
	  fprintf(fp,"<session SCP-ANGELA-ECDSA>\n");
	}
      if(SCP_FLORA_AES==session_mode)
	{
	  if(TRUE==verbose)
	    printf("<session SCP-FLORA-AES>\n");
	  fprintf(fp,"<session SCP-FLORA-AES>\n");
	}
      if(SCP_ON_AES==session_mode)
	{
	  if(TRUE==verbose)
	    printf("<session SCP-AES>\n");
	  fprintf(fp,"<session SCP-AES>\n");
	}
      fpscript=fopen(script_file,"r");
      if(NULL==fpscript)
	{
	  printf("ERROR: impossible to open <%s>\n",script_file);
	  return(EXIT_FAILURE);
	}
      //initialize seq & ch id
      iframe=0;
      seq=0;
      ch_id=9;
      //bug #1623 correction
      tr_id=0;
      host();
      connection_request();
      usip();
      connection_reply();
      host();
      ack();
      host();
      hello_request();
      usip();
      ack();
      hello_reply();
      host();
      ack();
      //if in AES mode, the challenge/response is performed
      //note that we are in fixed-random-number mode
      if(SCP_ON_AES==session_mode || SCP_FLORA_AES==session_mode)
	{
	  challenge();
	  usip();
	  ack();
	  challenge_response();
	  host();
	  ack();
	}
      while(fgets(line,MAX_STRING,fpscript)!=NULL)
	{
	  if(TRUE==verbose)
	    printf("%s",line);
	  //if 1st char is a #, then considered as a comment and skip to next line
	  if('#'==line[0])
	    continue;
	  //look for the command
	  command=process_command(line);
	  if(TRUE==verbose)
	    printf("command=%s\n",idf_scp_cmd[command]);
	  if(COMMAND_UNKNOWN==command)
	    {
	      printf("ERROR: the command <%s> is unknown or not supported; check the script file <%s>\n",line,script_file);
	      return(EXIT_FAILURE);
	    }
	  switch (command) {
	  case COMMAND_WRITE_CONFIGURATION:
	    printf("this command is not implemented\n");
	    break;
	  case COMMAND_HELP:
	    if(0==nb_params)
	      {
		if(EXIT_SUCCESS!=help())
		  {
		    printf("ERROR: help\n");
		    return(EXIT_FAILURE);
		  }
	      }
	    else
	      {
		printf("ERROR for help command\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //write-file is an abstraction for write-data+erase-data, used in scp and scp-flora
	  case COMMAND_WRITE_FILE:
	    if(1==nb_params)
	      {
		if(EXIT_SUCCESS!=write_file(params[0],NULL))
		  {
		    printf("ERROR: write-file\n");
		    return(EXIT_FAILURE);
		  }
	      }
	    else
	      if(1==nb_params)
		{
		  if(EXIT_SUCCESS!=write_file(params[0],params[1]))
		    {
		      printf("ERROR: write-file\n");
		      return(EXIT_FAILURE);
		    }
		}
	      else
		{
		  printf("ERROR: incorrect format for WRITE-FILE command: write-file <s19file> <address-offset:optional>\n");
		  return(EXIT_FAILURE);
		}
	    break;
	    //write-only-file is an abstraction for write-data, used in scp and scp-flora
	  case COMMAND_WRITE_ONLY:
	    if(1==nb_params)
	      {
		if(EXIT_SUCCESS!=write_only(params[0],NULL))
		  {
		    printf("ERROR: write-only\n");
		    return(EXIT_FAILURE);
		  }
	      }
	    else
	      if(2==nb_params)
		{
		  if(EXIT_SUCCESS!=write_only(params[0],params[1]))
		    {
		      printf("ERROR: write-only\n");
		      return(EXIT_FAILURE);
		    }
		}
	      else
		{
		  printf("ERROR: incorrect format for WRITE-ONLY command: write-file-only <s19file> <address-offset:optional>\n");
		  return(EXIT_FAILURE);
		}
	    break;
	    //ERASE_DATA is common to SCP and SCP-FLORA
	  case COMMAND_ERASE_DATA:
	    if(2==nb_params)
	      {
		if(EXIT_SUCCESS!=del_data(params[0],params[1]))
		  {
		    printf("ERROR: erase-file\n");
		    return(EXIT_FAILURE);
		  }
		// #bug 2130: missing packets added
		usip();
		ack();
		del_mem_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for ERASE-FILE command: erase-file <hex-start-addr> <hex-length>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //VERIFY-FILE is an abstraction for VERIFY-DATA in SCP, renamed in COMPARE-DATA in SCP-FLORA
	  case COMMAND_VERIFY_FILE:
	    if(1==nb_params)
	      {
		if(EXIT_SUCCESS!=verify_file(params[0],NULL))
		  {
		    return(EXIT_FAILURE);
		  }
	      }
	    else
	      if(2==nb_params)
		{
		  if(EXIT_SUCCESS!=verify_file(params[0],params[1]))
		    {
		      return(EXIT_FAILURE);
		    }
		}
	      else
		{
		  printf("ERROR: incorrect format for VERIFY-FILE command: verify-file <s19file> <address-offset:optional>\n");
		  return(EXIT_FAILURE);
		}
	    break;
	    //command for SCP only
	  case COMMAND_WRITE_BLPK:
	    if(1==nb_params)
	      {
		if(EXIT_SUCCESS!=write_bpk_blpk(params[0]))
		  {
		    printf("ERROR: write-bpk-blpk\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_bpk_blpk_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-BLPK command: write-blpk <hex-value>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //command for SCP only
	  case COMMAND_WRITE_FAK:
	    if(1==nb_params)
	      {
		if(EXIT_SUCCESS!=write_bpk_fak(params[0]))
		  {
		    printf("ERROR: write-bpk-fak\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_bpk_fak_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-FAK command: write-fak <hex-value>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //command for SCP only
	  case COMMAND_READ_CONFIGURATION:
	    if(EXIT_SUCCESS!=read_configuration())
	      {
		printf("ERROR: read-configuration\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    ack();
	    read_configuration_response();
	    host();
	    ack();
	    break;
	    //command for SCP only
	  case COMMAND_READ_MEMORY_MAPPING:
	    if(EXIT_SUCCESS!=mem_mapping())
	      {
		printf("ERROR: mem-mapping\n");
		return(EXIT_FAILURE);
	      }
	    usip();
	    ack();
	    mem_mapping_response();
	    host();
	    ack();
	    break;
	    //SCP FLORA specific command
	  case COMMAND_WRITE_BPK:
	    if(2==nb_params)
	      {
		if(EXIT_SUCCESS!=write_bpk(params[0],params[1]))
		  {
		    printf("ERROR: write-bpk\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_bpk_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-BPK command: write-bpk <hex-value> <offset in secure RAM>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //SCP FLORA/ANGELA specific command
	  case COMMAND_WRITE_CRK:
	    if(1==nb_params)
	      {
		//params[0] is the filename containing the RSA PubKey
		if(EXIT_SUCCESS!=write_crk(params[0]))
		  {
		    printf("ERROR: write-crk\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_crk_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-CRK command: write-crk <public key file name>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //SCP FLORA/ANGELA specific command
	  case COMMAND_REWRITE_CRK:
	    if(1==nb_params)
	      {
		//params[0] is the filename containing the RSA PubKey
		if(EXIT_SUCCESS!=rewrite_crk(params[0]))
		  {
		    printf("ERROR: rewrite-crk\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		rewrite_crk_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for REWRITE-CRK command: rewrite-crk <ECDSA public key file name>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //SCP FLORA/ANGELA specific command

	  case COMMAND_WRITE_OTP:
	    if(2==nb_params)
	      {
		if(EXIT_SUCCESS!=write_otp(params[0],params[1]))
		  {
		    printf("ERROR: write-otp\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_otp_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-OTP command: write-otp <offset in customer OTP> <hex-value>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //with 2 parameters, SCP FLORA/ANGELA specific command
	  case COMMAND_WRITE_TIMEOUT:
	    if(2==nb_params)
	      {
		if(EXIT_SUCCESS!=write_timeout(params[0][0],params[1]))
		  {
		    printf("ERROR: write-timeout\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		write_timeout_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for WRITE-TIMEOUT command: write-timeout <0:UART|1:USB> <hex-timeout-value-ms>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //SCP FLORA/ANGELA specific command
	  case COMMAND_KILL_CHIP:
	    if(0==nb_params)
	      {
		if(EXIT_SUCCESS!=kill_chip())
		  {
		    printf("ERROR: kill-chip\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		kill_chip_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for KILL-CHIP command: kill-chip w/o params\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    //SCP FLORA/ANGELA specific command
	  case COMMAND_EXECUTE_CODE:
	    if(1==nb_params)
	      {
		//params[0] is the address where the plugin starts
		if(EXIT_SUCCESS!=execute_code(params[0]))
		  {
		    printf("ERROR: execute-code\n");
		    return(EXIT_FAILURE);
		  }
		usip();
		ack();
		execute_code_response();
		host();
		ack();
	      }
	    else
	      {
		printf("ERROR: incorrect format for EXECUTE-CODE command: execute-code <32-bit address>\n");
		return(EXIT_FAILURE);
	      }
	    break;
	    
	  default:
	    printf("ERROR: the command <%s> is not supported\n",line);
	    return(EXIT_FAILURE);
	  }
	}
      (void)fclose(fpscript);
      disconnection_request();
      usip();
      disconnection_reply();
      return(EXIT_SUCCESS);
    }
  return(EXIT_SUCCESS);
}


int read_file_ascii_data(FILE*	p_pFile, const int p_iHexDataLength, u8* p_pucHexDataBuf, int*	p_piHexDataBufLen)
{
  int		l_iErr	 = EXIT_SUCCESS;
  int		l_iIndex = 0;
  int		l_iData  = 0; 
  if(p_pFile == NULL)
    {
      return EXIT_FAILURE;
    }
  if(p_pucHexDataBuf == NULL)
    {
      return EXIT_FAILURE;
    }
  if(p_piHexDataBufLen == NULL)
    {
      return EXIT_FAILURE;
    }
  if(*p_piHexDataBufLen == 0)
    {
      return EXIT_FAILURE;
    }
  if(*p_piHexDataBufLen < p_iHexDataLength)
    {
      return EXIT_FAILURE;
    }
  for(l_iIndex=0;l_iIndex<p_iHexDataLength;l_iIndex++)
    {
#ifndef _MXIM_HSM
      l_iErr=fscanf(p_pFile,"%02x",&l_iData);
#else
      l_iErr=fscanf_s(p_pFile,"%02x",&l_iData);
#endif//MXIM_HSM
      if(l_iErr!=1)
	{
	  printf("ERROR: read text file error\n");
	  return(EXIT_FAILURE);
	} 
      p_pucHexDataBuf[l_iIndex]=l_iData;
    }
  return EXIT_SUCCESS;
}

int read_file_rsa(u8* puk, int	size, u8* pukexp, u8* privexp, int expsize, char* filename)
{
  FILE*	l_pFile = NULL;
  int		l_iErr=0;
  char	l_tcLine[MAXLINE];
  fpos_t	l_llCurrentPos;
  int		l_iSize=0;
  int		l_iIndex=0;
  if(TRUE==verbose)
    {
      printf("<read_file_rsa <%s>>\n",filename);
    }
  if((filename == NULL)||(strlen(filename)==0))
    {
      printf("ERROR invalid rsa file: pointer is null or string paramter is empty\n");
      return(EXIT_FAILURE); 
    }
  l_pFile=fopen(filename,"r");
  if(l_pFile==NULL)
    {
      printf("ERROR on opening rsa file <%s>\n",filename);
      return(EXIT_FAILURE);
    }
  memset(puk,0,size);
  l_iSize=size;
  l_iErr = read_file_ascii_data(l_pFile, size, puk, &l_iSize);
  if(l_iErr != EXIT_SUCCESS)
    {
      printf("ERROR: read puk in rsa file error\n");
      return(EXIT_FAILURE);
    }
  //-- save current file position 
  fgetpos(l_pFile,&l_llCurrentPos);
  memset(l_tcLine,0,MAXLINE);
  fgets(l_tcLine,MAXLINE,l_pFile);
  fsetpos(l_pFile,&l_llCurrentPos);
  //this test does not work, so we do not try to detect the format of the file
  //the rsa file format is: modulus<cr>privexp<cr>pubexp<cr>
  /*  if(((int)strlen(l_tcLine)/2) == expsize)
    {
      //-- Read first public exponent and then private exponent
      memset(pukexp,0,expsize);
      l_iSize=expsize;
      l_iErr = read_file_ascii_data(l_pFile, expsize, pukexp, &l_iSize);
      if(l_iErr != EXIT_SUCCESS)
	{
	  printf("ERROR: read pukexp in rsa file error\n");
	  return(EXIT_FAILURE);
	}
      memset(privexp,0,size);
      l_iSize=size;
      l_iErr = read_file_ascii_data( l_pFile, size, privexp, &l_iSize);
      if(l_iErr != EXIT_SUCCESS)
	{
	  printf("ERROR: read privexp in rsa file error\n");
	  return(EXIT_FAILURE);
	}
    }
    else*/
    {
      //-- Read first private exponent and then public exponent
      memset(privexp,0,size);
      l_iSize=size;
      l_iErr = read_file_ascii_data(l_pFile, size, privexp, &l_iSize);
      if(l_iErr != EXIT_SUCCESS)
	{
	  printf("ERROR: read privexp in rsa file error\n");
	  return(EXIT_FAILURE);
	}
      memset(pukexp,0,expsize);
      l_iSize=expsize;
      l_iErr = read_file_ascii_data(l_pFile, expsize, pukexp, &l_iSize);
      if(l_iErr != EXIT_SUCCESS)
	{
	  printf("ERROR: read pukexp in rsa file error\n");
	  return(EXIT_FAILURE);
	}
    }
  if(TRUE==verbose)
    {
      for(l_iIndex=0;l_iIndex<size;l_iIndex++)
	printf("%02x",puk[l_iIndex]);
      printf("\n");
      for(l_iIndex=0;l_iIndex<expsize;l_iIndex++)
	printf("%02x",pukexp[l_iIndex]);
      printf("\n");
      for(l_iIndex=0;l_iIndex<size;l_iIndex++)
	printf("%02x",privexp[l_iIndex]);
      printf("\n");
    }
  fclose(l_pFile);
  return EXIT_SUCCESS;
}

int read_file_ecdsa(u8* puk_x, u8* puk_y, u8* privk, int size, char* filename)
{
  FILE*	l_pFile = NULL;
  int		l_iErr=0;
  int		l_iSize=0;
  int		l_iIndex=0;
  if(filename == NULL)
    {
      printf("ERROR read_file_ecdsa - invalid file name. \n");
      return EXIT_FAILURE;
    }
  if(TRUE==verbose)
    printf("<read_file_ecdsa <%s>>\n",filename);
  l_pFile=fopen(filename,"r");
  if(l_pFile==NULL)
    {
      printf("ERROR on opening <%s>\n",filename);
      return EXIT_FAILURE;
    }
  //-----------------//
  // ECDSA - PRIVK --//
  //-----------------------------------------------------------------
  memset(privk,0,size);
  l_iSize=size;
  l_iErr = read_file_ascii_data(l_pFile, size, privk, &l_iSize);
  if(l_iErr != EXIT_SUCCESS)
    {
      printf("ERROR: read privk in ecdsa key file error\n");
      return(EXIT_FAILURE);
    }
  //-----------------//
  // ECDSA - PUK_X --//
  //-----------------------------------------------------------------
  memset(puk_x,0,size);
  l_iSize=size;
  l_iErr = read_file_ascii_data(l_pFile, size, puk_x, &l_iSize);
  if(l_iErr != EXIT_SUCCESS)
    {
      printf("ERROR: read puk_x in ecdsa key file error\n");
      return(EXIT_FAILURE);
    }
  //-----------------//
  // ECDSA - PUK_Y --//
  //-----------------------------------------------------------------
  memset(puk_y,0,size);
  l_iSize=size;
  l_iErr = read_file_ascii_data( l_pFile, size, puk_y, &l_iSize);
  if(l_iErr != EXIT_SUCCESS)
    {
      printf("ERROR: read puk_y in ecdsa key file error\n");
      return(EXIT_FAILURE);
    }
  if(TRUE==verbose)
    {
      for(l_iIndex=0;l_iIndex<size;l_iIndex++)
	printf("%02x",puk_x[l_iIndex]);
      printf("\n");
      for(l_iIndex=0;l_iIndex<size;l_iIndex++)
	printf("%02x",puk_y[l_iIndex]);
      printf("\n");
      for(l_iIndex=0;l_iIndex<size;l_iIndex++)
	printf("%02x",privk[l_iIndex]);
      printf("\n");
    }
  fclose(l_pFile);
  return EXIT_SUCCESS;
}

int process_string(char* output, char* reference, char*	line, int fgets_correction, int* p_piFound)
{
  int		i,j;
  char	dupline[MAXLINE];
  char	dupreference[MAXLINE];
  if(p_piFound != NULL)
    {
      *p_piFound = 0;
    }
  for(i=0;i<(int)strlen(line);i++)
    dupline[i]=(char)toupper((int)line[i]);	
  dupline[strlen(line)]='\0';
  for(i=0;i<(int)strlen(reference);i++)
    dupreference[i]=(char)toupper((int)reference[i]);	
  dupreference[strlen(reference)]='\0';
  if(strstr(dupline,dupreference)!= NULL)
    {
      if(p_piFound != NULL)
	{
	  *p_piFound = 1;
	}
      for(j=-1,i=0;i<(int)strlen(line)-fgets_correction;i++)
	{
	  if(line[i]=='=')
	    j=i;
	}
      if(strlen(line)>MAXLINE)
	{
	  return(EXIT_FAILURE);
	}
      if(j!=-1)
	{
	  for(i=j+1;i<(int)strlen(line)-fgets_correction;i++)
	    output[i-j-1]=line[i];
	}
      else
	{
	  return(EXIT_FAILURE);
	}
      output[i-j-1]='\0';
    }
  return(EXIT_SUCCESS);
}

int process_hexvalue(int *value_len,u8 *value,char *reference,char *line,int fgets_correction)
{
  int i,j,k;
  char dupline[MAXLINE];
  char dupreference[MAXLINE];
  for(i=0;i<(int)strlen(line);i++)
    dupline[i]=(char)toupper((int)line[i]);
  dupline[strlen(line)]='\0';
  for(i=0;i<(int)strlen(reference);i++)
    dupreference[i]=(char)toupper((int)reference[i]);
  dupreference[strlen(reference)]='\0';
  k=-1;
  if(strstr(dupline,dupreference)==dupline)
    {
      found=1;
      for(j=-1,i=0;i<(int)strlen(line)-fgets_correction;i++)
	if(line[i]=='=')
	  j=i;
      if((((int)strlen(line)-fgets_correction-j-1)%2)!=0)
	{
	  //the hexadecimal values shall be a multiple of 2 chars
	  printf("ERROR: hexadecimal value shall be 2-digit bytes (%d digits found)\n",(int)strlen(line)-fgets_correction-j-1);
	  *value_len=k;
	  return(EXIT_FAILURE);
	}
      if(j!=-1)
	for(k=0,i=j+1;i<(int)strlen(line)-fgets_correction;i+=2,k++)
	  {
	    value[k]=hex(line[i],line[i+1]);
	  }
    }
  *value_len=k;
  return(EXIT_SUCCESS);
}

int process_hexint(int *value,char *reference,char *line,int fgets_correction)
{
  int i,j,k;
  char dupline[MAXLINE];
  char dupreference[MAXLINE];
  for(i=0;i<(int)strlen(line);i++)
    dupline[i]=(char)toupper((int)line[i]);
  dupline[strlen(line)]='\0';
  for(i=0;i<(int)strlen(reference);i++)
    dupreference[i]=(char)toupper((int)reference[i]);
  dupreference[strlen(reference)]='\0';
  k=-1;
  *value=-1;
  if(strstr(dupline,dupreference)==dupline)
    {
      found=1;
      for(j=-1,i=0;i<(int)strlen(line)-fgets_correction;i++)
	if(line[i]=='=')
	  j=i;
      if(j!=-1)
	for((*value)=0,k=0,i=j+1;i<(int)strlen(line)-fgets_correction;i+=2,k++)
	  {
	    (*value)=((*value)<<8)^(hex(line[i],line[i+1]));
	  }
    }
  return(EXIT_SUCCESS);
}


int process_value(u8 *value,char *reference,char *line,int limit,int fgets_correction)
{
  int i,j;
  char dupline[MAXLINE];
  char dupreference[MAXLINE];
  for(i=0;i<(int)strlen(line);i++)
    dupline[i]=(char)toupper((int)line[i]);
  dupline[strlen(line)]='\0';
  for(i=0;i<(int)strlen(reference);i++)
    dupreference[i]=(char)toupper((int)reference[i]);
  dupreference[strlen(reference)]='\0';
  if(strstr(dupline,dupreference)==dupline)
    {
      found=1;
      for(j=-1,i=0;i<(int)strlen(line)-fgets_correction;i++)
	if(line[i]=='=')
	  j=i;
      if(j!=-1)
	for((*value)=0,i=j+1;i<(int)strlen(line)-fgets_correction;i++)
	  {
	    (*value)=((*value)*10)+(int)line[i]-(int)'0';
	    printf("<%c>",line[i]);
	  }
      if((*value)>=limit)
	{
	  printf("ERROR: %s shall be less than %d\n",reference,limit);
	  return(EXIT_FAILURE);
	}
    }
  return(EXIT_SUCCESS);
}

int process_intvalue(int *value,char *reference,char *line,int limit,int fgets_correction)
{
  int i,j;
  char dupline[MAXLINE];
  char dupreference[MAXLINE];
  for(i=0;i<(int)strlen(line);i++)
    dupline[i]=(char)toupper((int)line[i]);
  dupline[strlen(line)]='\0';
  for(i=0;i<(int)strlen(reference);i++)
    dupreference[i]=(char)toupper((int)reference[i]);
  dupreference[strlen(reference)]='\0';
  *value=-1;
  if(strstr(dupline,dupreference)==dupline)
    {
      found=1;
      for(j=-1,i=0;i<(int)strlen(line)-fgets_correction;i++)
	if(line[i]=='=')
	  j=i;
      if(j!=-1)
	for((*value)=0,i=j+1;i<(int)strlen(line)-fgets_correction;i++)
	  {
	    (*value)=((*value)*10)+(int)line[i]-(int)'0';
	  }
      if((*value)>=limit)
	{
	  printf("ERROR: %s shall be less than %d (%d submitted)\n",reference,limit,*value);
	  return(EXIT_FAILURE);
	}
    }
  return(EXIT_SUCCESS);
}

int process_arg(char *line,int fgets_correction)
{
  int i;
  int j;
  int resu;
  int tmp_value;
  int l_iFoundString=0;
  char string_pp[MAXLINE];
  found=0;
  memset(string_pp,0,MAXLINE);
  
  //  resu=process_intvalue(&(config_struct.flash_mb),"flash_size_mb",line,MAX_FLASH_MB);
  resu=process_intvalue(&j,"flash_size_mb",line,MAX_FLASH_MB,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR while extracting <flash_size_mb> field\n");
      return(EXIT_FAILURE);
    }
  else
    if(found==1)
      {
	config_struct.flash_mb=j;
      }
  
  resu=process_hexvalue(&i,config_struct.usn,"usn",line,fgets_correction);
  //simple filtering on acceptable values, 13 or 16
  //stricter filtering will be done later, because at this stage, session_mode may be unknown
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on usn retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=USN_LEN && i!=USN_FLORA_LEN && i!=USN_ANGELA_LEN && i!=-1)
	{
	  printf("ERROR while extracting <usn> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
      else
	{
	  if(i==USN_FLORA_LEN ||i==USN_ANGELA_LEN || i==USN_LEN)
	    {
	      config_struct.usn_len=i;
	    }
	}
    }
  resu=process_hexvalue(&i,aes_key,"aes_key",line,fgets_correction);	
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on aes_key retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <aes_key> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_hexvalue(&i,aes_data,"aes_data",line,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on aes_data retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <aes_data> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_hexvalue(&i,config_struct.fka,"fka",line,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on fka retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <fka> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_hexvalue(&i,config_struct.fkc,"fkc",line,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on fkc retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <fkc> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_hexvalue(&i,config_struct.fks,"fks",line,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on fks retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <fks> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_string(g_tcHSMRSALabelKey,"name_of_rsa_key",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <name_of_rsa_key> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(g_tcHSMECDSALabelKey,"name_of_ecdsa_key",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <name_of_ecdsa_key> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(g_tcQuorum_K,"quorum_k",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <quorum_k> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(g_tcQuorum_N,"quorum_n",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <quorum_n> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(ecdsafile,"ecdsa_file",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR on ecdsa_file retrieval\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(rsafile,"rsa_file",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR on rsa_file retrieval\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
	
	/*
	resu=process_hexvalue(&i,config_struct.rsa,"rsamod",line,fgets_correction);
	1if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on rsa retrieval\n");
      return(EXIT_FAILURE);
    }
	  else
		if(i!=-1)
		  {
		config_struct.rsa_len=i;
		  }
	  resu=process_hexvalue(&i,config_struct.rsa_pubexp,"public_exponent",line,fgets_correction);
	  if(EXIT_SUCCESS!=resu)
		{
		  printf("ERROR on rsa pub exponent retrieval\n");
		  return(EXIT_FAILURE);
		}
	  else
		if(i!=-1)
		  config_struct.rsa_explen=i;
	  resu=process_hexvalue(&i,config_struct.rsa_privexp,"private_exponent",line,fgets_correction);
	  if(EXIT_SUCCESS!=resu)
		{
		  printf("ERROR on rsa priv exponent retrieval\n");
		  return(EXIT_FAILURE);
		}
	  else
		if(i!=-1)
		  {
		config_struct.rsa_privexplen=i;
		}
	*/
  resu=process_hexint(&tmp_value,"addr_offset",line,fgets_correction);
  if(resu!=EXIT_SUCCESS)
    {
      printf("ERROR while extracting <addr_offset> field\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(tmp_value!=-1)
	address_offset=tmp_value;
    }
  
  resu=process_hexint(&tmp_value,"transaction_id",line,fgets_correction);
  if(resu!=EXIT_SUCCESS)
    {
      printf("ERROR while extracting <addr_offset> field\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(tmp_value!=-1)
	trid=tmp_value;
    }
  
  // Add of chunk_size arguments
  resu = process_intvalue(&tmp_value,"chunk_size",line,MAX_CHUNK_SIZE,fgets_correction);
  if ( EXIT_SUCCESS != resu )
    {
      printf("ERROR while extracting <chunk_size> field\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(tmp_value!=-1)
	chunk_size=tmp_value;
    }
  
  resu=process_hexvalue(&i,random_number,"random_number",line,fgets_correction);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR on rsa pub exponent retrieval\n");
      return(EXIT_FAILURE);
    }
  else
    {
      if(i!=16 && i!=-1)
	{
	  printf("ERROR while extracting <random_number> field: bad length (%d bytes)\n",i);
	  return(EXIT_FAILURE);
	}
    }
  resu=process_string(output_file,"output_file",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <output_file> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  resu=process_string(script_file,"script_file",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <script_file> field\n");
	  return(EXIT_FAILURE);
	}
      found=1;
    }
  
  resu=process_string(string_pp,"pp",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <pp> field\n");
	  return(EXIT_FAILURE);
	}
      
      for(i=0;i<(int)strlen(string_pp);i++)
	string_pp[i]=(char)toupper((int)string_pp[i]);
      if(strstr(string_pp,"E_CMAC")!=NULL)
	{
	  config_struct.pp=SCP_PP_E_CMAC;
	}
      else
	{
	  if(strstr(string_pp,"CMAC")!=NULL)
	    {
	      config_struct.pp=SCP_PP_CMAC;
	    }
	  else
	    {
	      if(strstr(string_pp,"E_RMAC")!=NULL)
		{
		  config_struct.pp=SCP_PP_E_RMAC;
		}
	      else
		{
		  if(strstr(string_pp,"RMAC")!=NULL)
		    {
		      config_struct.pp=SCP_PP_RMAC;
		    }
		  else
		    {
		      if(strstr(string_pp,"RSA")!=NULL)
			{
			  config_struct.pp=SCP_PP_RSA;
			}
		      else
			{
			  if(strstr(string_pp,"ECDSA")!=NULL)
			    {
			      config_struct.pp=SCP_PP_ECDSA;
			    }
			  else
			    {
			      config_struct.pp=SCP_PP_CLEAR;
			    }
			  
			}
		    }
		}
	    }
	}
      found=1;
    }
  resu=process_string(session_string,"session_mode",line,fgets_correction,&l_iFoundString);
  if(l_iFoundString)
    {
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR while extracting <session_mode> field\n");
	  return(EXIT_FAILURE);
	}
      if(strstr(session_string,"SCP_ON_AES")!=NULL)
	{
	  session_mode=SCP_ON_AES;
	}
      if(strstr(session_string,"SBL")!=NULL)
	{
	  session_mode=SBL;
	}
      if(strstr(session_string,"SCP_OFF_AES")!=NULL)
	{
	  session_mode=SCP_OFF_AES;
	}
      if(strstr(session_string,"SCP_FLORA_AES")!=NULL)
	{
	  session_mode=SCP_FLORA_AES;
	}
      if(strstr(session_string,"SCP_RSA")!=NULL)
	{
	  session_mode=SCP_RSA;
	}
      if(strstr(session_string,"SCP_FLORA_RSA")!=NULL)
	{
	  session_mode=SCP_FLORA_RSA;
	}
      if(strstr(session_string,"SCP_ANGELA_ECDSA")!=NULL)
	{
	  session_mode=SCP_ANGELA_ECDSA;
	}
      if(strstr(session_string,"MSP_MAXQ1852_ECDSA")!=NULL)
	{
	  session_mode=MSP_MAXQ1852_ECDSA;
	}
      found=1;
    }
  if(strstr(line,"verbose")!=NULL)
    {
      verbose=(strstr(line,"yes")!=NULL)?TRUE:FALSE;
      found=1;
    }
  if(!found)
    {
      printf("ERROR: line with unknown field: <%s>\n",line);
      return(EXIT_FAILURE);
    }
  return(EXIT_SUCCESS);
}

static int load_args(int argc, char **argv)
{
  int k;
  int resu;
  
  for(k=1;k<argc;k++)
    {
      resu=process_arg(argv[k],0);
      if(EXIT_SUCCESS!=resu)
	return(EXIT_FAILURE);
    }
  
  if(MSP_MAXQ1852_ECDSA==session_mode||SCP_ANGELA_ECDSA==session_mode)
    {
      config_struct.ecdsa_len=ECDSA_MODULUS_LEN;
      
#ifndef _MXIM_HSM
      resu=read_file_ecdsa(config_struct.ecdsa_pubkey_x,config_struct.ecdsa_pubkey_y,config_struct.ecdsa_privkey,config_struct.ecdsa_len,ecdsafile);
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR in read_file_ecdsa\n");
	  return(EXIT_FAILURE);
	}
#endif
      if(config_struct.pp != SCP_PP_ECDSA)
	{
	  printf("WARNING\n");
	  printf("SCP session mode is defined with this value: \"MSP_MAXQ1852_ECDSA\".\n");
	  printf("But the protection profile (\"pp\" value) is different from \"ECDSA\".\n");
	}
    }

  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
#ifndef _MXIM_HSM
      //-- DR MODIF code should be identical as ca_sign and crk_sign
      //resu=read_file_rsa(	config_struct.rsa,
      //					config_struct.rsa_len,
      //					config_struct.rsa_pubexp,
      //					config_struct.rsa_explen,
      //					config_struct.rsa_privexp,
      //					config_struct.rsa_privexplen,
      //					rsafile);
      
      //-- Init config_struct RSA parameters
      config_struct.rsa_privexplen	=	RSA_MODULUS_LEN;
      config_struct.rsa_explen		=	RSA_PUBLIC_EXPONENT_LEN;
      config_struct.rsa_len			=	SIGNATURE_LEN;
      resu=read_file_rsa(config_struct.rsa, config_struct.rsa_len, config_struct.rsa_pubexp, config_struct.rsa_privexp, config_struct.rsa_explen, rsafile);
      if(EXIT_SUCCESS!=resu)
	{
	  printf("ERROR in read_file_rsa\n");
	  return(EXIT_FAILURE);
	}
      
      if(config_struct.pp != SCP_PP_RSA)
	{
	  printf(" WARNING\n");
	  printf("SCP session mode is defined with one of this value: \"SCP_RSA\" or \"SCP_FLORA_RSA\".\n");
	  printf("But the protection profile (\"pp\" value) is different from \"RSA\".\n");
	}
      if(config_struct.rsa_len!=config_struct.rsa_privexplen)
	{
	  printf("ERROR: lengths of RSA modulus and RSA private exponent do not match: %d bytes vs %d bytes\n",	config_struct.rsa_len,
		 config_struct.rsa_privexplen);
	  return(EXIT_FAILURE);
	}
#endif//MXIM_HSM
    }

  if(SCP_ON_AES==session_mode||SCP_FLORA_AES==session_mode)
    {
      if(config_struct.pp != SCP_PP_E_CMAC)
	{
	  printf(" WARNING\n");
	  printf("SCP session mode is defined with one of this value: \"SCP_ON_AES\" or \"SCP_FLORA_AES\".\n");
	  printf("But the protection profile (\"pp\" value) is different from \"E_CMAC\".\n");
	}
    }
  if(((SCP_FLORA_RSA==session_mode || SCP_FLORA_AES==session_mode)&&(config_struct.usn_len!=USN_FLORA_LEN))||
     ((SCP_RSA==session_mode || SCP_ON_AES==session_mode || SCP_OFF_AES==session_mode)&&(config_struct.usn_len!=USN_LEN)))
    {
      printf("ERROR: USN with bad length: %d\n",config_struct.usn_len);
      return(EXIT_FAILURE);
    }
  return(EXIT_SUCCESS);
}

int load_default_config(void)
{
  int i;
  u8 usn_default[]={0x04,0x00,0x43,0x47,0x1f,0xd2,0x03,0x08,0x0c,0x07,0x00,0x00,0x7f,0x24,0xea,0x2f};
  verbose=TRUE;
  session_mode=SCP_RSA;
  // default config
  config_struct.cpu=IC400ABC;
  config_struct.life_cycle=P6;
  config_struct.already_diversified=NOT;
  //config_struct.pp=SCP_PP_CMAC;
  config_struct.pp=SCP_PP_RSA;
  //flash size is 32MB
  config_struct.flash_mb=32;
  address_offset=0;
  chunk_size=1024;
  for(i=0;i<16;i++)
    random_number[i]=rand()&255;
  for(i=0;i<16;i++)
    blpk[i]=i+1;
  for(i=0;i<16;i++)
    fak[i]=0x21;
  for(i=0;i<16;i++)
    aes_key[i]=0x41;
  for(i=0;i<16;i++)
    aes_data[i]=0x51;
  for(i=0;i<USN_LEN;i++)
    config_struct.usn[i]=usn_default[i];
  for(i=0;i<UCL_AES_BLOCKSIZE;i++)
    {
      config_struct.mka[i]=0x31;
      config_struct.mkc[i]=0x32;
      config_struct.mks[i]=0x33;
      config_struct.tka[i]=0x41;
      config_struct.tkc[i]=0x42;
      config_struct.tks[i]=0x43;
      config_struct.pka[i]=0x51;
      config_struct.pkc[i]=0x52;
      config_struct.pks[i]=0x53;
      config_struct.fka[i]=0x61;
      config_struct.fkc[i]=0x62;
      config_struct.fks[i]=0x63;
      config_struct.sblpk[i]=0x91;
    }
  //  printf("<load default config>\n");
  sprintf(script_file,"script.txt");
  sprintf(output_file,"session.txt");
  return(EXIT_SUCCESS);
}

 int load_ini_config(FILE *fp)
 {
  char line[MAXLINE];
  int resu;
  //    printf("<load .ini config>\n");
  while(fgets(line,MAXLINE,fp)!=NULL)
    {
      if(line[strlen(line)]!='\0')
	{
	  printf("ERROR: overflow on line <%s>\n",line);
	  return(EXIT_FAILURE);
	}
      if('#'==line[0])
	continue;
      resu=process_arg(line,1);
      if(resu!=EXIT_SUCCESS)
	return(EXIT_FAILURE);
    }
  return(EXIT_SUCCESS);
}

//this function reads the .ini and configures the parameters
static int load_config(void)
{
  FILE *fp;
  int resu;
  load_default_config();
  //read the configuration file
  fp=fopen(INIFILE,"r");
  //if file not present
  if(fp==NULL)
    {
      //setup with the default configuration
      printf("WARNING: <%s> not found\n",INIFILE);
    }
  else
    {
      resu=load_ini_config(fp);
      if(resu!=EXIT_SUCCESS)
	return(EXIT_FAILURE);
      (void)fclose(fp);
    }
  return(EXIT_SUCCESS);
}

void display_config(int std_display)
{
  int i=0;
  if(TRUE==std_display)
    printf("<display config>\n");
  
  if(SBL==session_mode)
    {
      printf("mode: SBL\n");
      
      if(SCP_PP_CMAC==config_struct.pp)
	printf("pp: CMAC\n");
      
      if(SCP_PP_E_CMAC==config_struct.pp)
	printf("pp: E-CMAC\n");
      
      if(SCP_PP_RMAC==config_struct.pp)
	printf("pp: RMAC\n");
      
      if(SCP_PP_E_RMAC==config_struct.pp)
	printf("pp: E-RMAC\n");
      
      if(SCP_PP_CLEAR==config_struct.pp)
	printf("pp: PLAIN\n");
    }
  else
    {
      if(SCP_ON_AES==session_mode)
	{
	  printf("mode: SCP online AES\n");
	  
	  if(SCP_PP_CMAC==config_struct.pp)
	    printf("pp: CMAC\n");
	  
	  if(SCP_PP_E_CMAC==config_struct.pp)
	    printf("pp: E-CMAC\n");
	}
      else
	{
	  if(SCP_OFF_AES==session_mode)
	    {
	      printf("mode: SCP offline AES\n");
	    }
	  else
	    {
	      if(SCP_RSA==session_mode)
		{
		  printf("mode: SCP RSA\n");
		}
	      else
		{
		  if(SCP_FLORA_RSA==session_mode)
		    {
		      printf("mode: SCP FLORA RSA\n");
		    }
		  else
		    {
		      if(SCP_FLORA_AES==session_mode)
			{
			  printf("mode: SCP FLORA AES\n");
			  if(SCP_PP_CMAC==config_struct.pp)
			    printf("pp: CMAC\n");
			  if(SCP_PP_E_CMAC==config_struct.pp)
			    printf("pp: E-CMAC\n");
			}
		      else
			{
			  if(MSP_MAXQ1852_ECDSA==session_mode)
			    {
			      printf("mode: SCP MAXQ1852 ECDSA\n");
			    }
			  else
			    if(SCP_ANGELA_ECDSA==session_mode)
			      {
				printf("mode: SCP ANGELA ECDSA\n");
				printf("PP=%d\n",config_struct.pp);
			      }
			}
		    }
		}
	    }
	}
    }
  if(TRUE==verbose)
    {
      printf("verbose\n");
    }
  else
    {
      printf("mute\n");
    }
  printf("PP=%d -> ",config_struct.pp);
  switch(config_struct.pp)
    {
    case SCP_PP_CLEAR:
      printf("CLEAR\n");
      break;
    case SCP_PP_RMAC:
      printf("RMAC\n");
      break;
    case SCP_PP_E_RMAC:
      printf("E-RMAC\n");
      break;
    case SCP_PP_CMAC:
      printf("CMAC\n");
      break;
    case SCP_PP_E_CMAC:
      printf("E-CMAC\n");
      break;
    case SCP_PP_RSA:
      printf("RSA\n");
      break;
    case SCP_PP_ECDSA:
      printf("ECDSA\n");
      break;
    case SCP_PP_UNK:
      printf("unknown\n");
      break;
    default:
      printf("ERROR\n");
      break;
    }
  printf("output file: %s\n",output_file);
  
  //data used by PCI LINUX SCP only
  if(SCP_ON_AES==session_mode||SCP_OFF_AES==session_mode||SCP_RSA==session_mode)
    {
      printf("blpk:");
      for(i=0;i<16;i++)
	printf("%02x",blpk[i]);
      printf("\n");
      printf("fak:");
      for(i=0;i<16;i++)
	printf("%02x",fak[i]);
      printf("\n");
      printf("aes_key:");
      for(i=0;i<16;i++)
	printf("%02x",aes_key[i]);
      printf("\n");
      printf("aes_data:");
      for(i=0;i<16;i++)
	printf("%02x",aes_data[i]);
      printf("\n");
    }
  if(SCP_ON_AES==session_mode)
    {
      printf("random number:");
      for(i=0;i<16;i++)
	printf("%02x",random_number[i]);
      printf("\n");
    }
  if(SCP_RSA==session_mode||SCP_FLORA_RSA==session_mode)
    {
#ifndef _MXIM_HSM
      printf("rsa modulus:");
      for(i=0;i<config_struct.rsa_len;i++)
	printf("%02x",config_struct.rsa[i]);
      printf("\n");
      printf("rsa public exponent:");
      for(i=0;i<config_struct.rsa_explen;i++)
	printf("%02x",config_struct.rsa_pubexp[i]);
      printf("\n");
      printf("rsa private exponent:");
      for(i=0;i<config_struct.rsa_len;i++)
	printf("%02x",config_struct.rsa_privexp[i]);
      printf("\n");
#else
      if(strlen(g_tcHSMRSALabelKey) != 0)
	{
	  printf("rsa key: %s\n",g_tcHSMRSALabelKey);
	}

#endif//MXIM_HSM
    }
  if(MSP_MAXQ1852_ECDSA==session_mode)
    {
#ifndef _MXIM_HSM
      printf("transaction ID: %08x\n",trid);
      printf("ecdsa privkey:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_privkey[i]);
      printf("\n");
      printf("ecdsa public x:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_pubkey_x[i]);
      printf("\n");
      printf("ecdsa public y:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_pubkey_y[i]);
      printf("\n");
#else
	if(strlen(g_tcHSMECDSALabelKey) != 0)
	{
	  printf("ecdsa key: %s\n",g_tcHSMECDSALabelKey);
	}
#endif//MXIM_HSM
    }
  if(SCP_ANGELA_ECDSA==session_mode)
    {
#ifndef _MXIM_HSM
      printf("transaction ID: %08x\n",trid);
      printf("ecdsa privkey:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_privkey[i]);
      printf("\n");
      printf("ecdsa public x:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_pubkey_x[i]);
      printf("\n");
      printf("ecdsa public y:");
      for(i=0;i<config_struct.ecdsa_len;i++)
	printf("%02x",config_struct.ecdsa_pubkey_y[i]);
      printf("\n");
#else
	if(strlen(g_tcHSMECDSALabelKey) != 0)
	{
	  printf("ecdsa key: %s\n",g_tcHSMECDSALabelKey);
	}
#endif//MXIM_HSM
    }
  printf("flash maximal size: %dMBytes\n",config_struct.flash_mb);
  printf("script file:<%s>\n",script_file);
  printf("chunk size: %d\n",chunk_size);
  printf("addr.offset: %08x\n",address_offset);
}

int process(void)
{
  int resu;
  resu=process_script();
  return(resu);
}

int main(int argc,char **argv)
{
  int resu;
  #ifdef _MXIM_HSM
  
  ULONG l_ulQuorumKValue=0; /*= atol(g_tcQuorum_K);*/
  ULONG l_ulQuorumNValue=0; /*= atol(g_tcQuorum_N);*/
  bool l_bPKCS11Login = false;
  unsigned long l_ulAttributeKeyType = CKA_LABEL;
  unsigned long l_ulHSMLabelKeyLength = 0;/*strlen(g_tcHSMLabelKey);*/
  memset(g_tcHSMRSALabelKey,0,_MXIM_MAX_STRING);
  memset(g_tcHSMECDSALabelKey,0,_MXIM_MAX_STRING);
  memset(g_tcQuorum_K,0,_MXIM_MAX_STRING);
  memset(g_tcQuorum_N,0,_MXIM_MAX_STRING);
  printf(	"SBL/SCP packets builder v%d.%d.%d (build %d) (c)Maxim Integrated 2006-2014\n",MAJV,MINV,ZVER,BUILD);
  printf("\n--warning: this tool handles keys in PCI PTS compliant way --\n");
#else
  printf(	"SBL/SCP packets builder v%d.%d.%d (build %d) (c)Maxim Integrated 2006-2014\n",MAJV,MINV,ZVER,BUILD);	
  printf("--warning: this tool does not handle keys in a PCI PTS compliant way --\n");
#endif
  resu=load_config();
  if(resu!=EXIT_SUCCESS)
    return(EXIT_FAILURE);
  resu=load_args(argc,argv);
  if(resu!=EXIT_SUCCESS)
    return(EXIT_FAILURE);
  init();
  if(TRUE==verbose)
    {
      display_config(FALSE);
    }
  sprintf(output_name,"%s.log",output_file);
  fp=fopen(output_name,"w");
  if(NULL==fp)
    {
      printf("ERROR: unable to create <%s>\n",output_file);
      return(EXIT_FAILURE);
    }
#ifndef _MXIM_HSM
fprintf(fp,"session generation v%d.%d.%d (build %d) (c)Maxim IC 2006-2011\n",MAJV,MINV,ZVER,BUILD);
#endif

#ifdef _MXIM_HSM
 fprintf(fp, "UCL Version: %s (%s)", (char *)g_objMXIMUCLLibrary.GetVersion(), (char *)g_objMXIMUCLLibrary.GetBuildDate());
 fprintf(fp,"HSM try open connection"); 
 
 l_ulQuorumKValue = atol(g_tcQuorum_K);
 l_ulQuorumNValue = atol(g_tcQuorum_N);
 
 
 if( (l_ulQuorumKValue != 0)&&(l_ulQuorumNValue != 0))
   {
     l_bPKCS11Login=true;
   }
 
 int l_iErr = MXIMHSMOpenConnection(&g_objMXHSMCLI,
				    verbose,
				    0x04,
				    &l_ulQuorumKValue,
				    &l_ulQuorumNValue);
 
 if(EXIT_SUCCESS!=l_iErr)
   {
     printf("ERROR: aborting\n");
     
     return(EXIT_FAILURE);
   }
 
#else
 fprintf(fp,"UCL Version: %s (%s)", (char *)ucl_get_version(),(char *)ucl_get_build_date());
#endif//MXIM_HSM
  resu=process();

  (void)fclose(fp);
  if(EXIT_SUCCESS!=resu)
    {
      printf("ERROR: aborting\n");
#ifdef _MXIM_HSM
      
      int l_iErr = MXIMHSMCloseConnection(&g_objMXHSMCLI);
      
      if(EXIT_SUCCESS!=l_iErr)
	{
	  printf("Warning: fails to close HSM connection\n");
	}
#endif//MXIM_HSM
      return(EXIT_FAILURE);
    }
  printf("<%s> created\n",output_name);
  
#ifdef _MXIM_HSM
  l_iErr = MXIMHSMCloseConnection(&g_objMXHSMCLI);
  
  if(EXIT_SUCCESS!=l_iErr)
    {
      printf("Warning: fails to close HSM connection\n");  
    }
#endif//MXIM_HSM

  return(EXIT_SUCCESS);
}
