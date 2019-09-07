#!/bin/bash

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
    echo "Configures the SecureROM Package for the current host computer."
    echo
    echo "Copyright (c)2012-2014 Maxim Integrated Products, Inc."
    echo
    echo "Usage: ./setup.sh [--soc=<rev>]"
    echo
    echo "   --soc=<rev> specify the MAX32555 revision.  Default is A1."
    echo
    echo "NOTE: Launch this script from the root directory of the SecureROM package."
    echo
}

if [ $# -gt 1 ]; then
    usage >&2
    exit 2
fi

if [ ! -d ./Host/customer_scripts/ ]; then
    echo >&2 "You must run this script while you are in the root directory of the SecureROM package."
    echo >&2 "Please execute: 'cd <path of the directory where you unzipped the package>' beforehand."
    echo >&2
    exit 3
fi

homedir=$(pwd)
soc='A1'

while [ $# -ge 1 ]; do
	case $1 in
	--help)	usage
		exit 0
		;;
	--soc=)	echo >&2 "error: No ROM/chip version specified"
		exit 4
		;;
	--soc=*)
		soc=${1#--soc=}
		;;
	--)	shift
		break
		;;
	-*)	echo >&2 "error: Unknown option \`$1'"
		exit 5
		;;
	*)	break
		;;
	esac
	shift
done

export LHASSA_SCRIPTS_PATH=$homedir

# No need to issue an error of our own if this fails since `findrom.sh'
# (or, in rare cases, the shell itself) has already complained ....
#
romdir=$( Host/customer_scripts/lib/rom/findrom.sh "$soc" )  ||  exit 10
readonly romdir

#identifying the OS, as cygwin uses a serial_sender.exe while linux directly uses the python application
system=$(uname -s)
case $system in
*CYGWIN*) os="cygwin"
	;;
*Linux*)  os="linux"
	;;
*)	echo >&2 "Unknown system \`$system'!"
	exit 20
	;;
esac

echo "    Setting up MAX32555 (default rev. $soc) SecureROM Package... for $os"
echo

# Only a warning, the intall itself does not need `objcopy' ...
which objcopy  >/dev/null  || {
	echo "\
warning: \`objcopy' utility not available.
    You should install the \"binutils\" package."
}


DESTFILE=~/.profile
if test "$os" = "cygwin"; then DESTFILE=~/.bash_profile; fi

cp -p Host/session_build/bin/$os/session_build* Host/customer_scripts/lib

echo "${romdir##*/}" >Host/customer_scripts/lib/romversion

# add the LHASSA_SCRIPTS_PATH variable into the .profile
# in order to be set at host startup
echo "\
# The following line has been added by LHASSA PACKAGE's setup.sh script.
export LHASSA_SCRIPTS_PATH=$homedir"  >>$DESTFILE

echo "\
Info: New environment variable LHASSA_SCRIPTS_PATH added by
      LHASSA PACKAGE's setup.sh script into $DESTFILE."
echo "
>>> You need to logout then login again to make this variable available.
>>> You can also do \"source $DESTFILE\" to make this variable available
    (in this terminal session only)."
echo
exit 0






