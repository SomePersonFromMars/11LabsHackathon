#!/usr/bin/env python3
import os
import subprocess

def compile_cpp_code(source_code):
    source_file_path = 'tmp.cpp'
    with open(source_file_path, 'w') as source_file:
        if isinstance(source_code, bytes):
            source_code = source_code.decode()
        source_file.write(source_code)
    executable = source_file_path.replace('.cpp', '')
    compile_command = f"g++ {source_file_path} -o {executable}"
    result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return ("", {"status": "FAILED", "output": result.stderr})
    return (executable, {"status": "SUCCESS"})

def run_tests(executable, tests_dict):
    statuses = {}
    for i, (test_name, test) in enumerate(tests_dict.items()):
        print(f"Running test {i + 1}/{len(tests_dict)}: {test_name}")
        input_data, expected_output = test
        result = subprocess.run([f"./{executable}"], input=input_data, capture_output=True, text=True)
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

def get_task_tests(tasks_path, task_index):
    tests_list = sorted([tasks_path + f'/{task_index}/tests/{file[:-3]}' for file in os.listdir(tasks_path + f'/{task_index}/tests') if file.endswith('.in')])
    tests_dict = {}
    for test_path in tests_list:
        test_name = os.path.basename(test_path)
        with open(f"{test_path}.in", 'r') as infile:
            input_data = infile.read()
        with open(f"{test_path}.out", 'r') as outfile:
            expected_output = outfile.read().strip()
        tests_dict[test_name] = (input_data, expected_output)
    return tests_dict

def compile_and_test_task(source_code, task_index, tasks_path='tasks'):
    tests_dict = get_task_tests(tasks_path, task_index)
    status = {}
    executable, compile_status = compile_cpp_code(source_code)
    status["compilation"] = compile_status
    if executable:
        test_statuses = run_tests(executable, tests_dict)
        os.remove(executable)
        status["tests"] = test_statuses
    return status

def main():
    with open('tasks/0/sol1.cpp', 'r') as file:
        source_code = file.read()

    status = compile_and_test_task(source_code, 0)

    print("Compilation status:", status["compilation"])
    if "tests" in status:
        for test_name, result in status["tests"].items():
            print(f"Test {test_name}: {result}")
    else:
        print("No tests were run.")

if __name__ == "__main__":
    main()