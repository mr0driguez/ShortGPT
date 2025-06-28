from shortGPT.gpt import gpt_utils
def getGenderFromText(text):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/voice_identify_gender.yaml')
    chat = chat.replace("<<STORY>>", text)
    prompt = f"{system}\n\n{chat}"
    result = str(gpt_utils.get_gpt4free_completion(prompt)).replace("\n", "").lower()
    if 'female' in result:
        return 'female'
    return 'male'