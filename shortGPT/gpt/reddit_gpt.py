from shortGPT.gpt import gpt_utils
import random
import json
def generateRedditPostMetadata(title):
    name = generateUsername()
    if title and title[0] == '"':
        title = title.replace('"', '')
    n_months = random.randint(1,11)
    header = f"{name} - {n_months} months ago"
    n_comments = random.random() * 10 + 2
    n_upvotes = n_comments*(1.2+ random.random()*2.5)
    return title, header, f"{n_comments:.1f}k", f"{n_upvotes:.1f}k"


def getInterestingRedditQuestion():
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_generate_question.yaml')
    prompt = f"{system}\n\n{chat}"
    return str(gpt_utils.get_gpt4free_completion(prompt))

def createRedditScript(question):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_generate_script.yaml')
    chat = chat.replace("<<QUESTION>>", question)
    prompt = f"{system}\n\n{chat}"
    result = "Reddit, " + question + " " + str(gpt_utils.get_gpt4free_completion(prompt))
    return result
    

def getRealisticness(text):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_filter_realistic.yaml')
    chat = chat.replace("<<INPUT>>", text)
    attempts = 0
    while attempts <= 4:
        attempts+=1
        try:
            prompt = f"{system}\n\n{chat}"
            result = str(gpt_utils.get_gpt4free_completion(prompt))
            return json.loads(result)['score']
        except Exception as e:
            print("Error in getRealisticness", e.args[0])
    raise Exception("LLM Failed to generate a realisticness score on the script")

def getQuestionFromThread(text):
    if ((text.find("Reddit, ") < 15) and (10 < text.find("?") < 100)):
        question = text.split("?")[0].replace("Reddit, ", "").strip().capitalize()
    else:
        chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_filter_realistic.yaml')
        chat = chat.replace("<<STORY>>", text)
        prompt = f"{system}\n\n{chat}"
        question = str(gpt_utils.get_gpt4free_completion(prompt)).replace("\n", "")
        question = question.replace('"', '').replace("?", "")
    return question


def generateUsername():
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_username.yaml')
    prompt = f"{system}\n\n{chat}"
    return str(gpt_utils.get_gpt4free_completion(prompt)).replace("u/", "")


