import argparse
import ast
import datetime
import os
import subprocess
import sys
import utils
import pprint
import python_transformer
import complexity
from utils import clear_string

"""
python -u to unbuffer
"""

def parse_args():
    parser = argparse.ArgumentParser(description="""
            A framework to automatically transform Python code.
            """,)
    parser.add_argument("-sd", "--src_dir", dest = "source_dir", required = False, default = None,
                        help = "a directory of source files you need to transform.")
    parser.add_argument("-td", "--target_dir", dest = "target_dir", required = False, default = None,
                        help = "a directory of target files to save after transformation.")
    parser.add_argument("-s", "--src_file", dest = "source_file", required = False, default = None,
                        help = "source file you need to transform.")
    parser.add_argument("-t", "--target_file", dest = "target_file", required = False, default = None,
                        help = "target file to save after transformation.")
    parser.add_argument("-j", "--json", dest = "json_file", required = False, default = None,
                        help = "save results into a json file.")
    parser.add_argument("-c", "--csv", dest = "csv_file", required = False, default = None,
                        help = "save statistics into a csv file.")
    parser.add_argument("-e", "--evaluation_tests_dir", dest = "evaluation_tests_dir", required = False, default = None,
                        help = "dir of tests to run.")
    parser.add_argument("-r", "--rule", dest = "single_rule", required = False, default = None,
                        help = "specify single rule to run.")
    parser.add_argument("-ga", "--genetic_algorithm", dest = "genetic_algorithm", required = False, default = None,
                        help = "code transformation with genetic algorithm")
    parser.add_argument("-num", "--num_candidates_to_select", dest = "num_candidates_to_select", required = False, default = 4,
                        help = "how many candidates to select for genetic algorithm")
    parser.add_argument("-b", "--benchmark", dest = "benchmark", required = False, default = None,
                        help = "a benchmark directory including multiple files you need to transform.")
    parser.add_argument("-apr", "--automated_program_repair", dest = "apr", required = False, default = None,
                        help = "if you need to generate programs for task program repair (True/False).")
    parser.add_argument("-bugs", "--inject_bugs", dest = "bug_injection", required = False, default = None,
                        help = "bug injection (True/False).")
    parser.add_argument("-applyall", "--applyall", dest = "applyall", required = False, default = None,
                        help = "apply all applicable rules.")
    parser.add_argument("-time_budget", "--time_budget", dest = "time_budget", required = False, default = None,
                        help = "time_budget")
    args = parser.parse_args()
    return args

def clear_content(source_file):
    """This function is to perform: original code -> ast(original code) -> unparse(ast(original code));
    In this way, you can avoid unnecessary changes when diff <orignal code, transformed code>. 
    For example, some syntactical elements, like double quotes, are converted into single quotes
    """
    clear_original_content = utils.clear_string(utils.read_file(source_file))
    tree = ast.parse(clear_original_content)
    clear_content = ast.unparse(tree)
    utils.write_file(source_file, clear_content)
    return source_file

def inject_bugs(benchmark, evaluation_tests_dir, csv_file, target_dir):
    files_to_transform = utils.get_python_files_dir(benchmark)
    if len(files_to_transform) == 0:
        print(f"No Python files in benchmark {files_to_transform}!")
        return
    json_file = python_transformer.inject_bugs(files_to_transform, evaluation_tests_dir, csv_file, target_dir)

def transform_benchmark(benchmark, evaluation_tests_dir, genetic_algorithm, csv_file, apr, time_budget):
    files_to_transform = utils.get_python_files_dir(benchmark)
    if len(files_to_transform) == 0:
        print(f"No Python files in benchmark {files_to_transform}!")
        return
    print(files_to_transform)
    python_transformer.initialize_whole_benchmark(files_to_transform, genetic_algorithm, evaluation_tests_dir, csv_file, time_budget, apr)
    exit(0)
    
