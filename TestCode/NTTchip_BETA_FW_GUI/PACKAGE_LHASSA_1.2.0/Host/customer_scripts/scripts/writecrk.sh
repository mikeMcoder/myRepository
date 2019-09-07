#!/bin/sh

# Copyright (C) 2012-2014 Maxim Integrated Products, Inc., All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of Maxim Integrated 
# Products, Inc. shall not be used except as stated in the Maxim Integrated 
# Products, Inc. Branding Policy.
#
# The mere transfer of this software does not imply any licenses
# of trade secrets, proprietary technology, copyrights, patents,
# trademarks, maskwork rights, or any other form of intellectual
# property whatsoever. Maxim Integrated Products, Inc. retains all 
# ownership rights.

usage() {
    echo
    echo "Write the test CRK for MAX32555 SecureROM loader."
    echo "Copyright (c) MAXIM INTEGRATED 2012-2014"
    echo ""
    echo "**** CAUTION: This tool is not PCI compliant. It is for development purposes only. ****"
    echo ""
    echo " MAX32555 pre-requisites:"
    echo "   - For MAX32555 rev A1"
    echo "   - Chip must be in Phase 3"
    echo ""
    echo " Syntax: writecrk <serialport> <CRK packets directory>";
    echo
    echo "    <serialport> = serial port device (e.g. COM1, /dev/ttyS0)"
    echo ""
}

if [ -z $1 ]; then
	usage
	exit 1
fi

TOOLDIR=$(readlink -e $(dirname $0))
#PACKETDIR=$TOOLDIR/../../../SCP_Packets/prod_p3_write_crk
PACKETDIR=$2
if ! test -f "$PACKETDIR/packet.list"
then
    cd $PACKETDIR
    ls -1 *.packet >packet.list
    cd $TOOLDIR
fi
$TOOLDIR/sendscp.sh $1 $PACKETDIR 

