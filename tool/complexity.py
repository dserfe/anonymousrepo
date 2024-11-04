import csv
import ast
import datetime
import string
import subprocess
import utils
import os
from subprocess import Popen, PIPE

def cal_mi_value(file_path):
    radon_halstead_opts =  ["radon", "hal", file_path]
    hal_output = utils.run_cmds(radon_halstead_opts, None)
    print("Halstead Metrics:" + hal_output.replace("\n",",") + "\n")

    radon_mi_opts = ["radon", "mi", file_path, "-s"]
    mi_output = utils.run_cmds(radon_mi_opts, None)
    print("Maintainability Index:" + mi_output.replace("\n",",") + "\n")
    mi_value = mi_output.split(" - ")[-1].replace(" ","").replace("\n","").split("(")[-1].split(")")[0]
    return mi_value

def cal_cyclomatic_cmplx(file_path):
    try:
        content = utils.read_file(file_path)
        new_content = "def test():\n"
        for line in content.split("\n"):
            newline = "  "+ line + "\n"
            new_content += newline
        tmp_path = ".tmp_cal_cyclomatic_cmplx.py"
        utils.write_file(tmp_path,new_content)
        lizard_opts = ["lizard", tmp_path]
        lizard = subprocess.run(lizard_opts, stdout=subprocess.PIPE)
        lizard_output = lizard.stdout.decode('utf-8').replace("\n",",")
        items = " ".join(lizard_output.split(",")[-2].strip().split()).split(" ")
        radon_opts = ["radon", "cc", tmp_path, "-a"]
        radon = subprocess.run(radon_opts, stdout=subprocess.PIPE)
        radon_output = radon.stdout.decode('utf-8').replace("\n",",")
        cc = radon_output.split("Average complexity:")[-1].replace(" ","").replace(",","").split("(")[-1].split(")")[0]
        # print(radon_output)
        # print(cc)
        # exit(0)
    except:
        cc = 0
    k = {
            "Nloc":items[0].strip(),
            # "Avg_NLOC": items[1],  
            "AvgCCN": items[2].strip(),
            # "Avg_token": items[3],
            "Fun_Cnt":int(items[4].strip())-1,
        }
    
    return k

def cal_complexity(file_path):
    res = {
        "effort": None, "difficulty": None, "calculated_length": None,
        "length": None, "vocabulary": None, "mi_value": None
    }
    try:
        content = utils.read_file(file_path)
        new_content = "def test():\n"
        for line in content.split("\n"):
            newline = "  "+ line + "\n"
            new_content += newline
        tmp_path = ".tmp_cal_complexity.py"
        utils.write_file(tmp_path,new_content)

        radon_halstead_opts =  ["radon", "hal", tmp_path]
        hal_output = utils.run_cmds(radon_halstead_opts, None).replace("\n",",")
        # print(hal_output)
        effort = hal_output.split(",")[-4].split(":")[-1].strip()
        difficulty = hal_output.split(",")[-5].split(":")[-1].strip()
        calculated_length = hal_output.split(",")[-7].split(":")[-1].strip()
        length = hal_output.split(",")[-8].split(":")[-1].strip()
        vocabulary = hal_output.split(",")[-9].split(":")[-1].strip()
        # print(effort,difficulty,calculated_length,length,vocabulary)

        radon_mi_opts = ["radon", "mi", tmp_path, "-s"]
        mi_output = utils.run_cmds(radon_mi_opts, None)
        # print("Maintainability Index:" + mi_output.replace("\n",",") + "\n")
        mi_value = mi_output.split(" - ")[-1].replace(" ","").replace("\n","").split("(")[-1].split(")")[0]

        res = {
            "effort": effort, "difficulty": difficulty, "calculated_length": calculated_length,
            "length": length, "vocabulary": vocabulary, "mi_value": mi_value
        }
    except:
        pass
    return res

