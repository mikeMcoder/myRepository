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
#ifndef _MXIM_SCP_DEFINITIONS_INCLUDE
#define _MXIM_SCP_DEFINITIONS_INCLUDE



//------------------------//
//-- SCP - frame format --//
//------------------------//

//-------------------//
//-- SCP - targets --//
//-------------------//
#define SBL 0
#define HOST 0

//for historical reason, the chip is named USIP
//should be changed, because we now support JIBE, LONDA, MAXQ1852, LIGHTHOUSE
//anyway, its purpose is mainly to say "not HOST" !
#define USIP 1

//----------------------------------------------------------------------------------------------//


//------------------//
//-- SCP - modes  --//
//------------------//

#define SCP_ON_AES		0x01
#define SCP_OFF_AES	0x02
#define SCP_RSA	0x03
#define SCP_FLORA_RSA	0x04
#define SCP_FLORA_AES	0x05
#define MSP_MAXQ1852_ECDSA 0x06
#define SCP_ANGELA_ECDSA	0x07

#define SCP_SESSION_MODE_UNK		0xFF

//----------------------------------------------------------------------------------------------//

//------------------------------//
//-- SCP - security profiles  --//
//------------------------------//

#define SCP_PP_CLEAR				0x00
#define SCP_PP_RMAC					0x01
#define SCP_PP_E_RMAC				0x02
#define SCP_PP_CMAC					0x05
#define SCP_PP_E_CMAC				0x06
#define SCP_PP_RSA					0x09
#define SCP_PP_ECDSA				0x0A
#define SCP_PP_UNK					0xFF

//----------------------------------------------------------------------------------------------//
 
	
#define MAX_FRAME 20000
#define MAX_IDF 400
#define MAX_STRING 20000


#define HEADER_LEN				8
#define CRC_LEN					4
#define COMMAND_LEN				4

#define DATA_CHECKSUM_LEN		4

//----------------------------------------------------------------------------------------------//

//-------------------------------------//
//-- SCP - physical layer parameters --//
//-------------------------------------//


//USIP-SBL and JIBE-SCP commands, synchros, ....
#define SYNCH1					0xBE
#define SYNCH2					0xEF
#define SYNCH3					0xED

//----------------------------------------------------------------------------------------------//


//--------------------------------------//
//-- SCP - transport layer parameters --//
//--------------------------------------//

#define HELLO_SCP_REQ_BLOCK_LEN 0x0E
#define HELLO_SCP_REQ_LEN		0x0A
#define HELLO_SCP_REQ_CONST_LEN 0x09
#define HELLO_SCP_REP_BLOCK_LEN 0x32
#define HELLO_SCP_REP_CONST_LEN 0x0A
#define HELLO_REQ_BLOCK_LEN		0x0C
#define HELLO_REP_BLOCK_LEN		0x32
#define HELLO_OFF_REQ_BLOCK_LEN 0x0C
#define HELLO_OFF_REP_BLOCK_LEN 0x22
#define CHALLENGE_BLOCK_LEN		0x14
#define SUCCESS_BLOCK_LEN		0x4
#define FAILURE_BLOCK_LEN		0x4
	
#define HELLO_REQ_LEN			0x08
#define HELLO_REQ_CONST_LEN		0x08
#define HELLO_REP_LEN			0x2E
#define HELLO_REP_CONST_LEN		0x07
#define HELLO_REP_LC			0x0B
#define HELLO_REP_UMV			0x0C
#define HELLO_REP_UmV			0x0D
#define HELLO_REP_SMV			0x0E
#define HELLO_REP_SmV			0x0F
#define HELLO_REP_HMV			0x10
#define HELLO_REP_HmV			0x11
#define HELLO_OFF_REQ_LEN       0x08
#define HELLO_OFF_REQ_CONST_LEN 0x08
#define HELLO_OFF_REP_LEN		0x1E
#define HELLO_OFF_REP_CONST_LEN 0x07
#define HELLO_OFF_REP_LC		0x0B
#define HELLO_OFF_REP_UMV		0x0C
#define HELLO_OFF_REP_UmV		0x0D
#define HELLO_OFF_REP_SMV		0x0E
#define HELLO_OFF_REP_SmV		0x0F
#define HELLO_OFF_REP_HMV		0x10
#define HELLO_OFF_REP_HmV		0x11
#define CHALLENGE_VALUE			4
#define CHALLENGE_LEN			0x10
#define HELLO_REP_RANDOM		0x22
#define HELLO_REP_USN			0x12
#define HELLO_OFF_REP_USN		0x12


