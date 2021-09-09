# Copyright (c) 1991-2013 Kawahara Lab., Kyoto University
# Copyright (c) 2000-2005 Shikano Lab., Nara Institute of Science and Technology
# Copyright (c) 2005-2013 Julius project team, Nagoya Institute of Technology
# All rights reserved

## Makefile for mkfa, DFA compiler
## *** Needs GNU bison and flex ***
SHELL=/bin/sh
.SUFFIXES:
.SUFFIXES: .c .o
.c.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ -c $<

CC=gcc
CFLAGS=-g -O2
CPPFLAGS= -DPACKAGE_NAME=\"\" -DPACKAGE_TARNAME=\"\" -DPACKAGE_VERSION=\"\" -DPACKAGE_STRING=\"\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DHAVE_LIBREADLINE=1 -DSTDC_HEADERS=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_SYS_STAT_H=1 -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 -DHAVE_MEMORY_H=1 -DHAVE_STRINGS_H=1 -DHAVE_INTTYPES_H=1 -DHAVE_STDINT_H=1 -DHAVE_UNISTD_H=1 -DHAVE_READLINE_READLINE_H=1 -DHAVE_LIBREADLINE_HISTORY=1 -DHAVE_READLINE_HISTORY_H=1
LDFLAGS= 
RM=/bin/rm -f
#BISON=@BISON@
#FLEX=@FLEX@
prefix=/usr/local
exec_prefix=${prefix}
INSTALL=/usr/bin/install -c

######################################################################
#YACS = gram.y
#FLEXS = gram.l
OBJS = gram.tab.o main.o voca.o nfa.o dfa.o triplet.o

TARGET=mkfa

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $(TARGET) $(OBJS) $(LDFLAGS)

#gram.tab.c: $(YACS)
#	$(BISON) $(YACS)
#
#lex.yy.c: $(FLEXS)
#	$(FLEX) $(FLEXS)

install: install.bin

install.bin:
	${INSTALL} -d ${exec_prefix}/bin
	${INSTALL} $(TARGET) ${exec_prefix}/bin

clean:
	$(RM) *.o *~ core
	$(RM) $(TARGET) $(TARGET).exe

distclean:
	$(RM) *.o *~ core
	$(RM) $(TARGET) $(TARGET).exe
	$(RM) Makefile

# dependencies
gram.tab.o : gram.tab.c lex.yy.c mkfa.h
gram.tab.c : gram.y
$(OBJS) : mkfa.h