def find_tests(testdir, id):
    tests = {}
    for dirpath, _, files in os.walk(testdir):
        for file in files:
            if id + "_" in file and ".in" in file:
                idx = file.split(".")[0].split("_")[-1]
                in_file_path = os.path.join(dirpath, file)
                out_file_path = in_file_path.replace("_" + idx + ".in", "_" + idx + ".out")
                if os.path.exists(out_file_path) == False:
                    raise Exception("Test {} with index {} in&out files not matching!".format(id, idx))
                if idx not in tests:
                    tests[idx] = {"in": None, "out":None}
                tests[idx]["in"] = in_file_path
                tests[idx]["out"] = out_file_path
    return tests

def run_pytest(id, filepath, testdir):
    conclusion = None
    if "codeforces" in id or "atcoder" in id:
        conclusion = run_avatar_test(id, filepath, testdir)
    elif "HumanEval" in id:
        conclusion = run_humaneval_test(id, filepath, testdir)
    elif "ClassEval" in id:
        conclusion = run_classeval_test(id, filepath, testdir)
    elif "sample" in id:
        conclusion = run_cruxeval_test(id, filepath, testdir)
    else:
        raise ValueError(f"{file_path} is not in a supportive benchmark!")
    return conclusion

def run_cruxeval_test(id, filepath, testdir):
    print("*Running tests for: {}".format(id))
    test_file = os.path.join(testdir, "test", id + "_test.py")
    code = utils.read_file(filepath)
    input_content = utils.read_file(test_file)
    
    failure = []
    tests_pass = []
    error_or_timeout = []
    conclusion = []

    check_file = ".tmp_test/tmp_test.py" + id
    os.makedirs(".tmp_test/", exist_ok=True)
    new_code = f"{code}\n{input_content}\n"
    # print(new_code)
    utils.write_file(check_file, new_code)
    p = Popen(['python3', check_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    try:
        stdout, stderr_data = p.communicate(timeout=100)#input=input_content.encode(), 
        output_actual, stderr_actual = stdout.decode('utf-8'), stderr_data.decode('utf-8')
        print(output_actual, stderr_actual)
        if output_actual == "" and stderr_actual == "":
            tests_pass.append(filepath)
        elif "AssertionError" in output_actual:
            print(f"output_actual, stderr_data: {output_actual, stderr_data}")
            failure.append(filepath)
        else:
            print(f"output_actual, stderr_data: {output_actual, stderr_data}")
            error_or_timeout.append(filepath)
    except subprocess.TimeoutExpired:
        error_or_timeout.append(filepath)
        
    results = {
        "tests_pass": tests_pass,
        "failure": failure,
        "error_or_timeout": error_or_timeout
    }
    for res in results:
        if len(results[res]):
            conclusion.append(res)
    print(f"Result: {conclusion}")
    return conclusion

def run_classeval_test(id, filepath, testdir):
    print("*Running tests for: {}".format(id))
    test_file = os.path.join(testdir, "test", id + "_test.py")
    code = utils.read_file(filepath)
    input_content = utils.read_file(test_file)
    
    failure = []
    tests_pass = []
    error_or_timeout = []
    conclusion = []
    entry_point = """\n
if __name__ == "__main__":
    unittest.main()
    """
    check_file = ".tmp_test/tmp_test.py"  + id
    os.makedirs(".tmp_test/", exist_ok=True)
    new_code = f"{code}\n{input_content}\n{entry_point}"
    # print(new_code)
    utils.write_file(check_file, new_code)
    try:
        # print(os.getcwd())
        result = subprocess.run(['python3', check_file], capture_output=True, text=True)
        output = result.stderr
        print(output)
        if "OK" in output:
            tests_pass.append(filepath)
        elif "AssertionError" in output or "FAIL" in output or "FAILED" in output:
            failure.append(filepath)
        else:
            error_or_timeout.append(filepath)
    except subprocess.TimeoutExpired:
        error_or_timeout.append(filepath)
        
    results = {
        "tests_pass": tests_pass,
        "failure": failure,
        "error_or_timeout": error_or_timeout
    }
    for res in results:
        if len(results[res]):
            conclusion.append(res)
    print(f"Result: {conclusion}")
    return conclusion

def run_humaneval_test(id, filepath, testdir):
    print("*Running tests for: {}".format(id))
    test_file = os.path.join(testdir, "test", id + "_test.py")
    entry_file = os.path.join(testdir, "entry", id + "_entry.txt")
    code = utils.read_file(filepath)
    input_content = utils.read_file(test_file)
    entry_point = utils.read_file(entry_file)
    
    failure = []
    tests_pass = []
    error_or_timeout = []
    conclusion = []

    check_file = ".tmp_test/tmp_test.py" + id
    os.makedirs(".tmp_test/", exist_ok=True)
    new_code = f"{code}\n{input_content}\ncheck({entry_point})"
    # print(new_code)
    utils.write_file(check_file, new_code)
    p = Popen(['python3', check_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    try:
        stdout, stderr_data = p.communicate(timeout=100)#input=input_content.encode(), 
        output_actual, stderr_actual = stdout.decode('utf-8'), stderr_data.decode('utf-8')
        print(output_actual, stderr_actual)
        if output_actual == "" and stderr_actual == "":
            tests_pass.append(filepath)
        elif "AssertionError" in output_actual:
            print(f"output_actual, stderr_data: {output_actual, stderr_data}")
            failure.append(filepath)
        else:
            print(f"output_actual, stderr_data: {output_actual, stderr_data}")
            error_or_timeout.append(filepath)
    except subprocess.TimeoutExpired:
        error_or_timeout.append(filepath)
        
    results = {
        "tests_pass": tests_pass,
        "failure": failure,
        "error_or_timeout": error_or_timeout
    }
    for res in results:
        if len(results[res]):
            conclusion.append(res)
    print(f"Result: {conclusion}")
    return conclusion
    

def run_avatar_test(id, filepath, testdir):
    print("Running tests for: {}".format(id))
    tests_pass = []
    infinite_loop = []
    runtime_error = []
    test_failure = []
    compileerror_or_timeout = []
    details = []
    runtime_error_details = []
    test_failure_details = []
    conclusion = []
    tests = find_tests(testdir, id)
    tests_passed = 0
    for idx in tests:
        infile = tests[idx]["in"]
        outfile = tests[idx]["out"]
        input_content = utils.read_file(infile)
        output_expected = utils.read_file(outfile)
        p = Popen(['python3', filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
        try:
            print(infile)
            stdout, stderr_data = p.communicate(input=input_content.encode(), timeout=100)
            output_actual = stdout.decode('utf-8')
        except subprocess.TimeoutExpired:
            compileerror_or_timeout.append(filepath)
            break

        detail = "Test {} has actual output {}, expected output is {}".format(idx, output_actual.strip(), output_expected.strip())
        details.append(detail)
        print(detail, flush = True)
        if(output_actual.strip().replace("\n", " ") == output_expected.strip().replace("\n", " ")):
            tests_passed += 1
        else:
            if stderr_data.decode()=='':
                print("[Drop Transformation] due to test failure.")
                if filepath not in runtime_error:
                    test_failure.append(filepath)
                    test_failure_details.append(detail)
                    break
            else:
                print(f"[Drop Transformation]due to runtime error: {stderr_data.decode()}")
                if filepath not in test_failure:
                    runtime_error.append(filepath)
                    runtime_error_details.append(detail)
                    break
    if tests_passed == len(tests):
        tests_pass.append(filepath)

    results = {
        "tests_pass": tests_pass,
        "infinite_loop": infinite_loop,
        "runtime_error": runtime_error,
        "test_failure": test_failure,
        "compileerror_or_timeout": compileerror_or_timeout
    }
    for res in results:
        if len(results[res]):
            conclusion.append(res)
    return conclusion