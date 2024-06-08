import json
import re
import yaml

with open("java_spring_api.json", 'r', encoding='utf-8') as f:
    raw_data = json.load(f)


def load_config(filepath):
    # 从 YAML 文件加载配置
    with open(filepath, 'r') as file:
        config_dict = yaml.safe_load(file)
        return ConfigObject(config_dict)

class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                # 如果值是字典，再次调用此类将其转换为对象
                value = ConfigObject(value)
            self.__dict__[key] = value

    def __len__(self):
        return len(self.__dict__)

    def __str__(self) -> str:
        # 改进的打印方法，递归打印配置项
        def _str(obj, indent=0):
            result = ""
            for key, value in obj.__dict__.items():
                result += '    ' * indent + str(key) + ': '
                if isinstance(value, ConfigObject):
                    result += '\n' + _str(value, indent + 1)
                else:
                    result += str(value) + '\n'
            return result
        return _str(self)

    def __iter__(self):
        # 返回一个迭代器，遍历配置项
        for key, value in self.__dict__.items():
            yield (key, value)


def statistic(): 
    print(f"There are {len(raw_data.keys())} APIs")


    related_files = []
    total_num = 0
    for api_name, usage_list in raw_data.items():
        # print(len(usage_list))
        total_num += len(usage_list)
        for single_use in usage_list:
            related_files.append(single_use['git_name'])
            
    print(f"There are {total_num} benchmarks")
    print(f"There are {len(set(related_files))} unique projects")


def construct_how_to_use(api, code):
    # 使用 re.escape 确保 api 中的特殊字符被正确处理
    escaped_api = re.escape(api)
    
    # 动态构造正则表达式，匹配 api 函数调用
    pattern = rf'({escaped_api}\()'
    
    contents = []

    for match in re.finditer(pattern, code, re.DOTALL):
        start_pos = match.start(1)
        # 寻找对应的闭合括号，考虑括号的嵌套
        open_brackets = 1
        cursor = match.end(1)
        while open_brackets > 0 and cursor < len(code):
            if code[cursor] == '(':
                open_brackets += 1
            elif code[cursor] == ')':
                open_brackets -= 1
            cursor += 1
        
        # 提取内容
        content = code[match.end(1):cursor-1]

        # 提取前文和后文
        context_pre = code[:start_pos] + api + '('
        context_post = code[cursor-1:]
        
        contents.append({"context_pre":context_pre, 
                         "content":content, 
                         "context_post":context_post})
    
    return contents

def find_matching_parenthesis(code, start_pos):
    # 寻找匹配的闭合括号
    open_brackets = 1
    cursor = start_pos
    while open_brackets > 0 and cursor < len(code):
        if code[cursor] == '(':
            open_brackets += 1
        elif code[cursor] == ')':
            open_brackets -= 1
        cursor += 1
    return cursor  # 返回找到的匹配的闭合括号的位置


def construct_when_to_use(api, code):
    """
    A function that constructs when to use a given API within a code snippet.

    Args:
        api (str): The API to be used.
        code (str): The code snippet where the API is being used.

    Returns:
        list: A list of dictionaries containing the context before the API call, the API call content, and the context after the API call within the code snippet.
    """
    # 使用 re.escape 确保 api 中的特殊字符被正确处理
    escaped_api = re.escape(api)
    pattern = rf'({escaped_api}\()'
    
    usages = []

    for match in re.finditer(pattern, code):
        start_pos = match.start(1) + len(api) + 1  # 定位到API调用的开括号后的第一个字符
        end_pos = find_matching_parenthesis(code, start_pos)  # 找到匹配的闭合括号位置

        # 提取内容，即API调用及其完整表达式
        content = code[match.start(1):end_pos]
        
        # 提取API调用之前的代码作为前文
        context_pre = code[:match.start(1)]
        
        # 提取API调用表达式之后的代码作为后文
        context_post = code[end_pos:]
        
        usages.append({"context_pre":context_pre, 
                         "content":content, 
                         "context_post":context_post})
    
    return usages


def generate_how_to_use(config):
    total_data = []

    for api_name, usage_list in raw_data.items():
        current_data = []
        for single_use in usage_list:
            api = '.'.join(api_name.split('.')[-2:])
            comment = single_use['comment']
            file_left_context = single_use['left_context']
            file_right_context = single_use['right_context']
            pure_code = single_use['code'].replace(comment, '').strip()
            import_list = ["import "+i for i in single_use['import_text']]
            input_data = pure_code 
            if config.USE_COMMENT:
                input_data = comment + '\n' + input_data
                
            if config.USE_FILE_CONTEXT:
                input_data = '\n'.join(file_left_context.split('\n')[-config.LINE_BEFORE:]) + '\n' + input_data
            
            if config.USE_IMPORT_MESSAGE:
                input_data = '\n'.join(import_list) + "\n" + input_data
            current_data += construct_how_to_use(api, input_data)
        total_data.append({api_name:current_data})
        #     print(construct_how_to_use(api, single_use['code'])[0][0])
        #     print(construct_how_to_use(api, single_use['code'])[0][1])
        #     print(construct_how_to_use(api, single_use['code'])[0][2])
        #     break
        # break
        
    print(len(total_data))


    with open(f"{config.SAVE_FILE_NAME}.json", 'w', encoding='utf-8') as f:
        json.dump(total_data, f, ensure_ascii=False, indent=4)


def generate_when_to_use(config):
    when_to_use = []

    for api_name, usage_list in raw_data.items():
        current_data = []
        for single_use in usage_list:
            
            api = '.'.join(api_name.split('.')[-2:])
            comment = single_use['comment']
            file_left_context = single_use['left_context']
            file_right_context = single_use['right_context']
            pure_code = single_use['code'].replace(comment, '').strip()
            import_list = ["import "+i for i in single_use['import_text']]
            input_data = pure_code 
            if config.USE_COMMENT:
                input_data = comment + '\n' + input_data
                
            if config.USE_FILE_CONTEXT:
                input_data = '\n'.join(file_left_context.split('\n')[-config.LINE_BEFORE:]) + '\n' + input_data
            
            if config.USE_LIBRARY_CANDIDATE:
                parent = '.'.join(api_name.split('.')[:-1])
                with open("parent_apis.json", 'r', encoding='utf-8') as f:
                    parent_api = json.load(f)
                if parent in parent_api:
                    available_api = parent_api[parent]
                else:
                    if "HttpStatus" in parent:
                        available_api = ["value"]
                    elif "HttpMethod" in parent or "RequestMethod" in parent:
                        available_api = ["name", "toString"]
                    else:
                        raise ValueError("No available API", parent)
                available_api_str = '\n'.join(available_api)
                prompts = f"/* The available APIs in {parent} is {available_api_str} */\n"
                input_data = prompts + input_data
            
            if config.USE_IMPORT_MESSAGE:
                input_data = '\n'.join(import_list) + "\n" + input_data
            current_data += construct_when_to_use(api, input_data)
        when_to_use.append({api_name:current_data})
            # print(construct_when_to_use(api, single_use['code'])[0]["context_pre"])
            # print("#################")
            # print(construct_when_to_use(api, single_use['code'])[0]["content"])
            # print("#################")
            # print(construct_when_to_use(api, single_use['code'])[0]["context_post"])
            
            
    with open(f"{config.SAVE_FILE_NAME}.json", 'w', encoding='utf-8') as f:
        json.dump(when_to_use, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    statistic()
    
    config = load_config("config.yaml")
    if config.TYPE == "how":
        generate_how_to_use(config)
    elif config.TYPE == "when":
        generate_when_to_use(config)