all: generator build

generator: tools/generator.cpp
	g++ -O2 -o tools/generator tools/generator.cpp

build:
	$(MAKE) -C src build

clean:
	rm -f tools/generator
	$(MAKE) -C src clean

.PHONY: all build clean generator
