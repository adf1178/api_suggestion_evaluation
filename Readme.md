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

