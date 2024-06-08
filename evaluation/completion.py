import json
from vllm import LLM, SamplingParams
from analyze import evaluate_how, evaluate_when
import os
def complete(api_usage, llm, sampling_params):
    instruction = ""
    
    prompts = [f"{instruction}{code}" for code in api_usage]
    
    results = []
    outputs = llm.generate(prompts, sampling_params)
    

    for output in outputs:
        text = output.outputs[0].text
        results.append(text)
        # print(text)
    return results

def main():
    model_name = "codellama-34b"

    model_path = f'path/to/your/dir/{model_name}/'

    
    tokenizer_path = model_path
    parallel_size = 2     # gpu数量
    sampling_params = SamplingParams(temperature=0, top_p=1, max_tokens=32)
    llm = LLM(model=model_path, tensor_parallel_size=parallel_size, tokenizer=tokenizer_path, max_model_len=8192, gpu_memory_utilization=0.9)
    kind = "which"
    type_ = "type2"
    file_name = "function_comment"
    FIM = True
    # for file_name in  ["file20", "file40", "file60", "file80", "file100"] :
    # for file_name in ["file10", "file10_comment_import"]:
    for file_name in ["file10_LC_comment_import"]:
        #"function_comment", "function_import", "function_comment_import"
    # for file_name in ["function", "file10", "file10_comment", "file10_import", "file10_comment_import"]:
    
            
        if kind == "how":
            with open(f"data/{kind}/{kind}_to_use_{file_name}_type2.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif kind in ["when", "which"]:
            with open(f"data/{kind}/{kind}_to_use_{file_name}.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
        # with open(f"huawei_completion/how_to_use_{file_name}_{type_}.json", 'r', encoding='utf-8') as f:
        #     data = json.load(f)
        
        if FIM:
            file_name += "_fim"
        
        # check whether exists
        if kind == "how":
            if not os.path.exists(f"results/{kind}_to_use/{type_}/{model_name}"):
                os.makedirs(f"results/{kind}_to_use/{type_}/{model_name}")
            if os.path.exists(f"results/{kind}_to_use/{type_}/{model_name}/{file_name}.json"):
                print(f"Jump results/{kind}_to_use/{type_}/{model_name}/{file_name}.json")
                continue
                
        elif kind in ["when", "which"]:
            if not os.path.exists(f"results/{kind}_to_use/{model_name}"):
                os.makedirs(f"results/{kind}_to_use/{model_name}")
            if os.path.exists(f"results/{kind}_to_use/{model_name}/{file_name}.json"):
                print(f"Jump results/{kind}_to_use/{model_name}/{file_name}.json")
                continue
        
        total_results = []
        for item in data:
            api_name, values = list(item.keys())[0], list(item.values())[0]
            
            if not FIM:
                api_usage = [i['context_pre'] for i in values]
            else:
                if "starcoder" in model_name:
                    api_usage = [f"<fim_prefix>{i['context_pre']}<fim_suffix>{i['context_post']}<fim_middle>" for i in values]
                elif "deepseek" in model_name:
                    api_usage = [f"<｜fim▁begin｜>{i['context_pre']}<｜fim▁hole｜>{i['context_post']}<｜fim▁end｜>" for i in values]
                elif "codellama" in model_name:
                    api_usage = [f"{i['context_pre']}<FILL_ME>{i['context_post']}" for i in values]
            comple_results = complete(api_usage, llm, sampling_params)
            
            for idx, result in enumerate(comple_results):
                values[idx]['completion'] = result
                
            total_results.append({api_name: values})
            
        
        if kind == "how":
            if not os.path.exists(f"results/{kind}_to_use/{type_}/{model_name}"):
                os.makedirs(f"results/{kind}_to_use/{type_}/{model_name}")
            with open(f"results/{kind}_to_use/{type_}/{model_name}/{file_name}.json", 'w', encoding='utf-8') as f:
                json.dump(total_results, f, ensure_ascii=False, indent=4)
        elif kind in ["when", "which"]:
            if not os.path.exists(f"results/{kind}_to_use/{model_name}"):
                os.makedirs(f"results/{kind}_to_use/{model_name}")
            with open(f"results/{kind}_to_use/{model_name}/{file_name}.json", 'w', encoding='utf-8') as f:
                json.dump(total_results, f, ensure_ascii=False, indent=4)
        # with open(f"results/{kind}_to_use/{kind}_to_use/starcoderbase-3b/{file_name}.json", 'w', encoding='utf-8') as f:
        #     json.dump(total_results, f, ensure_ascii=False, indent=4)
        print('done', file_name)
        
        if kind == "how":
            evaluate_how(model_name, kind, type_, file_name)
        elif kind in ["when", "which"]:
            evaluate_when(model_name, kind, type_, file_name)
    
main()