#define HELLO_REQ				0x1
#define HELLO_REP				0x2
#define HELLO_OFF_REQ			0x8
#define HELLO_OFF_REP			0x9
#define CHALLENGE				0x7
#define SUCCESS					0x3
#define FAILURE					0x4
#define DATA					0x5

	
#define CON_REQ 				0x01	//Connection request
#define CON_REP					0x02	//Connection reply
#define CON_REF 				0x09	//Connection refused
#define DISC_REQ 				0x03	//Disconnection request
#define DISC_REP				0x04	//Disconnection reply
#define DATA_TRANSFER			0x05	//Data Exchange
#define ACK						0x06	//Acknowledge
#define ECHO_REQ				0x0B	//Echo request
#define ECHO_REP				0x0C	//Echo reply

#define USER_FLASH_CHECK		0x02
#define RESERVED_SECTOR_CHECK	0x03


//SCP-MAXQ1852 commands, synchro, ...
#define MAXQ1852_SCDESIGNATOR 0x80
#define MAXQ1852_SCPROMPT '>'
#define MAXQ1852_SCOFFSET 0x00
#define MAXQ1852_SC_LEN_BYTE1 1
#define MAXQ1852_SC_LEN_BYTE2 2

//----------------------------------------------------------------------------------------------//

//----------------------------------------//
//-- SCP - application layer parameters --//
//----------------------------------------//

#define ADMIN	0x02
#define USER	0x01

//----------------------------------------------------------------------------------------------//
	
//--------------------------------------//
//-- SCP - application layer commands --//
//--------------------------------------//


// bootloader commands
#define READ_CONFIGURATION		0x4203
	
//confused with FLORA ERASE-DATA
#define ERASE_MEM				0x4401
	
//confused with FLORA WRITE-DATA
#define WRITE_MEM				0x2402
	
//confused with FLORA COMPARE-DATA
#define VERIFY_MEM				0x2403
	
#define WRITE_BLPK				0x4702
#define WRITE_FAK				0x2703
#define AES_COMP				0x2701
#define MEM_MAPPING				0x2404
#define WRITE_CONFIGURATION		0x4202
// FLORA commands
#define WRITE_CRK				0x470A
#define REWRITE_CRK				0x461A
#define WRITE_OTP				0x4714
#define WRITE_BPK				0x4703
#define WRITE_TIMEOUT			0x4426
#define KILL_CHIP				0x4538
#define EXECUTE_CODE			0x2101
	


	
#define COMMAND_WRITE_FILE				0
#define COMMAND_VERIFY_FILE				1
#define COMMAND_WRITE_BLPK				2
#define COMMAND_WRITE_FAK				3
#define COMMAND_READ_CONFIGURATION		4
#define COMMAND_READ_MEMORY_MAPPING		5
#define COMMAND_WRITE_CRK				6
#define COMMAND_WRITE_BPK				7
#define COMMAND_WRITE_OTP				8
#define COMMAND_WRITE_TIMEOUT			9
#define COMMAND_KILL_CHIP				10
#define COMMAND_WRITE_CONFIGURATION		11
#define COMMAND_EXECUTE_CODE			12
#define COMMAND_UNKNOWN					13
#define COMMAND_WRITE_ONLY				14
#define COMMAND_ERASE_DATA				15
#define COMMAND_HELP					16
	
