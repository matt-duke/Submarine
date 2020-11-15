CC = gcc
CFLAGS = -Wall
SRC = $(wildcard *.c)
ROOTDIR = $(shell readlink --canonicalize ../..)
CMN = $(wildcard $(ROOTDIR)/common/*.c)
BINDIR = $(ROOTDIR)/bin
INCLUDES = -I$(CURDIR) -I$(ROOTDIR)/libs -I$(ROOTDIR)/common
LIBDIR = -L$(ROOTDIR)/libs/logger
LIBS  = -lhiredis_vip -levent -lpthread -llogger
EXE = $(BINDIR)/$(patsubst %.c,%,$(notdir $(CURDIR)).c)

all:
	$(CC) $(CFLAGS) $(INCLUDES) $(SRC) $(CMN) -o $(EXE) $(LIBS) $(LIBDIR)


# TODO #
# Make factory calibration app
