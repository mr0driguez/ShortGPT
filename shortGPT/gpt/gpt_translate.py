from .gpt_utils import get_gpt4free_completion

def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}: {text}"
    return get_gpt4free_completion(prompt)