# 
#  File: 
# 
# Copyright (C) Microsoft Corporation
# SPDX-License-Identifier: MIT


ifndef AFL_PATH
$(error AFL_PATH environment variable is not set)
endif

# Compiler and flags
CC = $(AFL_PATH)/afl-clang-fast   # Note: alf-clang-lto is another option, but it provides less accurate coverage data
CFLAGS = -ggdb -Wall -Wextra -Wno-unknown-pragmas -fprofile-instr-generate -fcoverage-mapping
INCLUDES = -I./ -Icommon/
LDFLAGS = -static -Wl,--allow-multiple-definition 

# Target executable
TARGET = example

# Find all C source files in the current directory
SRCS = $(wildcard common/*.c) example.c
OBJS = $(SRCS:.c=.o)

# Default target
all: $(TARGET)

# Rule to compile an executable
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) $(LDLIBS) $(INCLUDES)

# Clean rule
clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
