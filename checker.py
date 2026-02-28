#!/usr/bin/env python3

import os
import sys
import subprocess

# (subtask_name, n, num_tests) or (subtask_name, n, num_tests, max_abs); max_abs optional, default from generator
DEFAULT_MAX_ABS = 1000
params = [
    # ["Subtask1", 8, 100],
    # ["Subtask2", 9, 10],
    # ["Subtask3", 1000, 20, 10**6],
    ["Subtask4", 1000, 10, 10**7],
    ["Subtask5", 10000, 10, 10**8],
    ["Subtask6", 10**4, 10, 10**9],
    ["Subtask7", 10**4 + 5 * 10**3, 10, 10**9],
]

SRC_DIR = "./src"
INPUT_DIR = "input"
OUTPUT_DIR = "output"
REF_DIR = "ref"
REF_NAME = "answer.ref"
RUN_TIMEOUT = 2
REF_TIMEOUT = 60  # timeout for reference solution (good_src), e.g. for large n

# good_src = "brute_force"
# alt_src = ["basic_greedy", "optimized_greedy"]

good_src = "basic_greedy"
alt_src = ["optimized_greedy"]


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
        max_abs = param[3] if len(param) >= 4 else DEFAULT_MAX_ABS
        for i in range(num_tests):
            test_path = os.path.join(INPUT_DIR, f"{subtask}Test{i}.in")
            cmd = ["./tools/generator", test_path, str(n), str(max_abs)]
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if r.returncode != 0:
                print(f"Generator failed for {test_path}: {r.stderr}")
                sys.exit(1)


def generateRefs():
    """Generate test files into input/ and reference outputs into ref/ using good_src."""
    build()
    generateTests()
    if not os.path.isdir(INPUT_DIR):
        return
    os.makedirs(REF_DIR, exist_ok=True)
    in_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in"))
    for filename in in_files:
        test_name = filename[:-3]
        in_path = os.path.join(INPUT_DIR, filename)
        ref_path = os.path.join(REF_DIR, f"{test_name}.ref")
        try:
            with open(in_path, "rb") as fin:
                r = subprocess.run(
                    [f"./src/{good_src}"],
                    stdin=fin,
                    capture_output=True,
                    text=True,
                    timeout=REF_TIMEOUT,
                )
        except subprocess.TimeoutExpired:
            print(f"Warning: {good_src} timeout on {filename}, skipping ref.")
            continue
        if r.returncode != 0:
            print(f"Warning: {good_src} exit {r.returncode} on {filename}, skipping ref.")
            continue
        with open(ref_path, "w") as f:
            f.write(r.stdout)
    print(f"Refs written to {REF_DIR}/ (using {good_src}).")


def testsAlts():
    """Run each .in with good_src (reference), then each alt in alt_src; compare and report per alt."""
    if not os.path.isdir(INPUT_DIR):
        print("No input/ directory. Run generateTests first.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    in_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in"))
    if not in_files:
        print("No .in files in input/.")
        return

    ref_path = os.path.join(OUTPUT_DIR, REF_NAME)
    # results[alt_name] = {"passed": int, "failed": [(test_name, msg), ...]}
    results = {alt: {"passed": 0, "failed": []} for alt in alt_src}
    total = len(in_files)
    ref_fail_count = 0

    for filename in in_files:
        test_name = filename[:-3]
        in_path = os.path.join(INPUT_DIR, filename)

        # Run reference (good_src) once per test
        try:
            with open(in_path, "rb") as fin:
                r = subprocess.run(
                    [f"./src/{good_src}"],
                    stdin=fin,
                    capture_output=True,
                    text=True,
                    timeout=REF_TIMEOUT,
                )
        except subprocess.TimeoutExpired:
            ref_fail_count += 1
            for alt in alt_src:
                results[alt]["failed"].append((test_name, f"{good_src} timeout (no ref)"))
            continue
        if r.returncode != 0:
            ref_fail_count += 1
            for alt in alt_src:
                results[alt]["failed"].append((test_name, f"{good_src} exit {r.returncode} (no ref)"))
            continue

        with open(ref_path, "w") as f:
            f.write(r.stdout)
        ref_content = open(ref_path).read().strip()

        # Run each alt and compare to ref
        for alt in alt_src:
            out_path = os.path.join(OUTPUT_DIR, f"{test_name}_{alt}.out")
            try:
                with open(in_path, "rb") as fin:
                    r2 = subprocess.run(
                        [f"./src/{alt}"],
                        stdin=fin,
                        capture_output=True,
                        text=True,
                        timeout=RUN_TIMEOUT,
                    )
            except subprocess.TimeoutExpired:
                results[alt]["failed"].append((test_name, "timeout"))
                continue
            if r2.returncode != 0:
                results[alt]["failed"].append((test_name, f"exit {r2.returncode}: {r2.stderr or r2.stdout}"))
                continue

            with open(out_path, "w") as f:
                f.write(r2.stdout)
            out_content = r2.stdout.strip()
            if ref_content != out_content:
                results[alt]["failed"].append((test_name, f"diff: ref={ref_content!r} vs out={out_content!r}"))
            else:
                results[alt]["passed"] += 1

    # Report per alt
    if ref_fail_count:
        print(f"{good_src} (reference) failed on {ref_fail_count} test(s) (no ref for alts).")
    for alt in alt_src:
        passed = results[alt]["passed"]
        failed_list = results[alt]["failed"]
        print(f"{alt}: {passed}/{total} passed.")
        if failed_list:
            print(f"  Failed ({len(failed_list)}):")
            for name, msg in failed_list:
                print(f"    {name}: {msg}")
    if all(len(results[alt]["failed"]) == 0 for alt in alt_src) and ref_fail_count == 0:
        print("All tests passed for all alts.")


def all_cmd():
    build()
    generateTests()
    testsAlts()


def printUsage():
    print(f"Usage: {sys.argv[0]} <command>")
    print("Commands:")
    print("  build         Build generator and solutions")
    print("  generateTests Generate test cases into input/")
    print("  generateRefs  Generate tests and refs (using good_src) into input/ and ref/")
    print("  testsAlts     Run good_src (reference) vs each alt in alt_src and compare")
    print("  all           Build, generate tests, then run checks")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        printUsage()
    elif sys.argv[1] == "build":
        build()
    elif sys.argv[1] == "generateTests":
        generateTests()
    elif sys.argv[1] == "generateRefs":
        generateRefs()
    elif sys.argv[1] == "testsAlts":
        testsAlts()
    elif sys.argv[1] == "all":
        all_cmd()
    else:
        printUsage()
