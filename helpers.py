import json
import os

import discord
import requests
from discord import Embed
from dotenv import load_dotenv

from logger import log_request

# region Setup Env Vars

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ENV = os.getenv('ENV')
AI_MODEL = os.getenv('AI_MODEL')

# endregion

class EmbedHelper:
    @staticmethod
    def embed_ai_response(title: str, description: str, request: str):
        return Embed(
            title=title,
            description=description,
            type="rich",
            colour=discord.Color.blurple(),
        ).set_author(name="Knowledge God").set_footer(text=f"Request: {request}")

    @staticmethod
    def embed_error_message(title: str, description: str, request: str):
        return Embed(
            title=title,
            description=description,
            type="rich",
            colour=discord.Color.red()
        ).set_author(name="Knowledge God").set_footer(text=f"Request: {request}")


@log_request
def make_request(request):
    """Makes a request to Ollama's API and returns the response to the users prompt"""
    url = "http://localhost:11434/api/generate"
    return requests.post(url=url, data=json.dumps({
        "model": AI_MODEL,
        "prompt": request,
        "stream": False
    })).json().get("response")
