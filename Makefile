all: generator build

generator: tools/generator.cpp
	g++ -O2 -o tools/generator tools/generator.cpp

build:
	$(MAKE) -C src build

clean:
	rm -f tools/generator
	$(MAKE) -C src clean

.PHONY: all build clean generator help clean-input clean-output clean-all

clean-input:
	rm -f input/*

clean-output:
	rm -f output/*

clean-all: clean clean-input clean-output

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  build        Build all solutions"
	@echo "  clean        Clean all solutions"
	@echo "  clean-input  Clean all input files"
	@echo "  clean-output Clean all output files"
	@echo "  clean-all    Clean all input and output files"
	