import json
from fuzzywuzzy import fuzz


def find_first_unmatched_right_parenthesis(s, type):
    # 初始化计数器来跟踪左括号
    left_parenthesis_count = 0
    
    # 遍历字符串中的每个字符
    for index, char in enumerate(s):
        # 如果是左括号，增加计数器
        if char == '(':
            left_parenthesis_count += 1
        # 如果是右括号
        elif char == ')':
            # 如果计数器为零，这是一个非闭合的右括号
            if type == 'type1':
                if left_parenthesis_count == 0:
                    return index
                else:
                    left_parenthesis_count -= 1
            else:
                if left_parenthesis_count == 1:
                    return index+1
                else:
                    left_parenthesis_count -= 1
            # 否则，减少计数器
            
    
    # 如果所有的右括号都已闭合，返回 -1
    return -1
def evaluate_how(model_name, completion_type, type_, file_name):
    # model_name = "deepseek-33b"
    # completion_type = "how"
    # type_ = "type2"
    # file_name = "function"
    import json
    if completion_type == "how":
        with open(f"results/{completion_type}_to_use/{type_}/{model_name}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif completion_type == "when":
        with open(f"huawei_completion/when_to_use/{model_name}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        type_ = "type2"
    total_count = 0
    EM_count = 0
    total_esim = []
    group = {}
    for item in data:
        current = []
        api_name, values = list(item.keys())[0], list(item.values())[0]
        
        for single in values:
            gt = single['content']
            output = single['completion'][:find_first_unmatched_right_parenthesis(single['completion'], type_)]
            
            current.append(fuzz.ratio(output, gt))
            if gt == output:
                EM_count += 1

            total_count += 1
        group[api_name] = current
        
    for k, v in group.items():
        total_esim.extend(v)
        # print(f"The API {k}'s avg edit sim is {sum(v)/len(v):.2f}")
    print(f" Total AVG Edit SIM {sum(total_esim)/len(total_esim)}")  
    print(EM_count/total_count)
    
    
def evaluate_when(model_name, completion_type, type_, file_name):
    # model_name = "deepseek-33b"
    # completion_type = "how"
    # type_ = "type2"
    # file_name = "function"
    import json
    if completion_type == "how":
        with open(f"results/{completion_type}_to_use/{type_}/{model_name}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif completion_type in ["when", "which"]:
        with open(f"results/{completion_type}_to_use/{model_name}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        type_ = "type2"
    total_count = 0
    EM_count = 0
    API_ACC = 0
    total_esim = []
    group = {}
    for item in data:
        current = []
        api_name, values = list(item.keys())[0], list(item.values())[0]
        
        for single in values:
            gt = single['content']
            output = single['completion'][:find_first_unmatched_right_parenthesis(single['completion'], type_)].strip()
            current.append(fuzz.ratio(output, gt))
            # find the content before (
            api_output = output[:output.find("(")]
            api_gt = gt[:gt.find("(")]
            if gt == output:
                EM_count += 1
            if api_gt == api_output:
                API_ACC += 1
            total_count += 1
        group[api_name] = current
        
    for k, v in group.items():
        total_esim.extend(v)
        # print(f"The API {k}'s avg edit sim is {sum(v)/len(v):.2f}")
    print(f" Total AVG Edit SIM {sum(total_esim)/len(total_esim)}")  
    print("API Accuracy : ",API_ACC/total_count)
    print("Exact Match: ",EM_count/total_count)
    
    
if __name__ == "__main__":
    model_name = "codellama-34b"
    completion_type = "which"
    type_ = "type2"
    file_name = "file10_comment"
    # for file_name in ["function","file10", "file10_comment", "file10_import", "file10_comment_import"]:
    for file_name in ["file80"]:
        print(file_name)
        
        if completion_type == "how":
            evaluate_how(model_name, completion_type, type_, file_name)
        elif completion_type in ["when", "which"]:
            evaluate_when(model_name, completion_type, type_, file_name)