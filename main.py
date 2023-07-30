# main entry point to have a dialogue with the user and ChatGPT

import openai
import yaml

default_prompt = """You are a dungeon master and responding to the player's stated actions."""

messages = [
    {"role": "system", "content": default_prompt},
    {"role": "user", "content": "What's behind the magic door?"}]


def init():
    # Load config
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    openai.api_key = config["openai_key"]

def run():
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stop=None,
        max_tokens=350)
    
    print(response.choices[0].message.content)

if __name__ == "__main__":
    init()
    run()
