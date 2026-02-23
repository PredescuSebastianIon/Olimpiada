#!/usr/bin/env python3

import os
import sys
import subprocess

# subtask name, n, number of tests
params = [
    ["Subtask1", 8, 100],
    ["Subtask2", 9, 100],
    ["Subtask3", 10, 100],
]

SRC_DIR = "./src"
INPUT_DIR = "input"
OUTPUT_DIR = "output"
REF_NAME = "answer.ref"
RUN_TIMEOUT = 2

good_src = "brute_force"
alt_src = ["basic_greedy", "optimized_greedy"]


def build():
    """Compile generator and both solutions."""
    r = subprocess.run(["make", "all"], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print("Build failed:")
        print(r.stdout or "")
        print(r.stderr or "")
        sys.exit(1)


def generateTests():
    """Generate test files into input/."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    for param in params:
        subtask, n, num_tests = param[0], param[1], param[2]
        for i in range(num_tests):
            test_path = os.path.join(INPUT_DIR, f"{subtask}Test{i}.in")
            r = subprocess.run(
                ["./tools/generator", test_path, str(n)],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if r.returncode != 0:
                print(f"Generator failed for {test_path}: {r.stderr}")
                sys.exit(1)


def testsAlts():
    """Run each .in with brute_force (reference) and basic_greedy, compare outputs."""
    if not os.path.isdir(INPUT_DIR):
        print("No input/ directory. Run generateTests first.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    in_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in"))
    if not in_files:
        print("No .in files in input/.")
        return

    ref_path = os.path.join(OUTPUT_DIR, REF_NAME)
    passed = 0
    failed = []

    for filename in in_files:
        test_name = filename[:-3]
        in_path = os.path.join(INPUT_DIR, filename)

        # Run brute_force
        try:
            with open(in_path, "rb") as fin:
                r = subprocess.run(
                    ["./src/brute_force"],
                    stdin=fin,
                    capture_output=True,
                    text=True,
                    timeout=RUN_TIMEOUT,
                )
        except subprocess.TimeoutExpired:
            failed.append((test_name, "brute_force timeout"))
            continue
        if r.returncode != 0:
            failed.append((test_name, f"brute_force exit {r.returncode}: {r.stderr}"))
            continue

        with open(ref_path, "w") as f:
            f.write(r.stdout)

        # Run basic_greedy
        out_path = os.path.join(OUTPUT_DIR, f"{test_name}_basic_greedy.out")
        try:
            with open(in_path, "rb") as fin:
                r2 = subprocess.run(
                    ["./src/basic_greedy"],
                    stdin=fin,
                    capture_output=True,
                    text=True,
                    timeout=RUN_TIMEOUT,
                )
        except subprocess.TimeoutExpired:
            failed.append((test_name, "basic_greedy timeout"))
            continue
        if r2.returncode != 0:
            failed.append((test_name, f"basic_greedy exit {r2.returncode}: {r2.stderr}"))
            continue

        with open(out_path, "w") as f:
            f.write(r2.stdout)

        # Compare
        ref_content = open(ref_path).read().strip()
        out_content = open(out_path).read().strip()
        if ref_content != out_content:
            failed.append((test_name, f"diff: ref={ref_content!r} vs out={out_content!r}"))
        else:
            passed += 1

    total = len(in_files)
    print(f"Tests: {passed}/{total} passed.")
    if failed:
        print(f"Failed ({len(failed)}):")
        for name, msg in failed:
            print(f"  {name}: {msg}")
    else:
        print("All tests passed.")


def all_cmd():
    build()
    generateTests()
    testsAlts()


def printUsage():
    print(f"Usage: {sys.argv[0]} <command>")
    print("Commands:")
    print("  build         Build generator and solutions")
    print("  generateTests Generate test cases into input/")
    print("  testsAlts     Run brute_force vs basic_greedy and compare")
    print("  all           Build, generate tests, then run checks")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        printUsage()
    elif sys.argv[1] == "build":
        build()
    elif sys.argv[1] == "generateTests":
        generateTests()
    elif sys.argv[1] == "testsAlts":
        testsAlts()
    elif sys.argv[1] == "all":
        all_cmd()
    else:
        printUsage()
