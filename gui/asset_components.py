import os
import platform
import random
import subprocess

import gradio as gr

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


class AssetComponentsUtils:
    EDGE_TTS = "Free EdgeTTS (lower quality)"
    ELEVEN_TTS = "ElevenLabs(Very High Quality)"


    instance_background_video_checkbox = None
    instance_background_music_checkbox = None
    instance_voiceChoice: dict[str, gr.Radio] = {}
    instance_voiceChoiceTranslation: dict[str, gr.Radio] = {}

    @classmethod
    def getBackgroundVideoChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc["background video" == df["type"]]["name"])[:20]
        return choices

    @classmethod
    def getBackgroundMusicChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc["background music" == df["type"]]["name"])[:20]
        return choices

    @classmethod
    def getElevenlabsVoices(cls):
        api_key = ApiKeyManager.get_api_key("ELEVENLABS_API_KEY")
        voices_dict = ElevenLabsAPI(api_key).get_voices()
        if not voices_dict:
            print("No ElevenLabs voices found. Check your API key or ElevenLabs API status.")
            return ["No voices available"]
        voices = list(reversed(voices_dict.keys()))
        return voices

    @classmethod
    def start_file(cls, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    @classmethod
    def background_video_checkbox(cls):
        if cls.instance_background_video_checkbox is None:
            choices = cls.getBackgroundVideoChoices()
            cls.instance_background_video_checkbox = gr.CheckboxGroup(
                choices=choices,
                interactive=True,
                label="Choose background video",
                value=random.choice(choices)
            )
        return cls.instance_background_video_checkbox

    @classmethod
    def background_music_checkbox(cls):
        if cls.instance_background_music_checkbox is None:
            choices = cls.getBackgroundMusicChoices()
            cls.instance_background_music_checkbox = gr.CheckboxGroup(
                choices=choices,
                interactive=True,
                label="Choose background music",
                value=random.choice(choices)
            )
        return cls.instance_background_music_checkbox

    @classmethod
    def voiceChoice(cls, provider: str = None):
        if provider is None:
            provider = cls.ELEVEN_TTS
        if cls.instance_voiceChoice.get(provider, None) is None:
            if provider == cls.ELEVEN_TTS:
                voices = cls.getElevenlabsVoices() or ["No voices available"]
                default_voice = voices[0] if voices else "No voices available"
                cls.instance_voiceChoice[provider] = gr.Radio(
                    voices,
                    label="Elevenlabs voice",
                    value=str(default_voice),
                    interactive=True,
                )
        return cls.instance_voiceChoice[provider]

    @classmethod
    def voiceChoiceTranslation(cls, provider: str = None):
        if provider is None:
            provider = cls.ELEVEN_TTS
        if cls.instance_voiceChoiceTranslation.get(provider, None) is None:
            if provider == cls.ELEVEN_TTS:
                voices = cls.getElevenlabsVoices() or ["No voices available"]
                default_voice = voices[0] if voices else "No voices available"
                cls.instance_voiceChoiceTranslation[provider] = gr.Radio(
                    voices,
                    label="Elevenlabs voice",
                    value=str(default_voice),
                    interactive=True,
                )
        return cls.instance_voiceChoiceTranslation[provider]
