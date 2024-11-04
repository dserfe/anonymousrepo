from litellm import completion
import ast
import os
import time
import sys
import json
import google.generativeai as genai
from complexity import run_pytest
import utils

os.environ['GEMINI_API_KEY'] = "AIzaSyATD8hDdmnTJHw7uM9ZzJX_rKhA-cMQLhU"

class VariableReplacer(ast.NodeTransformer):
    def __init__(self, target_var, replacement_var):
        self.target_var = target_var
        self.replacement_var = replacement_var

    def visit_Name(self, node):
        if node.id == self.target_var:
            return ast.Name(id=self.replacement_var, ctx=node.ctx)
        return node
    
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.name == self.target_var:
            node.name = self.replacement_var
        return node

def replace_variable_in_statement(code, target_var, replacement_var):
    try:
        new_code = code.replace(target_var, replacement_var)
        # tree = ast.parse(code)
        # replacer = VariableReplacer(target_var, replacement_var)
        # new_tree = replacer.visit(tree)
        # new_code = ast.unparse(new_tree)
        return new_code
    except Exception as e:
        print(code, e)
        return code

def read_file(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def extract_variables(code):
    tree = ast.parse(code)
    collector = VariableCollector()
    collector.visit(tree)
    return collector.variables

class VariableCollector(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.Store)) and node.id not in {"True", "False", "None"}:
            if ("new" in node.id and "_" in node.id) or "loopchecker" in node.id or "conditionchecker" in node.id or "loop_" in node.id:
                self.variables.add(node.id)
        self.generic_visit(node)
    
    def visit_Module(self, node):
        self.generic_visit(node)

def extract_variables(code):
    tree = ast.parse(code)
    collector = VariableCollector()
    collector.visit(tree)
    print(collector.variables, "\n")
    return collector.variables

def generator_gemini(prompt, model = "gemini-1.5-pro"):
    messages = [
    {
        "role": "user",
        "content": prompt,
    }
    ]

    response_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "original name": {
                        "type": "string",
                    },
                    "variable name": {
                        "type": "string",
                    },
                },
                "required": ["variable name"],
            },
        }


    response = completion(
        model="gemini/gemini-1.5-pro", 
        messages=messages, 
        response_format={"type": "json_object", "response_schema": response_schema}
    )
    # print(response)

    answers = json.loads(response.choices[0].message.content)
    
    return answers

def get_newclass_func(code):
    class_funcs = {}
    if "from newClass" in code:
        for line in code.split("\n"):
            if "from newClass" in line and "import" in line:
                print(line)
                newclassname = line.split("from")[-1].split("import")[0].strip()
                func = line.split("as")[-1].strip()
                if newclassname not in class_funcs:
                    class_funcs[newclassname] = []
                class_funcs[newclassname].append(func)
    return class_funcs
    
def get_files(file_dir, dataset, tests_dir, new_dir):
    print(f"Working on {dataset}.")
    items = {}
    for dirpath, _, files in os.walk(file_dir):
        for file in files:
            if ".py-" in file:
                
                file_path = os.path.join(dirpath, file)
                code = read_file(file_path)
                print(file_path)
                ID = file.split(".py-")[0]
                print(f"Working on {ID}")
                if file not in items:
                    items[file] = {
                        "ID": ID,
                        "file": file,
                        "original_code": code,
                        "file_path": file_path,
                        "names": None,
                        "new_code": None,
                        "newclass_code":None,
                        "class_funcs": None
                    }
                class_funcs = get_newclass_func(code)
                vars_to_rename = extract_variables(code)
                
                print(f"vars_to_rename: {vars_to_rename}\nclass_funcs{class_funcs}")
                
                prompt = f"Can you generate new natural names for the following variables?\n{vars_to_rename}\n{code}"
                answers = generator_gemini(prompt)
                print(answers)
                
                vas_list = list(vars_to_rename)
                idx = 0
                for pair in answers:
                    if "original name" not in pair:
                        pair["original name"] = vas_list[idx]
                    idx += 1
                
                #process code
                for pair in answers:
                    code = replace_variable_in_statement(code, pair["original name"], pair["variable name"])
                print(code)
                utils.write_file(".tmp.py", code)
                
                items[file]["names"] = answers
                items[file]["class_funcs"] = class_funcs
                
                # process newclass code if exists
                if len(class_funcs) > 0:
                    for classname in class_funcs:
                        class_code = read_file(f"{dirpath}/{classname}.py")
                        new_class_code = class_code
                        for pair in answers:
                            if pair["original name"] in class_funcs[classname]:
                                new_class_code = replace_variable_in_statement(new_class_code, pair["original name"], pair["variable name"])
                    print(new_class_code)
                    utils.write_file(f".tmp_test/{classname}.py",new_class_code)
                    res = run_pytest(ID, ".tmp.py", tests_dir)
                    print(res)
                    if "tests_pass" in res:
                        print(f"{ID} pass after renaming!")
                        new_file = os.path.join(new_dir, file)
                        utils.write_file(new_file, code)
                        new_class_file = os.path.join(new_dir, f"{classname}.py")
                        utils.write_file(new_class_file, new_class_code)
                        
                        ID_file = os.path.join(new_dir, f"prompts/{ID}.py")
                        utils.write_file(ID_file, f"{code}\n\n#The following is code in dependent file {classname}.py:\n{new_class_code}")
                        items[file]["new_code"] = code
                        items[file]["newclass_code"] = new_class_code 
                        items[file]["prompt"] = f"{code}\nDependent file:\n{new_class_code}"
                    else:
                        print(f"{ID} fails after renaming!")
                        utils.write_file(new_file, items[file]["original_code"])
                        ID_file = os.path.join(new_dir, f"prompts/{ID}.py")
                        utils.write_file(ID_file, items[file]["original_code"])
                        
                        new_class_file = os.path.join(new_dir, f"{classname}.py")
                        utils.write_file(new_class_file, class_code)
                        items[file]["new_code"] = items[file]["original_code"]
                        items[file]["newclass_code"] = class_code 
                        items[file]["prompt"] = f"{items[file]['original_code']}\nDependent file:\n{class_code}"
                else:
                    res = run_pytest(ID, ".tmp.py", tests_dir)
                    print(res)
                    if "tests_pass" in res:
                        print(f"{ID} pass after renaming!")
                        new_file = os.path.join(new_dir, file)
                        utils.write_file(new_file, code)
                        
                        ID_file = os.path.join(new_dir, f"prompts/{ID}.py")
                        utils.write_file(ID_file, code)
                        items[file]["new_code"] = code
                        items[file]["prompt"] = code
                    else:
                        print(f"{ID} fails after renaming")
                        
                        utils.write_file(new_file, items[file]["original_code"])
                        ID_file = os.path.join(new_dir, f"prompts/{ID}.py")
                        utils.write_file(ID_file, items[file]["original_code"])
                        items[file]["prompt"] = items[file]["original_code"]
                        items[file]["new_code"] = items[file]["original_code"]
                

                # exit(0)
                # time.sleep(10)
    utils.write_json(f"renamed_jsons/{dataset}_renaming.json", items)


if __name__ == "__main__":
    args = sys.argv[1:]
    file_dir = args[0]
    dataset = args[1]
    tests_dir = args[2]
    new_dir = args[3]
    os.makedirs(new_dir, exist_ok = True)
    os.makedirs(new_dir + "/prompts", exist_ok = True)
    get_files(file_dir, dataset, tests_dir, new_dir)
    # generator_gemini("write a python code to calculate a + b")