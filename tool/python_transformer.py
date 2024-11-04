import ast
# import crossover
import complexity
import copy
import difflib
# import explore_fitness
import numpy as np
import itertools
import json
import os
import pprint
import random
import string
import signal
import shutil
import time
import operators.AprChangeArithOp
import utils
import unrelatedLibraries
import operators.AddBase64
import operators.AddCrypto
import operators.AddDatetime
import operators.AddDateutil
import operators.AddElseToFor
import operators.AddElseToWhile
import operators.AddNestedIf
import operators.AddNestedForInside
import operators.AddNestedForOutside
import operators.AddNestedWhileInside
import operators.AddNestedWhileOutside
import operators.AddNestedList
import operators.AddThread
import operators.AddTime
import operators.AddTryExceptInsideFunctions
import operators.AddTryExceptOutsideFunctions
import operators.ChangeAugment
import operators.ChangeFunctionNames
import operators.ChangeVarNames
import operators.CreateFunctions
import operators.CreateModuleDependencies
import operators.LocalVarToGlobalVar
import operators.ReplaceWithNumpy
import operators.AddScipy
import operators.AddSklearn
import operators.AddHttp
import operators.IntroduceConfusingVars
import operators.TransformLoopToRecursion
import operators.TransformFunctionToClass
import operators.AddDecorator
import operators.AprChangeArithOp
import operators.AprChangeCompareOp
import operators.AprChangeConditionOp
import operators.AprChangeReturn
import operators.AprChangeType
import statistics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import TextColor

#targets
#target_readability = {"num_tokens": 5037.84, "lines_of_code": 401.33, "num_conditions": 44.65, "num_loops": 11.54, "num_assignments": 88.94, "num_max_nested_loop": 1.23, "num_max_nested_if": 3.22, "num_max_conditions_in_if": 2.16, "max_line_tokens": 30.24, "num_of_variables": 44.42, "num_of_arrays": 12.92, "num_of_operators": 77.52,  "num_of_nested_casting": 1.19, "entropy": 6.96}  
target_readability = {"num_tokens": 5038, "lines_of_code": 402, "num_conditions": 45, "num_loops": 12, "num_assignments": 89, "num_max_nested_loop": 2, "num_max_nested_if": 4, "num_max_conditions_in_if": 3, "max_line_tokens": 31, "num_of_variables": 45, "num_of_arrays": 13, "num_of_operators": 78,  "num_of_nested_casting": 2, "entropy": 7}  
target_complexity = {"Base complexity": 66.29, "Predicates with operators": 25.59, "Nested levels": 20.73, "Complex code structures": 30.44, "Third-Party calls": 18.11, "Inter_dependencies": 19.86, "Intra_dependencies": 15.22} 

