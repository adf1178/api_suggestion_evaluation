# Benchmark generation

All of the scenarios are generated from generate/java_spring_api.json

Details are describted in `generate/Readme.md`

Note that generate_benchmark.py can only generate benchmark items for `how` and `when` scenarios. For which, you can use evaluation/construct_which.py to generate.

There are two types in `how to use`: we use type2 in our paper: For instance, given `Assert.NotNull` and expect  `(uid)`. For type1:  given `Assert.NotNull(` and expect  `uid)`, this is not suitable for LCMs because the tokenizer may have some problems.

# Evaluation

After generating benchmark item with some contexts: such as `when_to_use_file10_comment_import.json`, put it into `evaluation/data`.

Then set the:
- model_name
- model_path
- kind
- file_name

in `evaluation/completion.py`. And then run it, the results will be recorded in `evaluation/results`. The metric will be printed out after evaluation (via `evaluation/analyze.py`)

## Dependencies

- vllm
- transformers
- torch


## Results of throughput of individual LCMs

|       | SC-3B  | SC-7B   | SC-15B  | CL-7B   | CL-13B  | CL-34B  | DSC-1.3B | DSC-6.7B | DSC-33B | AVG          |
|-------|--------|---------|---------|---------|---------|---------|----------|----------|---------|--------------|
| Basic | 1754.49| 1320.146| 780.498 | 1222.648| 851.065 | 431.26  | 1748.49  | 1418.047 | 435.365 | 1106.88998   |
| +F    | 1700.799| 1184.1203| 708.1648 | 1111.044| 731.26  | 371.786 | 1668.663 | 1254.264 | 377.516 | 1011.95746   |
| +F+C  | 1496.631| 958.548 | 581.076 | 942.792 | 609.002 | 301.472 | 1602.197 | 1052.871 | 309.7578| 872.7052     |
| +F+I  | 1219.699| 727.053 | 453.575 | 759.631 | 466.998 | 233.966 | 1240.712 | 808.017  | 222.671 | 681.369111   |
| +F+R  | 1408.45 | 842.105 | 541.654 | 816.326 | 528.052 | 266.66  | 1371.683 | 945.43   | 263.6   | 775.995556   |
| +F+C+I| 1149.789| 676.72  | 393.424 | 678.305 | 417.358 | 205.642 | 1209.172 | 718.422  | 199.958 | 627.643333   |
| +F+C+I+R| 963.36 | 516.129 | 335.4649| 538.72  | 331.262 | 143.981 | 989.315  | 585.825  | 138.34  | 504.710767   |