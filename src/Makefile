CXX := g++
.DEFAULT_GOAL := help

.PHONY: help build clean clean-input clean-output clean-all

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  build        Build all solutions"
	@echo "  clean        Clean all solutions"
	@echo "  clean-input  Clean all input files"
	@echo "  clean-output Clean all output files"
	@echo "  clean-all    Clean all input and output files"

brute_force: brute_force.cpp
	$(CXX) -O2 -o brute_force brute_force.cpp

basic_greedy: basic_greedy.cpp
	$(CXX) -O2 -o basic_greedy basic_greedy.cpp

optimized_greedy: optimized_greedy.cpp
	$(CXX) -O2 -o optimized_greedy optimized_greedy.cpp

build: brute_force basic_greedy optimized_greedy

clean-all: clean clean-input clean-output

clean:
	rm -f brute_force basic_greedy optimized_greedy

clean-input:
	rm -f input/*

clean-output:
	rm -f output/*