def add_thread(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddThread.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def transform_localVar_to_globalVar(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.LocalVarToGlobalVar.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def move_functions_into_new_class(python_code, applicable_rules, target_file):
    try:
        update_content, applicable_rules = operators.CreateModuleDependencies.init(python_code, applicable_rules, target_file)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def create_functions(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.CreateFunctions.init(python_code, applicable_rules)
        return update_content, applicable_rules 
    except:
        return python_code, applicable_rules

def changing_AugAssign(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.ChangeAugment.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def change_function_names(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.ChangeFunctionNames.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def replace_with_numpy(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.ReplaceWithNumpy.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def add_datetime(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddDatetime.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_time(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddTime.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def add_crypto(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddCrypto.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def add_sklearn(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddSklearn.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def add_http(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddHttp.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_scipy(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddScipy.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def add_base64(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddBase64.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_dateutil(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddDateutil.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def introduce_confusing_vars(python_code, applicable_rules, max_num):
    try:
        update_content, applicable_rules = operators.IntroduceConfusingVars.init(python_code, applicable_rules, max_num)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def transform_range_to_recursion(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.TransformLoopToRecursion.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules
    
def transform_function_to_class(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.TransformFunctionToClass.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules 

def add_nested_if(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedIf.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_nested_for_in(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedForInside.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_nested_for_out(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedForOutside.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_nested_while_out(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedWhileOutside.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_nested_while_in(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedWhileInside.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_else_to_for(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddElseToFor.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_else_to_while(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddElseToWhile.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_nested_list(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddNestedList.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_try_except_outside_functions(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddTryExceptOutsideFunctions.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_try_except_inside_functions(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddTryExceptInsideFunctions.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def add_decorator(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AddDecorator.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def change_var_names(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.ChangeVarNames.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def apr_change_arith_op(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AprChangeArithOp.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def apr_change_compare_op(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AprChangeCompareOp.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def apr_change_condition_op(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AprChangeConditionOp.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def apr_change_type(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AprChangeType.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def apr_change_return(python_code, applicable_rules):
    try:
        update_content, applicable_rules = operators.AprChangeReturn.init(python_code, applicable_rules)
        return update_content, applicable_rules
    except:
        return python_code, applicable_rules

def transformation_single_rule(source_file, rule, applicable_rules, target_file):
    python_code = utils.read_file(source_file)
    if rule == "changing_AugAssign":
        update_content, applicable_rules = changing_AugAssign(python_code, applicable_rules)
    elif rule == "add_nested_for_in":
        update_content, applicable_rules = add_nested_for_in(python_code, applicable_rules)
    elif rule == "add_nested_for_out":
        update_content, applicable_rules = add_nested_for_out(python_code, applicable_rules)    
    elif rule == "add_nested_while_out":
        update_content, applicable_rules = add_nested_while_out(python_code, applicable_rules)
    elif rule == "add_nested_while_in":
        update_content, applicable_rules = add_nested_while_in(python_code, applicable_rules)
    elif rule == "add_nested_if":
        update_content, applicable_rules = add_nested_if(python_code, applicable_rules)
    elif rule == "create_functions":
        update_content, applicable_rules = create_functions(python_code, applicable_rules)
    elif rule == "add_try_except_inside_functions":
        update_content, applicable_rules = add_try_except_inside_functions(python_code, applicable_rules)
    elif rule == "add_try_except_outside_functions":
        update_content, applicable_rules = add_try_except_outside_functions(python_code, applicable_rules)
    elif rule == "add_else_to_for":
        update_content, applicable_rules = add_else_to_for(python_code, applicable_rules)
    elif rule == "add_else_to_while":
        update_content, applicable_rules = add_else_to_while(python_code, applicable_rules)
    elif rule == "move_functions_into_new_class":
        update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
    elif rule == "introduce_confusing_vars":
        update_content, applicable_rules = introduce_confusing_vars(python_code, applicable_rules, max_num = 1)
    elif rule == "change_function_names":
        update_content, applicable_rules = change_function_names(python_code, applicable_rules)
    elif rule == "add_nested_list":
        update_content, applicable_rules = add_nested_list(python_code, applicable_rules)
    elif rule == "replace_with_numpy":
        update_content, applicable_rules = replace_with_numpy(python_code, applicable_rules)
    elif rule == "add_datetime":
        update_content, applicable_rules = add_datetime(python_code, applicable_rules)
    elif rule == "add_time":
        update_content, applicable_rules = add_time(python_code, applicable_rules)
    elif rule == "add_crypto":
        update_content, applicable_rules = add_crypto(python_code, applicable_rules)
    elif rule == "add_sklearn":
        update_content, applicable_rules = add_sklearn(python_code, applicable_rules)
    elif rule == "add_http":
        update_content, applicable_rules = add_http(python_code, applicable_rules)
    elif rule == "add_scipy":
        update_content, applicable_rules = add_scipy(python_code, applicable_rules)
    elif rule == "add_base64":
        update_content, applicable_rules = add_base64(python_code, applicable_rules)
    elif rule == "add_dateutil":
        update_content, applicable_rules = add_dateutil(python_code, applicable_rules)
    elif rule == "transform_range_to_recursion":
        update_content, applicable_rules = transform_range_to_recursion(python_code, applicable_rules)
    elif rule == "transform_function_to_class":
        update_content, applicable_rules = transform_function_to_class(python_code, applicable_rules)        
    elif rule == "add_thread":
        update_content, applicable_rules = add_thread(python_code, applicable_rules)
    elif rule == "transform_localVar_to_globalVar":
        update_content, applicable_rules = transform_localVar_to_globalVar(python_code, applicable_rules)
    elif rule == "add_decorator":
        update_content, applicable_rules = add_decorator(python_code, applicable_rules)
    elif rule == "change_var_names":
        update_content, applicable_rules = change_var_names(python_code, applicable_rules)
    elif rule == "apr_change_arith_op":
        update_content, applicable_rules = apr_change_arith_op(python_code, applicable_rules)  
    elif rule == "apr_change_compare_op":
        update_content, applicable_rules = apr_change_compare_op(python_code, applicable_rules) 
    elif rule == "apr_change_condition_op":
        update_content, applicable_rules = apr_change_condition_op(python_code, applicable_rules)   
    elif rule == "apr_change_type":
        update_content, applicable_rules = apr_change_type(python_code, applicable_rules)   
    elif rule == "apr_change_return":
        update_content, applicable_rules = apr_change_return(python_code, applicable_rules)  
    else:
        raise "Operator Not Supported"
    return update_content, applicable_rules

def get_applicable_rules_complexity_non_changing(source_file, target_file = None):
    python_code = utils.read_file(source_file)
    applicable_rules = []
    try:
        update_content, applicable_rules = changing_AugAssign(python_code, applicable_rules)
        # update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
        update_content, applicable_rules = change_function_names(python_code, applicable_rules)
        update_content, applicable_rules = change_var_names(python_code, applicable_rules)
        # update_content, applicable_rules = introduce_confusing_vars(python_code, applicable_rules, max_num = 1)
    except:
        pass
    random_seed = np.random.randint(0, 2**32 - 1)
    random.seed(random_seed)
    random_rule = None
    if len(applicable_rules):
        random_rule = random.choice(applicable_rules)
    return random_rule, random_seed

def get_applicable_apr(source_file, target_file = None):
    python_code = utils.read_file(source_file)
    applicable_rules = []
    try:
        update_content, applicable_rules = apr_change_arith_op(python_code, applicable_rules)
        update_content, applicable_rules = apr_change_compare_op(python_code, applicable_rules)
        update_content, applicable_rules = apr_change_condition_op(python_code, applicable_rules)
        update_content, applicable_rules = apr_change_type(python_code, applicable_rules)
        update_content, applicable_rules = apr_change_return(python_code, applicable_rules)
        update_content, applicable_rules = changing_AugAssign(python_code, applicable_rules)
        # update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
        update_content, applicable_rules = change_function_names(python_code, applicable_rules)
        update_content, applicable_rules = change_var_names(python_code, applicable_rules)
        update_content, applicable_rules = introduce_confusing_vars(python_code, applicable_rules, max_num = 1)
    except:
        pass
    
    random_seed = np.random.randint(0, 2**32 - 1)
    random.seed(random_seed)
    random_rule = None
    if len(applicable_rules):
        random_rule = random.choice(applicable_rules)
    return random_rule, random_seed

def get_all_apr_rules(source_file, target_file = None):
    python_code = utils.read_file(source_file)
    applicable_rules = []
    update_content, applicable_rules = apr_change_arith_op(python_code, applicable_rules)
    update_content, applicable_rules = apr_change_compare_op(python_code, applicable_rules)
    update_content, applicable_rules = apr_change_condition_op(python_code, applicable_rules)
    update_content, applicable_rules = apr_change_return(python_code, applicable_rules)
    update_content, applicable_rules = apr_change_type(python_code, applicable_rules)
    
    return applicable_rules

def get_applicable_rules(source_file, target_file=None):
    python_code = utils.read_file(source_file)
    applicable_rules = []
    try:
        update_content, applicable_rules = add_nested_for_out(python_code, applicable_rules)    
        update_content, applicable_rules = add_nested_while_out(python_code, applicable_rules)
        update_content, applicable_rules = add_nested_if(python_code, applicable_rules)
        update_content, applicable_rules = create_functions(python_code, applicable_rules)
        update_content, applicable_rules = add_try_except_inside_functions(python_code, applicable_rules)
        update_content, applicable_rules = add_else_to_for(python_code, applicable_rules)
        update_content, applicable_rules = add_else_to_while(python_code, applicable_rules)
        update_content, applicable_rules = add_nested_list(python_code, applicable_rules)
        update_content, applicable_rules = transform_range_to_recursion(python_code, applicable_rules)
        update_content, applicable_rules = transform_function_to_class(python_code, applicable_rules)
        update_content, applicable_rules = add_thread(python_code, applicable_rules)
        update_content, applicable_rules = add_decorator(python_code, applicable_rules)
        update_content, applicable_rules = replace_with_numpy(python_code, applicable_rules)
        update_content, applicable_rules = add_datetime(python_code, applicable_rules)
        update_content, applicable_rules = add_time(python_code, applicable_rules)
        update_content, applicable_rules = add_crypto(python_code, applicable_rules)
        update_content, applicable_rules = add_sklearn(python_code, applicable_rules)
        update_content, applicable_rules = add_http(python_code, applicable_rules)
        update_content, applicable_rules = add_scipy(python_code, applicable_rules)
        update_content, applicable_rules = add_base64(python_code, applicable_rules)
        update_content, applicable_rules = add_dateutil(python_code, applicable_rules)

        # test_content, test_rules = change_function_names(python_code, [])
        # if "change_function_names" in test_rules:
        #     applicable_rules.append("move_functions_into_new_class")
        update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
        # update_content, applicable_rules = change_function_names(python_code, applicable_rules)
        # update_content, applicable_rules = change_var_names(python_code, applicable_rules)
        # update_content, applicable_rules = introduce_confusing_vars(python_code, applicable_rules, max_num = 1)
        
        #others
        # update_content, applicable_rules = add_nested_for_in(python_code, applicable_rules)
        # update_content, applicable_rules = add_nested_while_in(python_code, applicable_rules)
        # update_content, applicable_rules = add_if_inside_functions(python_code, applicable_rules)
        # update_content, applicable_rules = flip_if_branches(python_code, applicable_rules)
        # update_content, applicable_rules = add_try_except_outside_functions(python_code, applicable_rules)
        # update_content, applicable_rules = transform_localVar_to_globalVar(python_code, applicable_rules)
    except:
        pass
    return applicable_rules

def get_relative_metrics(individuals):
    updated_individuals = utils.get_relative_readability(individuals)
    updated_individuals = utils.get_relative_complexity(updated_individuals)
    return updated_individuals

def generate_new_node(variant_file, applicable_rules, applied_rules, complexity, readability, relevant_distance_readability, relevant_distance_complexity):
    return {
        "variant_file": variant_file, 
        "applicable_rules": applicable_rules, 
        "applied_rules": applied_rules, 
        "complexity": complexity, 
        "readability": readability, 
        "relevant_distance_readability": relevant_distance_readability,
        "relevant_distance_complexity": relevant_distance_complexity
       }

def initialize_csv(headers, csv_file):
    utils.write_header_csv(csv_file, headers)
    return csv_file

def filter_individuals(new_individuals):
    selection = [new_individuals[individual] for individual in new_individuals if new_individuals[individual]["relative_readability"] >= 0]
    return selection
    
def apply_multiple_rules(source_file, target_file, all_rules):
    applicable_rules = []
    for rule in all_rules:
        update_content, applicable_rules = transformation_single_rule(source_file, rule, applicable_rules, target_file)
        utils.write_file(target_file, update_content)
        source_file = target_file
    return target_file

def non_dominated_sorting(points):
    num_points = len(points)
    domination_counts = np.zeros(num_points, dtype=int)
    dominated_points = [[] for _ in range(num_points)]
    fronts = [[]]

    # First, identify all the points each point dominates and by how many points it is dominated
    for i in range(num_points):
        for j in range(num_points):
            if all(points[i] <= points[j]) and any(points[i] < points[j]):
                dominated_points[j].append(i)
                domination_counts[i] += 1
            elif all(points[j] <= points[i]) and any(points[j] < points[i]):
                dominated_points[i].append(j)
                domination_counts[j] += 1

    # Points that are not dominated by any other point are added to the first front
    current_front = [i for i in range(num_points) if domination_counts[i] == 0]
    fronts.append(current_front)

    # Remove dominated points from consideration for the next front
    while current_front:
        next_front = []
        for i in current_front:
            for j in dominated_points[i]:
                domination_counts[j] -= 1
                # If j is no longer dominated by any other points, add it to the next front
                if domination_counts[j] == 0:
                    next_front.append(j)
        fronts.append(next_front)
        current_front = next_front

    return fronts[:-1]

def crowding_distance(points):
    num_points = len(points)
    if num_points == 0:
        return []
    
    distances = np.zeros(num_points)
    sorted_indices = np.argsort(points, axis=0)
    
    # Ensure the boundary points are always selected
    distances[sorted_indices[0, :]] = np.inf
    distances[sorted_indices[-1, :]] = np.inf
    
    for i in range(1, num_points - 1): # each point
        for j in range(points.shape[1]): #  add the normalized distance between the neighboring points to the crowding distance of the current point
            distances[sorted_indices[i, j]] += (points[sorted_indices[i + 1, j], j] - points[sorted_indices[i - 1, j], j]) / (points[sorted_indices[-1, j], j] - points[sorted_indices[0, j], j])
            # computes the relative distance between the neighboring points 
    return distances

def get_statistics(final_set):
    if not final_set:
        return  {
            "avg_complexity": 0,
            "avg_readability": 0,
            "min_complexity": 0,
            "min_readability": 0,
            "max_complexity": 0,
            "max_readability": 0,
        }
    try:
        complexity_values = [item['relevant_distance_complexity'] for item in final_set]
        readability_values = [item['relevant_distance_readability'] for item in final_set]
        
        avg_complexity = sum(complexity_values) / len(complexity_values)
        avg_readability = sum(readability_values) / len(readability_values)
        min_complexity = min(complexity_values)
        min_readability = min(readability_values)
        max_complexity = max(complexity_values)
        max_readability = max(readability_values)
        
        result = {
            "avg_complexity": avg_complexity,
            "avg_readability": avg_readability,
            "min_complexity": min_complexity,
            "min_readability": min_readability,
            "max_complexity": max_complexity,
            "max_readability": max_readability,
        }
    
        return result
    except:
        return  {
            "avg_complexity": 0,
            "avg_readability": 0,
            "min_complexity": 0,
            "min_readability": 0,
            "max_complexity": 0,
            "max_readability": 0,
        }

def get_pareto_optimal_set(candidates, fraction = 0.2):

    complexity_values, readability_values, names = [], [], []
    for name in candidates:
        complexity_values.append(candidates[name]["relevant_distance_complexity"])
        readability_values.append(candidates[name]["relevant_distance_readability"])
        names.append(name)
            
    values = np.column_stack((complexity_values, readability_values))    
    fronts = non_dominated_sorting(values)
    selected_candidate_names = []

    num_candidates_to_select = round(len(candidates) * fraction)
    for front in fronts:
        if len(selected_candidate_names) >= num_candidates_to_select:
            break
        if len(front) > 1:
            distances = crowding_distance(values[front])
            front = [front[i] for i in np.argsort(-distances)]
        selected_candidate_names.extend([names[i] for i in front[:num_candidates_to_select - len(selected_candidate_names)]])

    # print(selected_candidate_names)
    return [candidates[name] for name in selected_candidate_names]

def get_final_pareto_optimal_set(candidates, fraction = 0.2):
    complexity_median = 0
    if len([candidates[name]["relevant_distance_complexity"] for name in candidates]) > 0:
        complexity_median = statistics.median([candidates[name]["relevant_distance_complexity"] for name in candidates])
    print("complexity_median", complexity_median)
    names_higher_than_median = []
    complexity_values, readability_values, names = [], [], []
    print("Candidates to select:")
    for name in candidates:
        print(name)
        complexity_values.append(candidates[name]["relevant_distance_complexity"])
        readability_values.append(candidates[name]["relevant_distance_readability"])
        names.append(name)
        
    # for name in candidates:
    #     if candidates[name]["relevant_distance_complexity"] >= complexity_median:
    #         complexity_values.append(candidates[name]["relevant_distance_complexity"])
    #         readability_values.append(candidates[name]["relevant_distance_readability"])
    #         names_higher_than_median.append(name)
            
    values = np.column_stack((complexity_values, readability_values))    
    fronts = non_dominated_sorting(values)
    selected_candidate_names = []

    print("fronts:", fronts)
    num_candidates_to_select = round(len(candidates) * fraction)
    if num_candidates_to_select < 1 and len(candidates) > 0:
        num_candidates_to_select = 1
        
    print("num_candidates_to_select", num_candidates_to_select)
    for front in fronts:
        # for i in front:
        #     item = names[i]
        #     print(i, item, candidates[item]["relevant_distance_complexity"], candidates[item]["relevant_distance_readability"], candidates[item]["applied_rules"])

        if len(selected_candidate_names) >= num_candidates_to_select:
            break
        if len(front) >= 1:
            sorted_indices = sorted(front, key=lambda i: candidates[names[i]]["relevant_distance_complexity"], reverse=True)
            # Select candidates based on sorted complexity within the front.
            for i in sorted_indices:
                if len(selected_candidate_names) >= num_candidates_to_select:
                    break
                item = names[i]
                if candidates[item]["relevant_distance_complexity"] < complexity_median:
                    print(f"{candidates[item]['relevant_distance_complexity']} is less than {complexity_median}!")
                    continue
                print(f"{i}, {item}, Complexity: {candidates[item]['relevant_distance_complexity']}, Readability: {candidates[item]['relevant_distance_readability']}, Rules: {candidates[item]['applied_rules']}")
                selected_candidate_names.append(item)
            if len(selected_candidate_names) > 0:
                break

    return [candidates[name] for name in selected_candidate_names]


def get_pareto_optimal_set_relative(candidates, num_candidates_to_select):
    names = list(candidates.keys())
    complexity_values = np.array([candidates[name]["relevant_distance_complexity"] for name in candidates])
    readability_values = np.array([candidates[name]["relevant_distance_readability"] for name in candidates])
    values = np.column_stack((complexity_values, readability_values))    
    fronts = non_dominated_sorting(values)
    selected_candidate_names = []

    for front in fronts:
        if len(selected_candidate_names) >= num_candidates_to_select:
            break
        if len(front) > 1:
            distances = crowding_distance(values[front])
            front = [front[i] for i in np.argsort(-distances)]
        selected_candidate_names.extend([names[i] for i in front[:num_candidates_to_select - len(selected_candidate_names)]])

    return [candidates[name] for name in selected_candidate_names]


def initialize(source_file, single_rule, genetic_algorithm, target_file, num_candidates_to_select, file_id = None, evaluation_tests_dir = None, apr=False):
    applicable_rules = []
    if genetic_algorithm:
        update_content, applicable_rules = transformation_ga(source_file, applicable_rules, target_file, num_candidates_to_select, csv_file, apr)
    elif single_rule:
        update_content, applicable_rules = transformation_single_rule(source_file, single_rule, applicable_rules, target_file)
    else:
        print("Apply all rules on a single file.")
        update_content, applicable_rules = transformation_all_applicable_rules(source_file, applicable_rules, target_file, file_id, evaluation_tests_dir)
    return update_content, applicable_rules

def check_tests(rule, applicable_rules, update_content_rec, file_id, evaluation_tests_dir, update_content):
    tmp_compilation_file = "tmp_compilation.py" + file_id
    if evaluation_tests_dir:
        if rule in applicable_rules:
            print(f"Checking transformation {rule}")
            utils.write_file(tmp_compilation_file, update_content_rec)
            recursion_result = complexity.run_pytest(file_id, tmp_compilation_file, evaluation_tests_dir)
            if "tests_pass" in str(recursion_result):
                update_content = update_content_rec
                return update_content, applicable_rules
            else:
                print(f"Drop {rule} due to {recursion_result}")
                update_content = update_content
                applicable_rules.remove(rule)
                return update_content, applicable_rules
        else:
            return update_content, applicable_rules
    else:
        print("No evaluation_tests_dir")
        return update_content_rec, applicable_rules

def check_tests_results(rule, applicable_rules, update_content_rec, file_id, evaluation_tests_dir, update_content):
    tmp_compilation_file = "tmp_compilation.py" + file_id
    if evaluation_tests_dir:
        if rule in applicable_rules:
            print(f"Checking transformation {rule}")
            utils.write_file(tmp_compilation_file, update_content_rec)
            recursion_result = complexity.run_pytest(file_id, tmp_compilation_file, evaluation_tests_dir)
            if "tests_pass" in str(recursion_result):
                return True
            else:
                return False
        else:
            return False
    else:
        raise ValueError("No tests provided.")
    

def transformation_all_applicable_rules(source_file, applicable_rules, target_file, file_id = None, evaluation_tests_dir = None):
    python_code = utils.read_file(source_file)
    applicable_rules = []
    try:
        update_content, applicable_rules = change_var_names(python_code, applicable_rules)
        
        update_content_nestedfor, applicable_rules = add_nested_for_out(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_nested_for_out", applicable_rules, update_content_nestedfor, file_id, evaluation_tests_dir, update_content)
         
        update_content_nestedwhile, applicable_rules = add_nested_while_out(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_nested_while_out", applicable_rules, update_content_nestedwhile, file_id, evaluation_tests_dir, update_content)
        
        update_content_nestedif, applicable_rules = add_nested_if(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_nested_if", applicable_rules, update_content_nestedif, file_id, evaluation_tests_dir, update_content)

        update_content, applicable_rules = add_try_except_inside_functions(update_content, applicable_rules)
        update_content, applicable_rules = add_else_to_for(update_content, applicable_rules)
        update_content, applicable_rules = add_else_to_while(update_content, applicable_rules)
        
        update_content_nestedlist, applicable_rules = add_nested_list(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_nested_list", applicable_rules, update_content_nestedlist, file_id, evaluation_tests_dir, update_content)

        update_content_rec, applicable_rules = transform_range_to_recursion(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("transform_range_to_recursion", applicable_rules, update_content_rec, file_id, evaluation_tests_dir, update_content)
                    
        update_content_thread, applicable_rules = add_thread(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_thread", applicable_rules, update_content_thread, file_id, evaluation_tests_dir, update_content)

        update_content_numpy, applicable_rules = replace_with_numpy(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("replace_with_numpy", applicable_rules, update_content_numpy, file_id, evaluation_tests_dir, update_content)

        update_content_datetime, applicable_rules = add_datetime(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_datetime", applicable_rules, update_content_datetime, file_id, evaluation_tests_dir, update_content)

        
        update_content_time, applicable_rules = add_time(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_time", applicable_rules, update_content_time, file_id, evaluation_tests_dir, update_content)

        update_content, applicable_rules = add_crypto(update_content, applicable_rules)
        update_content, applicable_rules = add_sklearn(update_content, applicable_rules)
        
        update_content_func, applicable_rules = create_functions(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("create_functions", applicable_rules, update_content_func, file_id, evaluation_tests_dir, update_content)
   
        update_content_dec, applicable_rules = add_decorator(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_decorator", applicable_rules, update_content_dec, file_id, evaluation_tests_dir, update_content)

        if "atcoder" in file_id or "codeforces" in file_id:
            update_content_funcname, applicable_rules = change_function_names(update_content, applicable_rules)
            update_content, applicable_rules = check_tests("change_function_names", applicable_rules, update_content_funcname, file_id, evaluation_tests_dir, update_content)

        update_content_http, applicable_rules = add_http(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_http", applicable_rules, update_content_http, file_id, evaluation_tests_dir, update_content)

        update_content_scipy, applicable_rules = add_scipy(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_scipy", applicable_rules, update_content_scipy, file_id, evaluation_tests_dir, update_content)

        update_content_base64, applicable_rules = add_base64(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_base64", applicable_rules, update_content_base64, file_id, evaluation_tests_dir, update_content)

        update_content_dateutil, applicable_rules = add_dateutil(update_content, applicable_rules)
        update_content, applicable_rules = check_tests("add_dateutil", applicable_rules, update_content_dateutil, file_id, evaluation_tests_dir, update_content)

        # update_content_newclass, applicable_rules = move_functions_into_new_class(update_content, applicable_rules, target_file)
        # update_content, applicable_rules = check_tests("move_functions_into_new_class", applicable_rules, update_content_newclass, file_id, evaluation_tests_dir, update_content)

        update_content, applicable_rules = changing_AugAssign(update_content, applicable_rules)

    except:
        pass
    return update_content, applicable_rules

        #others
        # update_content, applicable_rules = move_functions_into_new_class(python_code, applicable_rules, target_file)
        # update_content, applicable_rules = introduce_confusing_vars(python_code, applicable_rules, max_num = 1)
        # update_content, applicable_rules = add_nested_for_in(python_code, applicable_rules)
        # update_content, applicable_rules = add_nested_while_in(python_code, applicable_rules)
        # update_content, applicable_rules = add_if_inside_functions(python_code, applicable_rules)
        # update_content, applicable_rules = flip_if_branches(python_code, applicable_rules)
        # update_content, applicable_rules = add_try_except_outside_functions(python_code, applicable_rules)
        # update_content, applicable_rules = transform_localVar_to_globalVar(python_code, applicable_rules)


def initialize_whole_benchmark(files_to_transform, genetic_algorithm, evaluation_tests_dir, csv_file, time_budget, apr=False):
    if genetic_algorithm and files_to_transform:
        ga_whole_benchmark(files_to_transform, evaluation_tests_dir, time_budget, csv_file, apr)
        

class DocstringRemover(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant)):
            del node.body[0]
        self.generic_visit(node)
        return node

def remove_docstrings(source_code):
    tree = ast.parse(source_code)
    
    remover = DocstringRemover()
    new_tree = remover.visit(tree)
    
    new_code = ast.unparse(new_tree)
    return new_code
        
def compare_files_difflib(file1_path, file2_path):
    file1_text = ast.unparse(ast.parse(remove_docstrings(utils.read_file(file1_path)))).split("\n")
    file2_text = ast.unparse(ast.parse(remove_docstrings(utils.read_file(file2_path)))).split("\n")

    differ = difflib.Differ()
    # diff = differ.compare(file1_text, file2_text)
    diff = list(differ.compare(file1_text, file2_text))
    
    for d in diff:
        print(d)

    diff_dict = {}
    old_line = None

    for line in diff:
        if line.startswith('-'):
            old_line = line[2:].strip()
        elif line.startswith('+') and old_line:
            new_line = line[2:].strip()
            diff_dict[old_line] = new_line
            old_line = None  # Reset old_line
    return diff_dict

def get_diff(original_file, new_file):
    diff_dict = compare_files_difflib(original_file, new_file)
    return diff_dict
        
def inject_bugs(files_to_transform, evaluation_tests_dir, json_file, target_dir):  
    tmp_dir = target_dir  
    results = {}
    for file in files_to_transform:
        name_seed = utils.generate_sha(file)
        target_file = f"{tmp_dir}/{file.split('/')[-1].split('-')[0]}-{name_seed}" 
        applicale_apr_rules = get_all_apr_rules(file)
        target_file = apply_multiple_rules(file, target_file, applicale_apr_rules)
        print(target_file)
        diff_dict = get_diff(file, target_file)
        if file not in results:
            results[file] = {
                "target_file": target_file,
                "diff": diff_dict,
                "applicale_apr_rules": applicale_apr_rules,
            }
    # print(results)
    utils.write_json(json_file, results)
    return json_file
    
def generate_random_string(length = 10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def delete_file_if_exists(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def setup_file_info(file_id, file_path, time_budget):
    return {
            "file_id": file_id,
            "original_file": file_path,
            "time_per_iteration": {},
            "used_time": 0,
            "stop_rules": [],
            "unchanged_generations": 0,
            "time_limit": time_budget,
            "previous_pareto_set": set(),
            "potential_individuals": {},
            "rule_sequence_pool": [],
            "current_pareto_set_relative": {},
            "uniq_rules_per_iteration": {},
            "uniq_rules_all_iterations": [],
            "applied_rules": [],
            "result_initialization": False,
            "final_transformations": [],
            "iterations": 0,
            "all_files_per_iteration": {},
            "selected_files_per_iteration": {},
            "termination_reason": None,
    }

def ga_whole_benchmark(files_to_transform, evaluation_tests_dir, time_budget, csv_file, apr=False):
    target_metric = generate_new_node("target", [], [], target_complexity, target_readability, 1, 1)
    
    programs_to_transform = files_to_transform
    program_id_to_transform = [file.split(".py")[0].split("/")[-1] for file in files_to_transform]
    programs_evolution = {} # to save evolution results for each file per iteration
    iteration_individuals = {0: [], } # programs generated per iteration
    all_individuals = {0: [], }
    individuals = {} # all individuals with their details
    all_files_applied_rules = {} # a json file to record what rules applied for each file
    iterations = 0
    result_initialization = False
    
    tag = generate_random_string()
    json_dir = (evaluation_tests_dir.split("/")[-1] \
        if evaluation_tests_dir.split("/")[-1] != "" else evaluation_tests_dir.split("/")[-2]) \
            + f"{tag}_results"
    os.makedirs(f"{json_dir}", exist_ok=True)
    os.makedirs(f"{json_dir}/jsons", exist_ok=True)
    os.makedirs(f"{json_dir}/.tmp/", exist_ok=True)
    print(f"Json files saved at {json_dir}.")
    
    budget = time_budget #86400 #seconds
    
    for file_path in programs_to_transform:
        try:
        # if True:
            file_id = file_path.split(".py")[0].split("/")[-1]
            if file_id not in programs_evolution:
                programs_evolution[file_id] = setup_file_info(file_id, file_path, time_budget)
                
            # initialization of all initial programs
            if file_path not in individuals: 
                initial_rules = get_applicable_rules(file_path, f"{json_dir}/.tmp/")
                initial_complexity = utils.get_complexity(file_path, "initial", f"{file_path}_initial_complexity.csv")
                initial_readability = utils.get_readability(file_path)
                initial_relevant_distance_readability = utils.relevant_distance_readability(target_readability, initial_readability)
                initial_relevant_distance_complexity = utils.relevant_distance_complexity(target_complexity, initial_complexity)
                initial_node = generate_new_node(file_path, initial_rules, [], initial_complexity, initial_readability, initial_relevant_distance_readability, initial_relevant_distance_complexity)
                individuals[file_path] = initial_node
                print(f"Initial file: {file_path}, relevant_distance_readability: {initial_relevant_distance_readability}, relevant_distance_complexity: {initial_relevant_distance_complexity}")
                print(f"Initial rules (changing complexity) {initial_rules}\n")
                if file_path not in iteration_individuals[0]:
                    iteration_individuals[0].append(file_path)
        except Exception as e:
            print(e, file_path)
            
    start_time = time.time()
    print(f'STARTING AT {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
    budget_limit = False
    
    while len(programs_to_transform) > 0: 
        if budget_limit:
            break
        if len(iteration_individuals[iterations]) == 0:
            print(f"iteration_individuals-{iterations} is empty!")
            break
        
        iterations += 1
        if iterations not in iteration_individuals:
            iteration_individuals[iterations] = []
        if iterations not in all_individuals:
            all_individuals[iterations] = []
        print(utils.color_print_line(f"Iteration {iterations}:")) # track of iterations
        print(utils.color_print_line(f"Files to work on: {len(iteration_individuals[iterations - 1])}"))
        print(iteration_individuals[iterations - 1])
        
        for variant_file in iteration_individuals[iterations - 1]: # for variant_file in last iteration:
            try:
            # if True:
                print(utils.color_print_line(variant_file))
                if variant_file == "target":
                    continue
                if variant_file not in all_files_applied_rules:
                    all_files_applied_rules[variant_file] = []
                iteration_rules = []
                new_individuals = {}
                program_id = variant_file.split(".py")[0].split("/")[-1]
                if program_id not in program_id_to_transform:
                    continue
                tmp_dir = os.path.join(f"{json_dir}/generations", variant_file.split("/")[-1].split(".py")[0])
                
                # Get applicable rules that are changing complexity
                applicable_rules = get_applicable_rules(variant_file, f"{json_dir}/.tmp/")
                original_applicable_rules = applicable_rules
                
                if iterations not in programs_evolution[program_id]["time_per_iteration"]:
                    programs_evolution[program_id]["time_per_iteration"][iterations] = {"start" : time.time(), "end": None}
                
                # Apply a rule that are changing complexity
                for rule in applicable_rules:
                    print(utils.color_print_line(f"Iteration {iterations}: {rule} {variant_file}"))
                    if rule in programs_evolution[program_id]["stop_rules"]:
                        print(f"{rule} is in stop_rules!")
                        continue
                    
                    to_exclude_rules = []
                    name_seed = utils.generate_sha(f"{variant_file}_{rule}")
                    new_file = f"{tmp_dir}/{variant_file.split('/')[-1].split('-')[0]}-{name_seed}"
                    if new_file not in all_files_applied_rules:
                        all_files_applied_rules[new_file] = []
                    try:
                        update_content, _ = transformation_single_rule(variant_file, rule, [], new_file)
                        print(utils.color_print_line("Applied:"), rule)
                        utils.write_file(new_file, update_content)
                    except:
                        print(f"{rule} will be dropped!")
                        continue
                    
                    all_files_applied_rules[new_file].extend(all_files_applied_rules[variant_file])
                    all_files_applied_rules[new_file].append(rule)
                    
                    applied_rules = all_files_applied_rules[new_file]
                    applicable_rules = get_applicable_rules(new_file, f"{json_dir}/.tmp/")
                    res = check_tests_results(rule, applied_rules, update_content, program_id, evaluation_tests_dir, update_content)
                    if not res:
                        print(f"Test Failure when running {rule}")
                        continue
                    
                    # remove redundant transformations
                    if sorted(applied_rules) in [sorted(rule_sequence) for rule_sequence in programs_evolution[program_id]["rule_sequence_pool"]]:
                        print(utils.color_print_line(f"redundant rules: {applied_rules}"))
                        continue
                    try:
                        new_complexity = utils.get_complexity(new_file, "tmp", "tmp.csv")
                        new_readability = utils.get_readability(new_file)
                        relevant_distance_readability = utils.relevant_distance_readability(target_readability, new_readability)
                        relevant_distance_complexity = utils.relevant_distance_complexity(target_complexity, new_complexity)
                    except Exception as e:
                        print("Error when processing metrics: " + e)
                        continue

                    to_exclude_rules, lower_feature = utils.readability_stopping(new_readability, target_readability)
                    programs_evolution[program_id]["stop_rules"].extend(to_exclude_rules)
                    
                    if len(to_exclude_rules) > 0 and rule in to_exclude_rules:
                        print(f"Drop {new_file} due to lower readability {lower_feature} when applying {rule}.")
                        new_file = variant_file
                        
                    new_file_backup = new_file
                    
                    # Apply a random_rule that are not changing complexity
                    if apr:
                        random_rule, random_seed = get_applicable_apr(new_file, None)
                    else:
                        random_rule, random_seed = get_applicable_rules_complexity_non_changing(new_file, None)

                    random_rule_applied = False
                    if random_rule != None:
                        try:
                            name_seed_with_random_rule = utils.generate_sha(f"{new_file}_{random_rule}")
                            new_file_with_random_rule = f"{tmp_dir}/{new_file.split('/')[-1].split('-')[0]}-{name_seed_with_random_rule}"                        
                            if new_file_with_random_rule not in all_files_applied_rules:
                                all_files_applied_rules[new_file_with_random_rule] = []
                            update_content, _ = transformation_single_rule(new_file, random_rule, [], new_file_with_random_rule)
                            utils.write_file(new_file_with_random_rule, update_content)
                            all_files_applied_rules[new_file_with_random_rule].extend(all_files_applied_rules[new_file])
                            all_files_applied_rules[new_file_with_random_rule].append(random_rule)
                            random_rule_applied = True
                            print(utils.color_print_line(f"Applied: {random_rule}, random_seed: {random_seed}"))
                        except:
                            pass
                    
                    if random_rule_applied:
                        new_file = new_file_with_random_rule                    
                        applied_rules = all_files_applied_rules[new_file]
                        applicable_rules = get_applicable_rules(new_file, f"{json_dir}/.tmp/")
                        if sorted(applied_rules) in [sorted(rule_sequence) for rule_sequence in programs_evolution[program_id]["rule_sequence_pool"]]:
                            print(utils.color_print_line(f"redundant rules: {applied_rules}"))
                            continue
                        res = check_tests_results(random_rule, applied_rules, update_content, program_id, evaluation_tests_dir, update_content)
                        if not res:
                            new_file = new_file_backup
                            applied_rules.remove(random_rule)
                            print(f"Revert to {new_file}!")
                            # continue
                        try:
                            new_complexity = utils.get_complexity(new_file, "tmp", "tmp.csv")
                            new_readability = utils.get_readability(new_file)
                            relevant_distance_readability = utils.relevant_distance_readability(target_readability, new_readability)
                            relevant_distance_complexity = utils.relevant_distance_complexity(target_complexity, new_complexity)
                        except Exception as e:
                            print("Error when processing metrics: " + e)
                            continue
                        to_exclude_rules, lower_feature = utils.readability_stopping(new_readability, target_readability)
                        programs_evolution[program_id]["stop_rules"].extend(to_exclude_rules)

                        if len(to_exclude_rules) > 0 and random_rule in to_exclude_rules:
                            print(f"Drop {new_file} due to lower readability {lower_feature} when applying {random_rule}.")
                            continue
                    
                    print("File: {}, readability: {}, complexity: {}, rules: {}".\
                        format(new_file, relevant_distance_readability, relevant_distance_complexity, applied_rules))
                    
                    new_variant = generate_new_node(new_file, applicable_rules, applied_rules, new_complexity, new_readability, relevant_distance_readability, relevant_distance_complexity)
                    
                    for rule in applied_rules:
                        if rule not in iteration_rules:
                            iteration_rules.append(rule)
                        if rule not in programs_evolution[program_id]["uniq_rules_all_iterations"]:
                            programs_evolution[program_id]["uniq_rules_all_iterations"].append(rule)
                    
                    new_individuals[new_file] = new_variant
                    individuals[new_file] = new_variant
                    programs_evolution[program_id]["rule_sequence_pool"].append(applied_rules)
                    if iterations not in programs_evolution[program_id]:
                        programs_evolution[program_id][iterations] = {}
                    all_individuals[iterations].append(new_file)
                    programs_evolution[program_id][iterations][new_file] = new_variant
                    programs_evolution[program_id]["iterations"] = iterations
                    
            except Exception as e:
                print(variant_file, e)
                continue
                
            # current file finished current iteration
            programs_evolution[program_id]["time_per_iteration"][iterations]["end"] = time.time()
            programs_evolution[program_id]["used_time"] = get_time_used(programs_evolution[program_id]["time_per_iteration"])
            if iterations not in programs_evolution[program_id]["uniq_rules_per_iteration"] and len(iteration_rules) > 0:
                programs_evolution[program_id]["uniq_rules_per_iteration"][iterations] = iteration_rules
            programs_evolution[program_id]["potential_individuals"].update(new_individuals)
            if iterations not in programs_evolution[program_id]["selected_files_per_iteration"]:
                programs_evolution[program_id]["selected_files_per_iteration"][iterations] = []

            # iteration_individuals[iterations].append(new_file) # TODO: fix this, not all files will go to next iteration
            variant_iteration_optimal_set = get_final_pareto_optimal_set(new_individuals)
            print(utils.color_print_line(f"** variant_iteration_optimal_set:"))
            for v in variant_iteration_optimal_set:
                item = v["variant_file"]
                print(f"{item}, readability: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_readability']}, complexity: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_complexity']}, applied: {all_files_applied_rules[item]}")
                iteration_individuals[iterations].append(item)
                programs_evolution[program_id]["selected_files_per_iteration"][iterations].append(item)

            
            print(utils.color_print_line(f"** {program_id} potential_individuals:"))
            print(len(programs_evolution[program_id]["potential_individuals"]))
            if iterations not in programs_evolution[program_id]:
                print(programs_to_transform)
                print(programs_evolution[program_id]["original_file"])
                if programs_evolution[program_id]["original_file"] in programs_to_transform:
                    programs_to_transform.remove(programs_evolution[program_id]["original_file"])
                if program_id in program_id_to_transform:
                    program_id_to_transform.remove(program_id)
                programs_evolution[program_id]["termination_reason"] = f"no new transformations at Iteration {iterations}"
                result_initialization = summary(program_id, programs_evolution, individuals, result_initialization, csv_file, json_dir, all_files_applied_rules, evaluation_tests_dir)
            else:
                if iterations not in programs_evolution[program_id]["all_files_per_iteration"]:
                    programs_evolution[program_id]["all_files_per_iteration"][iterations] = programs_evolution[program_id][iterations]
                
            
            for item in programs_evolution[program_id]["potential_individuals"]:
                print(f"{item}, readability: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_readability']}, complexity: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_complexity']}, applied: {all_files_applied_rules[item]}")
            
        # non-dominated sorting and crowding distance calculation
        
        for program_id in programs_evolution:
            print(program_id)
            
            relative_fronts = get_pareto_optimal_set(programs_evolution[program_id]["potential_individuals"])
            programs_evolution[program_id]["current_pareto_set_relative"] = {(v["variant_file"]) for v in relative_fronts}  
            
            print(utils.color_print_line("** current_pareto_set:"))
            for item in programs_evolution[program_id]["current_pareto_set_relative"]:
                print(f"{item}, readability: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_readability']}, complexity: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_complexity']}, applied: {all_files_applied_rules[item]}")

            if programs_evolution[program_id]["current_pareto_set_relative"] == programs_evolution[program_id]["previous_pareto_set"]:
                programs_evolution[program_id]["unchanged_generations"] += 1
            else:
                programs_evolution[program_id]["unchanged_generations"] = 0
                previous_pareto_set = programs_evolution[program_id]["current_pareto_set_relative"]
            
            if programs_evolution[program_id]["unchanged_generations"] == 3:
                print(f"unchanged_generations: {programs_evolution[program_id]['unchanged_generations']}")
                if programs_evolution[program_id]["original_file"] in programs_to_transform:
                    programs_to_transform.remove(programs_evolution[program_id]["original_file"])
                if program_id in program_id_to_transform:
                    program_id_to_transform.remove(program_id)
                programs_evolution[program_id]["termination_reason"] = "unchanged_generations"
                result_initialization = summary(program_id, programs_evolution, individuals, result_initialization, csv_file, json_dir, all_files_applied_rules, evaluation_tests_dir)
                continue
                
            if programs_evolution[program_id]["used_time"] >= programs_evolution[program_id]["time_limit"]:
                print("Terminating GA due to time limit.")
                if programs_evolution[program_id]["original_file"] in programs_to_transform:
                    programs_to_transform.remove(programs_evolution[program_id]["original_file"])
                if program_id in program_id_to_transform:
                    program_id_to_transform.remove(program_id)
                programs_evolution[program_id]["termination_reason"] = "time limit"
                result_initialization = summary(program_id, programs_evolution, individuals, result_initialization, csv_file, json_dir, all_files_applied_rules, evaluation_tests_dir)
                continue
                    
        print(f"#Programs IDs for the next iteration {len(programs_to_transform), len(iteration_individuals[iterations])}")
        print(f"END at iteration {iterations}")
        
        print("Programs for next iteration:")
        for item in iteration_individuals[iterations]:
            program_id = item.split(".py")[0].split("/")[-1]
            print(f"{item}, readability: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_readability']}, complexity: {programs_evolution[program_id]['potential_individuals'][item]['relevant_distance_complexity']}, applied: {all_files_applied_rules[item]}")
        
        for item in programs_evolution[program_id]["potential_individuals"]:
            if len(iteration_individuals[iterations]) > 0:
                if item not in iteration_individuals[iterations]:
                    print(f"Deleting {item} to save disk space.")
                    delete_file_if_exists(item)
        
        utils.write_json(f"{json_dir}/jsons/iteration_individuals{iterations}.json", iteration_individuals[iterations])
        utils.write_json(f"{json_dir}/jsons/all_individuals{iterations}.json", all_individuals[iterations])
        
        print("Time comsuming:", time.time() - start_time)
        if time.time() - start_time >= budget:
            print("Terminating GA due to time limit.")
            utils.write_json(f"{json_dir}/jsons/iteration_individuals{iterations}.json", iteration_individuals[iterations])
            utils.write_json(f"{json_dir}/jsons/all_individuals{iterations}.json", all_individuals[iterations])
            budget_limit = True
            break

        

                
    # print(individuals)
    # save all individuals and their rules:
    # utils.write_json(f"{json_dir}/jsons/individuals.json", individuals))
    utils.write_json(f"{json_dir}/jsons/all_files_applied_rules.json", all_files_applied_rules)
    for program_id in program_id_to_transform:
        programs_evolution[program_id]["termination_reason"] = "time limit"
        result_initialization = summary(program_id, programs_evolution, individuals, result_initialization, csv_file, json_dir, all_files_applied_rules, evaluation_tests_dir)
    print(f'END AT {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')
    utils.dump_json(f"{json_dir}/jsons/programs_evolution.json", programs_evolution)
    
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function call timed out")

def set_timeout(seconds):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
def remove_same_id_pairs(all_pairs):
    uniq_pairs = []
    for pair in all_pairs:
        if pair[0].split("/")[-1].split("-")[0] != pair[1].split("/")[-1].split("-")[0]:
            uniq_pairs.append(pair)
    return uniq_pairs

def count_lines(program_code):
    return len(program_code.splitlines())

def get_time_used(time_dict):
    total_time = 0
    for iteration in time_dict:
        try:
            total_time += time_dict[iteration]["end"] - time_dict[iteration]["start"]
        except:
            pass
    return total_time

def find_most_diverse_rules_item(final_set):
    most_diverse_item = None
    max_complexity_item = None
    max_unique_rules_count = 0
    max_complexity = 0  # To keep track of the highest complexity among items.

    for item in final_set:
        program = item["variant_file"]
        rules = item['applied_rules']  # Assuming 'applied_rules' is directly accessible from the item.
        complexity = item["relevant_distance_complexity"]

        unique_rules = set(rules)  # Convert list of rules to a set to find unique rules.
        unique_rules_count = len(unique_rules)

        print(program, item["relevant_distance_readability"], complexity, rules)

        # Update the most diverse item if the current item has more unique rules,
        # or it has the same number of unique rules but higher complexity.
        if unique_rules_count > max_unique_rules_count:
            max_unique_rules_count = unique_rules_count
            most_diverse_item = item

        # Update the item with the maximum complexity if current complexity is higher than the recorded maximum.
        if complexity > max_complexity:
            max_complexity = complexity
            max_complexity_item = item

    # Randomly choose to return either the most diverse or the item with maximum complexity
    return random.choice([most_diverse_item, max_complexity_item])


def get_newclass(code):
    newclass = []
    if "from newClass" in code:
        for line in code.split("\n"):
            if "from newClass" in line:
                newfile = line.split("from")[-1].split("import")[0].strip() + ".py"
                if newfile not in newclass:
                    newclass.append(newfile)
    return newclass

def summary(program_id, programs_evolution, individuals, result_initialization, csv_file, json_dir, all_files_applied_rules, evaluation_tests_dir):
    current_pareto_set_relative = programs_evolution[program_id]["current_pareto_set_relative"]
    potential_individuals = programs_evolution[program_id]["potential_individuals"]
    source_file = programs_evolution[program_id]["original_file"]
    uniq_rules_per_iteration = programs_evolution[program_id]["uniq_rules_per_iteration"]
    uniq_rules_all_iterations = programs_evolution[program_id]["uniq_rules_all_iterations"]
    termination_reason = programs_evolution[program_id]["termination_reason"]
    
    final_set = get_final_pareto_optimal_set(programs_evolution[program_id]["potential_individuals"])
    
    for item in final_set:
        program = item["variant_file"]
        print(program, potential_individuals[program]["relevant_distance_readability"], potential_individuals[program]["relevant_distance_complexity"], potential_individuals[program]['applied_rules'])
    
    # select the one with the most diverse operators
    most_diverse_item = find_most_diverse_rules_item(final_set)
    
    for program in potential_individuals:
        print(program, potential_individuals[program]["relevant_distance_readability"], potential_individuals[program]["relevant_distance_complexity"])
    
    # final_set, random_seed, name_with_max_complexity = get_final_set(current_pareto_set_relative, potential_individuals)
    programs_evolution[program_id]["final_transformations"] = final_set
    result = get_statistics(final_set)
    
    original_content = ""
    newclass = []
    if most_diverse_item!= None:
        original_content = utils.read_file(most_diverse_item["variant_file"])
        original_rules = copy.deepcopy(most_diverse_item["applied_rules"])
        print(original_rules)
        update_content, most_diverse_item["applied_rules"] = transformation_single_rule(most_diverse_item["variant_file"], "move_functions_into_new_class", most_diverse_item["applied_rules"], most_diverse_item["variant_file"])
        if "move_functions_into_new_class" in most_diverse_item["applied_rules"]:
            res = check_tests_results("move_functions_into_new_class", most_diverse_item["applied_rules"], update_content, program_id, evaluation_tests_dir, update_content)
            if res:
                utils.write_file(most_diverse_item["variant_file"], update_content)
                newclass = get_newclass(update_content)
            else:
                print(f"Test Failure when running move_functions_into_new_class")
                most_diverse_item["applied_rules"] = original_rules
                utils.write_file(most_diverse_item["variant_file"], original_content)
    print(most_diverse_item["applied_rules"])
    res = {
        "source_file": source_file,
        "termination_reason": termination_reason,
        "initial_relevant_distance_complexity": individuals[source_file]["relevant_distance_complexity"],
        "initial_relevant_distance_readability": individuals[source_file]["relevant_distance_readability"],
        "#initial applicable operators": len(individuals[source_file]["applicable_rules"]),
        "#all applicable operators": len(uniq_rules_all_iterations),
        "#uniq_rules_per_iteration": [(iter, len(uniq_rules_per_iteration[iter])) for iter in uniq_rules_per_iteration],
        "operators used per iteration": uniq_rules_per_iteration,
        "iterations": programs_evolution[program_id]["iterations"],
        "time": programs_evolution[program_id]["used_time"],
        "#final_population_size": len(potential_individuals),
        "#pareto_optimal_set with complexity higher than median": len(current_pareto_set_relative),
        "#final_transformations": len(final_set),
        "final_transformations": final_set,
        "final_selection": most_diverse_item["variant_file"] if most_diverse_item!= None else None,
        "final_selection_original_content": original_content,
        "final_selection_class_dependencies": newclass,
        "avg_complexity": result['avg_complexity'], 
        "avg_readability": result['avg_readability'],
        "min_complexity": result['min_complexity'],
        "min_readability": result['min_readability'],
        "max_complexity": result['max_complexity'],
        "max_readability": result['max_readability'],
        "final_selection_rules": most_diverse_item["applied_rules"] if most_diverse_item!= None else None,
        "final_selection_complexity": most_diverse_item["relevant_distance_complexity"] if most_diverse_item!= None else None,
        "final_selection_readability": most_diverse_item["relevant_distance_readability"] if most_diverse_item!= None else None,
        "all_files_per_iteration": programs_evolution[program_id]["all_files_per_iteration"],
        "selected_files_per_iteration": programs_evolution[program_id]["selected_files_per_iteration"],
    }

    # print("RESULT", res)
    print(newclass)
    headers = [key for key in res.keys()]
    os.makedirs(f"{json_dir}/jsons", exist_ok=True)
    os.makedirs(f"{json_dir}/selection", exist_ok=True)
    os.makedirs(f"{json_dir}/no_inter_dependency", exist_ok=True)
    if most_diverse_item != None:
        shutil.copy(most_diverse_item["variant_file"], f"{json_dir}/selection")
        backup_file = os.path.join(f"{json_dir}/no_inter_dependency", most_diverse_item["variant_file"].split("/")[-1])
        utils.write_file(backup_file, res["final_selection_original_content"])
        for file in newclass:
            class_path = os.path.join("/".join(most_diverse_item["variant_file"].split("/")[:-1]), file)
            print(class_path)
            if os.path.exists(class_path):
                shutil.copy(class_path, f"{json_dir}/selection")
    csv_path = f"{json_dir}/jsons/{source_file.split('/')[-1].split('.py')[0]}.csv"
    if result_initialization == False:
        csv_file = initialize_csv(headers, csv_path)
    utils.write_dict_csv(csv_file, headers, res)
    utils.write_json(f"{json_dir}/jsons/{source_file.split('/')[-1].split('.py')[0]}.json", res)
    return True

    