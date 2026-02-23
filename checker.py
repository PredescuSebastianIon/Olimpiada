#!/usr/bin/env python3

import os
import sys

# subtask name, n, number of tests
params = [
    ["Subtask1", 8, 100], 
    ["Subtask2", 9, 100], 
    ["Subtask3", 10, 100], 
]

SRC_DIR = "./src"

good_src = "brute_force"
alt_src = ["tasks"]

os.system("make -C src clean build")

def all():
    generateTests()
    testsAlts()

def testsAlts():
    input_dir = os.fsencode("input")
    for file in os.listdir(input_dir):
        filename = os.fsdecode(file)
        # run test on brute_force and save to answer.ref
        # run on alt_src and save it to the f"output/{test_name}{alt_src}.out"
        # if diff -q answer.ref f"output/{test_name}{alt_src}.out"




def generateTests():
    for param in params:
        # Generate param[2] tests
        for i in range(param[2]):
            test_name = f"input/{param[0]}Test{i}.in"
            os.system(f"./tools/generator {test_name} {param[1]}")
        

def printUsage():
    print(f"Usage: {sys.argv[0]} <command>")
    print("Commands:")
    print("  generateTests   Generate test cases")
    print("  testsAlts       Run alternative solutions")
    print("  all             Generate tests and run checks")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        printUsage()
    elif sys.argv[1] == "generateTests":
        generateTests()
    elif sys.argv[1] == "testsAlts":
        testsAlts()
    elif sys.argv[1] == "all":
        all()
    else:
        printUsage()
