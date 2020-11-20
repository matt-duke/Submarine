CC = gcc
CFLAGS = -Wall
SRCDIR = src
SRC = $(wildcard $(SRCDIR)/*.c)
ROOTDIR = $(shell readlink --canonicalize ../..)
CMN = $(wildcard $(ROOTDIR)/common/*.c)
BINDIR = $(ROOTDIR)/bin
INCLUDES = -I$(CURDIR) -I$(ROOTDIR)/libs -I$(ROOTDIR)/common
LIBDIR = -L$(ROOTDIR)/libs/logger -L$(ROOTDIR)/libs/minihdlc
LIBS  = -lhiredis_vip -levent -lpthread -llogger -lminihdlc
EXE = $(BINDIR)/$(patsubst %.c,%,$(notdir $(CURDIR)).c)

all:
	$(CC) $(CFLAGS) $(INCLUDES) $(SRC) $(CMN) -o $(EXE) $(LIBS) $(LIBDIR)

libs: $(LOGGER) $(MINIHDLC)
	cd $(LOGGER) && make
	cd $(MINIHDLC) && make