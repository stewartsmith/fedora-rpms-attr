# Makefile for source rpm: attr
# $Id$
NAME := attr
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