#define COMMAND_MAXQ1852_LOAD_CUSTOMER_KEY						17
#define COMMAND_MAXQ1852_ERASE_CODE_FLASH_AREA					18
#define COMMAND_MAXQ1852_ERASE_ALL_FLASH_AREAS					19
#define COMMAND_MAXQ1852_LOAD_CODE								20
#define COMMAND_MAXQ1852_LOAD_DATA								21
#define COMMAND_MAXQ1852_VERIFY_CODE							22
#define COMMAND_MAXQ1852_VERIFY_DATA							23
#define COMMAND_MAXQ1852_WRITE_REGISTER							24
#define COMMAND_MAXQ1852_READ_REGISTER							25
#define COMMAND_MAXQ1852_ENGAGE_PLLO							26
#define COMMAND_MAXQ1852_VERIFY_CUSTOMER_KEY					27
#define COMMAND_MAXQ1852_ACTIVATE_CUSTOMER_KEY					28
#define COMMAND_MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE 29
#define COMMAND_MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE	30
#define COMMAND_MAXQ1852_LOAD_FILE								31
#define COMMAND_MAXQ1852_VERIFY_FILE								32
#define COMMAND_REWRITE_CRK				                                        33
#define MAX_SCP_COMMAND										34
	
#define MAXQ1852_LOAD_CUSTOMER_KEY								0x01
#define MAXQ1852_VERIFY_CUSTOMER_KEY						                0x02
#define MAXQ1852_ACTIVATE_CUSTOMER_KEY							        0x03
#define MAXQ1852_ERASE_CODE_FLASH_AREA							        0x10
#define MAXQ1852_ERASE_ALL_FLASH_AREAS							        0x11
#define MAXQ1852_LOAD_CODE									0x20
#define MAXQ1852_LOAD_DATA									0x21
#define MAXQ1852_VERIFY_CODE									0x30
#define MAXQ1852_VERIFY_DATA									0x31
#define MAXQ1852_WRITE_REGISTER									0x40
#define MAXQ1852_READ_REGISTER									0x41
#define MAXQ1852_ENGAGE_PLLO									0x50
#define MAXQ1852_GENERATE_APPLICATION_STARTUP_SIGNATURE			                        0x60
#define MAXQ1852_VERIFY_APPLICATION_STARTUP_SIGNATURE			                        0x61


	

//----------------------------------------------------------------------------------------------//
 

//-------------------------------------//
//-- ASCII files - format parameters --//
//-------------------------------------//

#define S19_ADDRESS_LEN		4
#define S19_ADDRESS_START	4
#define S19_DATA_START		(S19_ADDRESS_START+S19_ADDRESS_LEN*2)
#define S19_CRC_LEN			1
#define S19_WDATA_CHAR1		'S'
#define S19_WDATA_CHAR2		'3'
#define S19_LINE_LEN_POS1	2
#define S19_LINE_LEN_POS2	3
	
#define S20_ADDRESS_LEN		4
#define S20_ADDRESS_START	6
#define S20_DATA_START		(S20_ADDRESS_START+S20_ADDRESS_LEN*2)
#define S20_CRC_LEN 1
#define S20_WDATA_CHAR1		'S'
#define S20_WDATA_CHAR2		'3'
#define S20_LINE_LEN_POS1	2
#define S20_LINE_LEN_POS2	3
#define S20_LINE_LEN_POS3	4
#define S20_LINE_LEN_POS4	5
	
#define HEX_START_CHAR			':'
#define HEX_RECORD_TYPE_POS1	 7
#define HEX_RECORD_TYPE_POS2	8
#define HEX_LINE_LEN_POS1		1
#define HEX_LINE_LEN_POS2		2
#define HEX_ADDRESS_START		3
#define HEX_ADDRESS_END			6
#define HEX_DATA_START			9

//----------------------------------------------------------------------------------------------//



#endif
