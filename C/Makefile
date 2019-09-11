CFLAGS= -Wall -Wextra -Wpointer-arith -g
CC = gcc

SRCS := $(wildcard *.c)
HEADERS := $(wildcard *.h)
OBJECTS := $(SRCS:%.c=%.o)
BINS := $(SRCS:%.c=%.out)

all: $(BINS)

.PHONY: all clean

%.o: %.c
	$(CC) -c $<

%.out: %.o
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf *.o $(BINS)
