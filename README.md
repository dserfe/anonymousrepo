# GeneBench

Dear ICSE'26 reviewers, 

Please note that **we have not changed the data we claimed to make available at submission** (please check the commit history to confirm). But we added the following items to enhance further validation: 

(1) a detailed readme about the structure of the artifact; 

(2) instructions and scripts to reproduce the results ([reproduction](reproduction/) folder); 

(3) original problems from Avatar, ClassEval, CruxEval, and HumanEval ([original dataset](original_dataset/) folder); 

(4) figures uploaded for the rebuttal period ([rebuttal](rebuttal/) folder); 

(5) a Zenodo file containing all the transformations, including those used as the main GeneBench benchmark, Pareto-front solutions, and non-optimal solutions ([zenodo](https://doi.org/10.5281/zenodo.15541624))

## Repository Structure
⭐️ Original programs from different datasets, namely Avatar, ClassEval, CruxEval, and HumanEval ([original_datasets](original_datasets)).

⭐️ Transformations of original benchmarks that constructed the final problems in GeneBench ([final_transformation](final_transformation/)).  

⭐️ Detailed logs of the transformation process for each individual program, including statistics for each transformation across all iterations, such as time cost, applied operators, and readability/complexity metrics ([logs](logs)).

⭐️ Scripts to reproduce and visualize evaluation results in the paper ([reproduction](reproduction/)).  

⭐️ Source code of GeneBench ([tool](tool/)). You can see the implementation of all operators under [tool/operators](tool/operators).   

⭐️ Details of 22 semantically equivalent transformation operators, along with code examples illustrating how they transform the code ([operators](operators.pdf)). If you have trouble loading the entire file (three pages), please view it [here](https://drive.google.com/file/d/1clxGcZ4fivTVM7-9hFkTMkly5ZsXqGt1/view?usp=sharing)).   

We built CFG generation tool [py2cfgplus](https://github.com/dserfe/anonymousrepo/tree/main/tool/metrics/py2cfgPlus/py2cfgPlus) on top of [py2cfg](https://py2cfg.readthedocs.io/en/latest/).

## 

## Usage

**0. Before starting**
- GeneBench works with `Python3.10.12` on `Linux`
- You can run the following steps to set up the environment
```
git clone https://github.com/dserfe/anonymousrepo
cd anonymousrepo
python3 -m venv genebench_venv
source genebench_venv/bin/activate
pip3 install -r requirements.txt
echo -e "import nltk\nnltk.download('punkt_tab')" > setup_nltk.py
python3 setup_nltk.py
rm -rf setup_nltk.py
```

**1. Run with GeneBench**  

GeneBench supports multiple modes for code transformation:

- You can run the following commands to apply transformations on a single file with any single operator  
```
python3 -u tool/init.py --src_file [input_file] --target_file [output_file] -c [result_json] --evaluation_tests_dir [test_directory] -r [operator]
```
e.g., 
```
python3 -u tool/init.py --src_file dataset/HumanEval/code/HumanEval_0.py --target_file reproduction_examples/HumanEval0_transformation.py -c reproduction_examples/HumanEval_0_result.json --evaluation_tests_dir dataset/HumanEval -r add_nested_if |& tee reproduction_examples/HumanEval_0_add_nested_if.log
```

- You can run the following commands to apply transformations on a single file with all operators  
```
python3 -u tool/init.py --src_file [input_file] --target_file [output_file] -c [result_json] --evaluation_tests_dir [test_directory]
```
e.g., 
```
python3 -u tool/init.py --src_file dataset/HumanEval/code/HumanEval_0.py --target_file reproduction_examples/HumanEval0_transformation.py -c reproduction_examples/HumanEval_0_result.json --evaluation_tests_dir dataset/HumanEval |& tee reproduction_examples/HumanEval_0.log
```

- You can run the following commands to apply genetic algorithm on a whole benchmark with a time budget
```
python3 -u tool/init.py -b [benchmark directory] -c [result_json] --evaluation_tests_dir [test_directory] --genetic_algorithm nsga-ii --time_budget [time budget]
```
e.g.,
```
python3 -u tool/init.py -b dataset/HumanEval/code -c reproduction_examples/HumanEval_result.json --evaluation_tests_dir dataset/HumanEval --genetic_algorithm nsga-ii --time_budget 3600|& tee HumanEval_ga.log
```

**2. Reproduce the evaluation results**

To directly reproduce the results in the evaluation, one can run the following commands:
```python
cd reproduction
python3 Fig7.py # code quality of transformation
python3 Fig8.py # operator analysis
python3 Fig9.py # performance analysis
python3 Fig10.py # analysis of performance drop
```
