CXX := g++
.DEFAULT_GOAL := help

.PHONY: build clean

brute_force: brute_force.cpp
	$(CXX) -O2 -o brute_force brute_force.cpp

basic_greedy: basic_greedy.cpp
	$(CXX) -O2 -o basic_greedy basic_greedy.cpp

optimized_greedy: optimized_greedy.cpp
	$(CXX) -O2 -o optimized_greedy optimized_greedy.cpp

build: brute_force basic_greedy optimized_greedy

clean:
	rm -f brute_force basic_greedy optimized_greedy
