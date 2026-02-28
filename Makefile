CXX := g++
CXXFLAGS := -O2 -std=c++11

all: generator build

generator: tools/generator.cpp
	$(CXX) $(CXXFLAGS) -o tools/generator tools/generator.cpp

build:
	$(MAKE) -C src build

clean:
	rm -f tools/generator
	$(MAKE) -C src clean

.PHONY: all build clean generator help clean-input clean-output clean-ref clean-all

clean-input:
	rm -f input/*

clean-output:
	rm -f output/*

clean-ref:
	rm -f ref/*

clean-all: clean clean-input clean-output clean-ref

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  all          Build generator and solutions (default)"
	@echo "  build        Build solutions only"
	@echo "  generator    Build generator only"
	@echo "  clean        Remove binaries"
	@echo "  clean-input  Remove input/"
	@echo "  clean-output Remove output/"
	@echo "  clean-ref    Remove ref/"
	@echo "  clean-all    clean + clean-input + clean-output + clean-ref"