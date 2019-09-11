CFLAGS= -Wall -Wextra -Wpointr-arith -g
CC = gcc

SRCS := $(wildcard *.c)
HEADERS := $(wildcard *.h)
OBJECTS := $(SRCS:%.c=%.o)
BINS := $(SRCS:%.c=%)

all: $(BINS)

.PHONY: all clean

%: %.o
	$(CC) $(CFLAGS) $< -o $@.out

%.o: %.c
	$(CC) -c $< $@.o

clean:
	rm -rf *.o $(BINS)
