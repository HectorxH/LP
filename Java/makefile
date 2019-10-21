JFLAGS = -g -Xlint:all
JC = javac

JAVAS := $(wildcard estructuras/*.java) $(wildcard *.java)
CLASSES := $(JAVAS:.java=.class)

all: $(CLASSES)

.PHONY: all clean

%.class: %.java
	$(JC) $(JFLAGS) $^

.PRECIOUS: $(JAVAS)

clean:
	rm -rf $(CLASSES)
