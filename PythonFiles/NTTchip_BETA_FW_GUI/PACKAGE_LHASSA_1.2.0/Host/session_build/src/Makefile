# ----------------------------------------------------------------------------
# Copyright (c) 2009-2010, Maxim Integrated Products
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY MAXIM INTEGRATED PRODUCTS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL MAXIM INTEGRATED PRODUCTS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
#
# Created on: Feb, 2010
# Author:
#
# ---- Subversion keywords (need to set the keyword property)
# $Rev::               $:  Revision of last commit
# $Author::            $:  Author of last commit
# $Date::              $:  Date of last commit
#

#makefile for cygwin target
#possible targets: linux, cygwin
ifndef TARGET
TARGET=linux
endif

CC=	gcc

#CFLAGS=	-O2 -W -Wall -DWORD32
IFLAGS= -I../include
DIST=../bin/$(TARGET)
HOST_LIB=../../customer_scripts/lib
USR_LOCAL_LIB=/usr/local/lib

ifeq ($(TARGET),cygwin)
 LFLAGS= -L ./
 LIBFLAGS:= libucl.dll
 EXTENSION:=.exe
 UCL:= libucl.dll
 CFLAGS=	-O2 -W -Wall -DWORD32

else
 LFLAGS= -L ./ -Wl,-rpath=\$$ORIGIN
 LIBFLAGS:= -lucl
 EXTENSION:=.exe
 UCL:=libucl.so.2.4.1
 CFLAGS=	-O2 -W -Wall -DWORD32 -m32
endif

EXEC=	session_build$(EXTENSION)
OBJ=	session_build.o

#
# Rules
#

.PHONY:all
all:	$(EXEC)

.PHONY:doc
doc:
	$(warning no doc generated)

.PHONY:	clean
clean:
	rm -f -- $(OBJ) $(DIST)/$(EXEC)

.PHONY:	distclean
distclean:
	rm -f -- $(OBJ) $(DIST)/$(EXEC)

.PHONY:	uninstall
uninstall: clean

.PHONY: install
install: ;

#
# Dependencies
#

%.o:	%.c
	$(CC) $(CFLAGS) $(IFLAGS) -c -o $@ $<

session_build$(EXTENSION):	$(OBJ)
	$(CC) $(CFLAGS) $(IFLAGS)  $(LFLAGS) -o $(DIST)/$(EXEC) $(OBJ) $(LIBFLAGS)
	cp $(UCL) $(DIST)/
#move executable to directory where it is called from by scripts
	cp $(DIST)/$(EXEC) $(HOST_LIB)/
	cp $(DIST)/$(UCL) $(HOST_LIB)/
# End Of Makefile
