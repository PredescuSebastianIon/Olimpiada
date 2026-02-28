CXX := g++
CXXFLAGS := -O2 -std=c++11

.PHONY: build clean

brute_force: brute_force.cpp
	$(CXX) $(CXXFLAGS) -o brute_force brute_force.cpp

basic_greedy: basic_greedy.cpp
	$(CXX) $(CXXFLAGS) -o basic_greedy basic_greedy.cpp

optimized_greedy: optimized_greedy.cpp
	$(CXX) $(CXXFLAGS) -o optimized_greedy optimized_greedy.cpp

build: brute_force basic_greedy optimized_greedy

clean:
	rm -f brute_force basic_greedy optimized_greedy
