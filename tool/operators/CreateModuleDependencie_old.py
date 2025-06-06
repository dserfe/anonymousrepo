import ast
import os
import random
import utils

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name:
                self.imports.append(alias.name)
            if alias.asname:
                self.imports.append(alias.asname)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name:
                self.imports.append(alias.name)
            if alias.asname:
                self.imports.append(alias.asname)
        self.generic_visit(node)

class RemoveFunctionTransformer(ast.NodeTransformer):
    def __init__(self, function_names_to_remove):
        self.function_names_to_remove = function_names_to_remove

    def visit_FunctionDef(self, node):
        if node.name in self.function_names_to_remove:
            return None
        return self.generic_visit(node)
        # node.body.insert(0, ast.Expr(value=ast.Str(s=f'# {node.name} moved to a new class to create intra-dependencies.')))
        # return node

def move_functions_into_new_class(python_code, applicable_rules, target_file):
    root = ast.parse(python_code)

    imports = utils.get_imports(root)
    visitor = ImportVisitor()
    visitor.visit(root)
    import_names = visitor.imports
    funcDefs = [node for node in ast.walk(root) if isinstance(node, ast.FunctionDef)]

    # for node in ast.iter_child_nodes(root):
    #     if isinstance(node, ast.Assign) or isinstance(node, ast.Expr):
    #         # print(node)
    #         print(ast.unparse(node))
    # exit(0)
    idx = 0
    if len(funcDefs):
        for func_node in funcDefs:
            if idx > 1:
                break
            new_tree = ast.Module(body=imports + func_node, type_ignores=[])
            new_code = ast.unparse(new_tree)
            if "/" in target_file:
                dir = target_file.split("/")[0]
            else:
                dir = ""
            id = str(random.randint(2, 1000))
            newClassName = os.path.join(dir,"newClass" + id +".py")
            newModule = "newClass" + id
            idx += 1
            utils.write_file(newClassName, new_code)
            new_imports = []
            if func_node.name in import_names:
                continue
            import_node = utils.create_importFrom(newModule, func_node.name, func_node.name, 0)
            # import_node = ast.ImportFrom(
            #     module= newModule,
            #     names=[ast.alias(name=func_node.name, asname=func_node.name)],
            #     level=0  # level=0 for absolute import, level=1 for relative import (e.g., .module)
            # )
            new_imports.append(import_node)
            transformer = RemoveFunctionTransformer(func_node.name)
            root = transformer.visit(root)
            applicable_rules.append("move_functions_into_new_class")
            break
        root.body.insert(0, new_imports)

    update_content = ast.unparse(root)
    # print(update_content)
    # exit(0)
    return update_content, applicable_rules

def init(python_code, applicable_rules, target_file):
    update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
    return update_content, applicable_rules