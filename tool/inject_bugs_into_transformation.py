import os
import sys
import csv
import utils
import json

def get_python_files_dir(directory):
    file_list = []
    for dir, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") or ".py" in file:
                file_path = os.path.join(dir, file)
                file_list.append(file_path)
    return file_list

def get_dataset(dataset_dir):
    dataset = {}
    file_paths = get_python_files_dir(dataset_dir)
    for file_path in file_paths:
        file_ID = file_path.split("/")[-1].split(".py")[0]
        if file_ID not in dataset:
            dataset[file_ID] = {
                "file": file_path,
                "correct_code": utils.read_file(file_path)
            }
    return dataset

def get_datasets(dataset_dir):
    dataset = {}
    file_paths = get_python_files_dir(dataset_dir)
    for file_path in file_paths:
        if file_path.endswith(".csv") or file_path.endswith(".png"):
            continue
        file_ID = file_path.split("/")[-1].split(".py")[0]
        if file_ID not in dataset:
            dataset[file_ID] = {
                "file": []
            }
        dataset[file_ID]["file"].append(file_path)
    return dataset

def inject_buggy_stats(correct_code, target_file, bugs):
    tag = False
    num = 0
    print(target_file, "original bugs:", len(bugs))
    num = 0
    for original_stat in bugs:
        if original_stat in correct_code:
            correct_code.replace(original_stat, bugs[original_stat])
            print(f"{target_file}: correct: {original_stat}, buggy: {bugs[original_stat]}")
            num += 1
            tag = True
    print(target_file, "new bugs:", num)
    if tag:
        utils.write_file(target_file, correct_code)
    return tag

def main(dataset, bug_info, backup):
    for ID in dataset:
        # print(ID)
        index = f"/home/yang/Benchmark/dataset/python_codenet/{ID}.py"
        if index not in bug_info:
            print(f"{ID} not in bug_info")
            continue
        file = dataset[ID]["file"]
        correct_code = dataset[ID]["correct_code"]
        bugs = bug_info[index]["diff"]
        
        name_seed = utils.generate_sha(file)
        tmp_dir = "./apr_bugs_transformation"
        target_file = f"{tmp_dir}/{file.split('/')[-1].split('-')[0]}-{name_seed}" 
        tag = inject_buggy_stats(correct_code, target_file, bugs)
        if not tag:
            for file_path in backup[ID]["file"]:
                # print(file_path)
                correct_code = utils.read_file(file_path)
                name_seed = utils.generate_sha(file_path)
                tmp_dir = "./apr_bugs_transformation"
                target_file = f"{tmp_dir}/{file_path.split('/')[-1].split('-')[0]}-{name_seed}" 
                tag = inject_buggy_stats(correct_code, target_file, bugs)
                if tag:
                    break
                
        # print(target_file)
        
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def inject_bugs_per_case(program_file, bugs, tmp_dir):
    correct_code = utils.read_file(program_file)
    applied = {"diff":{}}
    
    name_seed = utils.generate_sha(program_file)
    target_file = f"{tmp_dir}/{program_file.split('/')[-1].split('-')[0]}-{name_seed}"
    
    for original_stat in bugs["diff"]:
        if original_stat in correct_code:
            new_code = correct_code.replace(original_stat, bugs["diff"][original_stat])
            correct_code = new_code
            applied["diff"].update({original_stat: bugs["diff"][original_stat]})
    utils.write_file(target_file, correct_code)
    return applied, target_file
    
def inject_bugs(bug_info, original_dataset, transformation_programs):
    original_dir = "original_bugs_humaneval"
    transformation_dir = "transformation_bugs_humaneval"
    for original_file_ID in bug_info:
        ID = original_file_ID.split("/")[-1].split(".py")[0]
        if ID not in transformation_programs:
            continue
        
        transformation_file = transformation_programs[ID]["file"][0]
        original_file = original_dataset[ID]["file"][0]

        applied, transformation_bugs_file = inject_bugs_per_case(transformation_file, bug_info[original_file_ID], transformation_dir)
        applied, original_bugs_file = inject_bugs_per_case(original_file, applied, original_dir)
        if len(applied):
            print(f"{applied},{original_bugs_file}, {transformation_bugs_file}")
        
if __name__ == "__main__":
    args = sys.argv[1:]
    original_programs = args[0]
    transformations = args[1]
    bugs = args[2] # humaneval_bugs.json; codenet_bugs.json
    
    bug_info = read_json(bugs)
    original_dataset = get_datasets(original_programs)
    transformation_programs = get_datasets(transformations)
    inject_bugs(bug_info, original_dataset, transformation_programs)