def format_file_with_autopep8(filename):
    command = ["autopep8", "--in-place", filename]

    try:
        subprocess.run(command, check=True)
        print(f"The file '{filename}' has been formatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while formatting: {e}")
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main(source_file, target_file, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, json_file, apr): #json_file is actually csv in other places
    file_id = source_file.split("/")[-1].split(".py")[0]
    print("[START] processing file: {}".format(file_id))
    source_file = clear_content(source_file)

    transformed_code, applicable_rules, patch_path, exception, diff_output, patch_path = None, None, None, None, None, None
    start = datetime.datetime.now()
    before_test_results, after_test_results = None, None
    if evaluation_tests_dir:
        before_test_results = complexity.run_pytest(file_id, source_file, evaluation_tests_dir)
        if "tests_pass" not in str(before_test_results):
            end = datetime.datetime.now()
            total_time = (end - start).total_seconds()
            print("[END] processing file: {}. Total Time: {}".format(file_id, total_time))
            result= {"file_id":file_id, "source_file": source_file, "target_file": None, "evaluation_tests_dir": evaluation_tests_dir,
                    "single_rule": single_rule, "genetic_algorithm": genetic_algorithm, "patch_path": None, "applicable_rules": [],
                    "exception": "Original tests failure/error", "total_time": total_time, "test_results_before": before_test_results,
                    "test_results_after": None, "diff_output": None, "original_code": utils.read_file(source_file), "transformed_code": None,
                    }
            # pprint.pprint(result, indent=2)
            # print(result)
            utils.write_json(json_file, result)
            return result
        else:
            print("tests_pass", file_id, source_file)
    # try:
    if True:
        transformed_code, applicable_rules = python_transformer.initialize(source_file, single_rule, genetic_algorithm, target_file, num_candidates_to_select, file_id, evaluation_tests_dir, apr)    
        if len(applicable_rules) > 0:
            utils.write_file(target_file, transformed_code)
        if evaluation_tests_dir: # TODO: modifying running tests
            if len(applicable_rules) > 0 :
                format_file_with_autopep8(target_file)
                diff_output, patch_path = utils.diff(source_file, target_file)
                patch_path = os.path.join("/".join(target_file.split("/")[:-1]), file_id + ".patch")
                utils.write_file(patch_path, diff_output)
                print(f"Checking {target_file}")
                after_test_results = complexity.run_pytest(file_id, target_file, evaluation_tests_dir)
        
    # except Exception as ex:
    #     exception = ex
    #     print("Exception: {}".format(exception))

    end = datetime.datetime.now()
    total_time = (end - start).total_seconds()
    result = {
        "file_id":file_id,
        "source_file": source_file,
        "target_file": target_file,
        "evaluation_tests_dir": evaluation_tests_dir,
        "single_rule": single_rule, 
        "genetic_algorithm": genetic_algorithm,
        "patch_path": patch_path,
        "applicable_rules": applicable_rules,
        "exception": exception, 
        "total_time": total_time,
        "test_results_before": before_test_results,
        "test_results_after": after_test_results,
        "diff_output": patch_path,
        "original_code": utils.read_file(source_file),
        "transformed_code": transformed_code,
    }
    pprint.pprint(result, indent=2)
    # print(result)
    utils.write_json(json_file, result)
    # utils.write_dict_csv(csv_file, list(result.keys()), result)
    print("[END] processing file: {}. Total Time: {}".format(file_id, total_time))
    return result
            
def transform_single_file(source_file, target_file, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr=False):
    result = main(source_file, target_file, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr)
    return result

def transform_files_in_dir(src_dir, target_dir, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr=False):
    final_results = []
    file_pairs = get_file_list(src_dir, target_dir)
    print(file_pairs)
    for pair in file_pairs:
        result = transform_single_file(pair["src"], pair["target"], evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr)
        final_results.append(result)
    return final_results

def get_file_list(src_dir, target_dir):
    pairs = []
    os.makedirs(target_dir, exist_ok=True)
    for dirpath, _, files in os.walk(src_dir):
        for file in files:
            if not ".py" in file:# or not ".py" in file:
                continue
            src_file_path = os.path.join(dirpath, file)
            target_file_path = os.path.join(target_dir, file)
            pair = {"src":src_file_path, "target": target_file_path }
            pairs.append(pair)
    return pairs

def setup_csv(csv_file):
    headers = [
        "file_id",
        "source_file",
        "target_file",
        "evaluation_tests_dir",
        "single_rule",
        "genetic_algorithm",
        "patch_path",
        "applicable_rules",
        "exception",
        "total_time"
    ]
    utils.write_header_csv(csv_file, headers)

if __name__ == "__main__":
    args = parse_args()
    src_dir = args.source_dir
    target_dir = args.target_dir
    source_file = args.source_file
    target_file = args.target_file
    csv_file = args.csv_file
    json_file = args.json_file
    evaluation_tests_dir = args.evaluation_tests_dir
    single_rule = args.single_rule
    genetic_algorithm = args.genetic_algorithm
    num_candidates_to_select = args.num_candidates_to_select
    apr = args.apr
    benchmark = args.benchmark
    bug_injection = args.bug_injection
    if args.time_budget:
        time_budget = float(args.time_budget)
    
    print("STARTING AT", datetime.datetime.now())
    # setup_csv(csv_file)
    
    if src_dir == None and source_file: #and not inject_bugs:
        transform_single_file(source_file, target_file, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr)
    elif src_dir and source_file == None: #and not inject_bugs:
        transform_files_in_dir(src_dir, target_dir, evaluation_tests_dir, single_rule, genetic_algorithm, num_candidates_to_select, csv_file, apr)
    elif benchmark and genetic_algorithm: #and not inject_bugs:
        transform_benchmark(benchmark, evaluation_tests_dir, genetic_algorithm, csv_file, apr, time_budget)
    elif bug_injection:
        inject_bugs(benchmark, evaluation_tests_dir, csv_file, target_dir)
    # elif applyall:
    #     applyall()
    
    print("END AT", datetime.datetime.now())