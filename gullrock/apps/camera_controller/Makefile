CC = gcc
CFLAGS = -Wall
SRC = $(wildcard *.c)
ROOTDIR = $(shell readlink --canonicalize ../..)
CMN = $(wildcard $(ROOTDIR)/common/*.c)
BINDIR = $(ROOTDIR)/bin
INCLUDES = -I$(ROOTDIR)/libs -I$(ROOTDIR)/common
LIBDIR = -L$(ROOTDIR)/libs/logger
LIBS  = -lhiredis_vip -lpthread -llogger -levent
EXE = $(BINDIR)/$(patsubst %.c,%,$(SRC))

all:
	$(CC) $(CFLAGS) $(INCLUDES) $(SRC) $(CMN) -o $(EXE) $(LIBS) $(LIBDIR)
