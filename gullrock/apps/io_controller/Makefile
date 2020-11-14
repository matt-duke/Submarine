CC = gcc
CFLAGS = -Wall
SRC = io_controller.c
ROOTDIR = $(shell readlink --canonicalize ../..)
CMN = $(wildcard $(ROOTDIR)/common/*.c)
BINDIR = $(ROOTDIR)/bin
INCLUDES = -I$(CURDIR) -I$(ROOTDIR)/libs -I$(ROOTDIR)/common -I$(ROOTDIR)/libs/linux-mpu9150/eMPL
LIBDIR = -L$(ROOTDIR)/libs/logger
LIBS  = -lhiredis_vip -levent -lpthread -llogger
EXE = $(BINDIR)/$(patsubst %.c,%,$(notdir $(CURDIR)).c)

all:
	$(CC) $(CFLAGS) $(INCLUDES) $(SRC) $(CMN) -o $(EXE) $(LIBS) $(LIBDIR)


# TODO #
# Make factory calibration app
