from shortGPT.gpt import gpt_utils
import json

def generate_title_description_dict(content):
    out = {"title": "", "description":""}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/yt_title_description.yaml')
    chat = chat.replace("<<CONTENT>>", f"{content}")
    
    while out["title"] == "" or out["description"] == "":
        prompt = f"{system}\n\n{chat}"
        result = str(gpt_utils.get_gpt4free_completion(prompt))
        try:
            response = json.loads(result)
            if "title" in response:
                out["title"] = response["title"]
            if "description" in response:
                out["description"] = response["description"]
        except Exception as e:
            pass
        
    return out['title'], out['description']
