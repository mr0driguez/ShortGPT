from shortGPT.gpt import gpt_utils
import json
from .gpt_utils import get_gpt4free_completion

def generateScript(script_description, language):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_script.yaml')
    chat = chat.replace("<<DESCRIPTION>>", script_description).replace("<<LANGUAGE>>", language)
    while not ('script' in out and out['script']):
        try:
            prompt = f"{system}\n{chat}"
            result = get_gpt4free_completion(prompt)
            out = json.loads(result)
        except Exception as e:
            print(e, "Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']

def correctScript(script, correction):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_edit_script.yaml')
    chat = chat.replace("<<ORIGINAL_SCRIPT>>", script).replace("<<CORRECTIONS>>", correction)

    while not ('script' in out and out['script']):
        try:
            prompt = f"{system}\n{chat}"
            result = get_gpt4free_completion(prompt)
            out = json.loads(result)
        except Exception as e:
            print("Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']

def generateScript_gpt4free(message, language):
    prompt = f"Generate a video script in {language} for: {message}"
    return get_gpt4free_completion(prompt)