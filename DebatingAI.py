import os # for file system operations
from openai import OpenAI # API call wrapping for ollama
import subprocess # for running ollama

MODEL_ZEPHYR = "zephyr:7b" # 7b is the size of the model
MODEL_HERMES = "hermes:7b" # 7b is the size of the model

# in order to keep this free, and without api keys we will use two local ollama models
# zephyr is a general purpose model
# hermes is a model that is trained on the hermes dataset

# we will use the ollama api to call the models

try:
    subprocess.run(["ollama", "run", MODEL_ZEPHYR], check=True)
    subprocess.run(["ollama", "run", MODEL_HERMES], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting ollama models: {e}")
    exit(1)

ZEPHYR_SYSTEM_PROMPT = "Given a topic you will give your opionion and thoughts, you will continue to debate with the user not in order to convince them but rathe\
    to try and create a deeper understanding of the topic, you are objective however kind and willing to listen to the user's perspective."
HERMES_SYSTEM_PROMPT = "Given a topic you will give your opionions and thoughts trying to advance the conversation and reach deeper understandings\
    you point out the flaws in the other person's argument and provide counter arguments, you are objective however kind and willing to listen to the user's perspective."

Zephyr = OpenAI(base_url="http://localhost:11434")
Hermes = OpenAI(base_url="http://localhost:11434")

zephyr_messages = []
hermes_messages = []

def callZephyr():
    messages = [{"role": "system", "content": ZEPHYR_SYSTEM_PROMPT}]
    for zep, herm in zip(zephyr_messages, hermes_messages):
        messages.append({"role": "assistant", "content": zep})
        messages.append({"role": "user", "content": herm})
    response = Zephyr.chat.completions.create(
        model=MODEL_ZEPHYR,
        messages=messages
    )
    return response.choices[0].message.content

def callHermes():
    messages = [{"role": "system", "content": HERMES_SYSTEM_PROMPT}]
    for zep, herm in zip(zephyr_messages, hermes_messages):
        messages.append({"role": "assistant", "content": herm})
        messages.append({"role": "user", "content": zep})
    response = Hermes.chat.completions.create(
        model=MODEL_HERMES,
        messages=messages
    )
    return response.choices[0].message.content

def main():
    print("Please enter a topic to debate on:")
    DebateTopic = input()
    print(f"Debating on: {DebateTopic}")

    zephyr_messages = ["Hi! I'm Zephyr, your debate partner. Let's dive into the topic: " + DebateTopic]
    hermes_messages = ["Hi! I'm Hermes, your debate partner. Let's dive into the topic: " + DebateTopic]
    while True:
        for i in range(10):
            zephyr_messages.append(callZephyr())
            hermes_messages.append(callHermes())
            print("Zephyr: " + zephyr_messages[-1])
            print("Hermes: " + hermes_messages[-1])
        
        cont = input("Continue? (y/n): ")
        if cont.upper == "N":
            break
    print("Thank you for debating with me! Goodbye!")

if __name__ == "__main__":
    main()