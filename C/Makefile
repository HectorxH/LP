TARGET = main.c

CFLAGS = -Wall -Wextra -Wpointer-arith -g
CC = gcc

SRCS := $(wildcard *.c)
HEADERS := $(wildcard *.h)
OBJECTS := $(SRCS:%.c=%.o)
BINS := $(TARGET:%.c=%.out)

all: $(BINS)

.PHONY: all clean

%.o: $(SRCS) $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(BINS) $(TARGET) $(OBJECTS)

$(BINS): $(TARGET) $(OBJECTS)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf *.o $(BINS)
