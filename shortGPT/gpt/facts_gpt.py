from shortGPT.gpt import gpt_utils
import json
def generateFacts(facts_type):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/facts_generator.yaml')
    chat = chat.replace("<<FACTS_TYPE>>", facts_type)
    prompt = f"{system}\n\n{chat}"
    result = gpt_utils.get_gpt4free_completion(prompt)
    return str(result)

def generateFactSubjects(n):
    out = []
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/facts_subjects_generation.yaml')
    chat = chat.replace("<<N>>", f"{n}")
    maxAttempts = int(1.5*n)
    attempts=0
    while len(out) != n & attempts <= maxAttempts:
        prompt = f"{system}\n\n{chat}"
        result = gpt_utils.get_gpt4free_completion(prompt)
        attempts+=1
        try:
            out = json.loads(str(result).replace("'", '"'))
        except Exception as e:
            print(f"INFO - Failed generating {n} fact subjects after {attempts} trials", e)
            pass
    if len(out) != n:
        raise Exception(f"Failed to generate {n} subjects. In {attempts} attemps")   
    return out