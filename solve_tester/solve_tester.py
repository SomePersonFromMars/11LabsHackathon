#!/usr/bin/env python3
import os
import subprocess
import tempfile

def compile_cpp_code(source_code):
    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=True) as temp_source_file:
        temp_source_file.write(source_code.encode())
        temp_source_file.flush()
        executable = temp_source_file.name.replace('.cpp', '')
        compile_command = f"g++ {temp_source_file.name} -o {executable}"
        result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return ("", { "status": "FAILED", "output": result.stderr })
    return (executable, { "status": "SUCCESS" })

def run_tests(executable, tests_dict):
    statuses = {}
    for i, (test_name, test) in enumerate(tests_dict.items()):
        print(f"Running test {i + 1}/{len(tests_dict)}: {test_name}")
        input_data, expected_output = test
        result = subprocess.run([f"{executable}"], input=input_data, capture_output=True, text=True)
        if result.returncode != 0:
            statuses[test_name] = {"status": "FAILED", "error": result.stderr}
            continue
        actual_output = result.stdout.strip()
        if actual_output == expected_output:
            statuses[test_name] = {"status": "PASSED"}
        else:
            statuses[test_name] = {
                "status": "FAILED",
                "expected": expected_output,
                "actual": actual_output
            }
    return statuses

def compile_and_test(source_code, tests_paths = None, tests_dict = None):
    if not tests_dict:
        if not tests_paths:
            raise ValueError("Either tests_paths or tests_dict must be provided.")
        tests_dict = {}
        for test_path in tests_paths:
            test_name = os.path.basename(test_path)
            with open(f"{test_path}.in", 'r') as infile:
                input_data = infile.read()
            with open(f"{test_path}.out", 'r') as outfile:
                expected_output = outfile.read().strip()
            tests_dict[test_name] = (input_data, expected_output)

    status = { }
    executable, compile_status = compile_cpp_code(source_code)
    status["compilation"] = compile_status
    if executable:
        test_statuses = run_tests(executable, tests_dict)
        os.remove(executable)
        status["tests"] = test_statuses
    return status

def main():
    with open('tasks/0/sol.cpp', 'r') as file:
        source_code = file.read()

    tests_paths = ['tasks/0/tests/0', 'tasks/0/tests/1', 'tasks/0/tests/2']
    status = compile_and_test(source_code, tests_paths=tests_paths)

    print("Compilation status:", status["compilation"])
    if "tests" in status:
        for test_name, result in status["tests"].items():
            print(f"Test {test_name}: {result}")
    else:
        print("No tests were run.")

if __name__ == "__main__":
    main()