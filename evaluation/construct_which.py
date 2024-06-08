import json
import os

whens = os.listdir("data/when")
# whichs = os.listdir("results/which_to_use")
# for model in whens:
#     model_results_path = os.path.join("results/when_to_use", model)
    
#     for result in os.listdir(model_results_path):
#         when_path = os.path.join("results/when_to_use", model, result)
#         which_path = os.path.join("results/which_to_use", model, result)
#         with open(when_path, 'r', encoding='utf-8') as f:
#             when_data = json.load(f)
#         with open(which_path, 'r', encoding='utf-8') as f:
#             which_data = json.load(f)
#         new_which_data = []
#         for idx1, apis in enumerate(which_data):
#             new_which = []
#             api_name, values = list(apis.keys())[0], list(apis.values())[0]
#             for idx2, item in enumerate(values):
#                 current = {}
#                 current = item
#                 current['content'] = when_data[idx1][api_name][idx2]['content'].split('.', 1)[1]
                
#                 new_which.append(current)
#             new_which_data.append({api_name: new_which})
        
#         with open(os.path.join("results/which_to_use2", model, result), "w") as f:
#             json.dump(new_which_data, f, indent=4, ensure_ascii=False)
for when_name in whens:
    when_path = os.path.join("data/when", when_name)
    with open(when_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    which_data = []
    for apis in data:
        api_name, values = list(apis.keys())[0], list(apis.values())[0]
        which = []
        
        for item in values:
            current = {}
            parrent_api = item['content'].split('.')[0]
            current['context_pre'] = item['context_pre'] + parrent_api + '.'
            current['content'] = item['content'].split('.', 1)[1]
            current['context_post'] = item['context_post']
            
            which.append(current)
        which_data.append({api_name: which})
    
    which_path = os.path.join("data/which", when_name.replace("when", "which"))
    with open(which_path, 'w', encoding='utf-8') as f:
        json.dump(which_data, f, indent=4, ensure_ascii=False)
            