import os # for file system operations
from openai import OpenAI # API call wrapping for ollama
import subprocess # for running ollama
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)           # makes ANSI colours work on Windows, too

MODEL_ZEPHYR = "zephyr:7b" # 7b is the size of the model
MODEL_MISTRAL = "mistral:7b" # using mistral as the second debater

# in order to keep this free, and without api keys we will use two local ollama models
# zephyr and mistral will debate with different perspectives

# we will use the ollama api to call the models

# try:
#     subprocess.run(["ollama", "serve", MODEL_ZEPHYR], check=True)
#     subprocess.run(["ollama", "serve", MODEL_MISTRAL], check=True)
# except subprocess.CalledProcessError as e:
#     print(f"Error starting ollama models: {e}")
#     exit(1)

ZEPHYR_SYSTEM_PROMPT = "Given a topic you will give your opionion and thoughts, you will continue to debate with the user not in order to convince them but rather to try and create a deeper understanding of the topic, you are objective however kind and willing to listen to the user's perspective."
MISTRAL_SYSTEM_PROMPT = "Given a topic you will give your opionions and thoughts trying to advance the conversation and reach deeper understandings, you point out the flaws in the other person's argument and provide counter arguments, you are objective however kind and willing to listen to the user's perspective."

# Configure OpenAI clients with dummy API key for Ollama
Zephyr = OpenAI(
    base_url="http://localhost:11434/v1",  # Updated URL to include /v1
    api_key="sk-dummy-key"  # Dummy API key required by the client
)
Mistral = OpenAI(
    base_url="http://localhost:11434/v1",  # Updated URL to include /v1
    api_key="sk-dummy-key"  # Dummy API key required by the client
)

zephyr_messages = []
mistral_messages = []

def callZephyr():
    messages = [{"role": "system", "content": ZEPHYR_SYSTEM_PROMPT}]
    # chronological order: Mistral (user) first, Zephyr (assistant) second
    for i in range(len(mistral_messages)):
        messages.append({"role": "user", "content": mistral_messages[i]})
        messages.append({"role": "assistant", "content": zephyr_messages[i]})
    # If Mistral has just spoken and Zephyr hasn't answered yet
    if len(zephyr_messages) < len(mistral_messages):
        # this branch is never hit in the current loop order,
        # but keeps the function symmetrical
        messages.append({"role": "user", "content": mistral_messages[-1]})

    response = Zephyr.chat.completions.create(
        model=MODEL_ZEPHYR,
        messages=messages
    )
    return response.choices[0].message.content


def callMistral():
    messages = [{"role": "system", "content": MISTRAL_SYSTEM_PROMPT}]
    # chronological order: Zephyr (user) first, Mistral (assistant) second
    for i in range(len(zephyr_messages)):
        messages.append({"role": "user", "content": zephyr_messages[i]})
        if i < len(mistral_messages):            # old Mistral replies
            messages.append({"role": "assistant",
                             "content": mistral_messages[i]})
    # Zephyr just spoke; Mistral hasn’t replied yet – include it
    if len(zephyr_messages) > len(mistral_messages):
        messages.append({"role": "user", "content": zephyr_messages[-1]})

    response = Mistral.chat.completions.create(
        model=MODEL_MISTRAL,
        messages=messages
    )
    return response.choices[0].message.content


# -----------------------------------
# helpers
# -----------------------------------
def _build_history(you_first, you_hist, them_hist):
    """Interleave two parallel lists chronologically."""
    msgs = []
    for u, t in zip(you_hist, them_hist):
        msgs.append({"role": "user",      "content": you_first and u or t})
        msgs.append({"role": "assistant", "content": you_first and t or u})
    return msgs

def _chat(client, model, sys_prompt, you_hist, them_hist,
          color, label, you_first, stream=False):
    """Core call that can stream or return the whole string."""
    messages = [{"role": "system", "content": sys_prompt}]
    messages += _build_history(you_first, you_hist, them_hist)

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )

    if not stream:                         # classic, non-stream mode
        return resp.choices[0].message.content

    # ----- stream mode -----
    full = ""
    print(f"{color}{label}: {Style.RESET_ALL}", end="", flush=True)
    for chunk in resp:
        delta = chunk.choices[0].delta.content or ""
        full += delta
        print(f"{color}{delta}{Style.RESET_ALL}", end="", flush=True)
    print()                                # newline after model finishes
    return full

# -----------------------------------
# thin wrappers so the rest of your code barely changes
# -----------------------------------
def callZephyr(stream=False):
    return _chat(
        Zephyr, MODEL_ZEPHYR,
        ZEPHYR_SYSTEM_PROMPT,
        mistral_messages,     # mistral speaks first *to* Zephyr
        zephyr_messages,
        Fore.CYAN, "Zephyr", you_first=False, stream=stream
    )

def callMistral(stream=False):
    return _chat(
        Mistral, MODEL_MISTRAL,
        MISTRAL_SYSTEM_PROMPT,
        zephyr_messages,      # zephyr speaks first *to* Mistral
        mistral_messages,
        Fore.MAGENTA, "Mistral", you_first=False, stream=stream
    )


def main():
    global zephyr_messages, mistral_messages
    print("Please enter a topic to debate on:")
    DebateTopic = input()
    print(f"Debating on: {DebateTopic}")

    # Initialize with opening statements
    zephyr_messages.append(f"Hi! I'm Zephyr, your debate partner. Let's dive into the topic: {DebateTopic}")
    mistral_messages.append(f"Hi! I'm Mistral, your debate partner. Let's dive into the topic: {DebateTopic}")
    print("Zephyr: " + zephyr_messages[-1])
    print("Mistral: " + mistral_messages[-1])

    while True:
        for i in range(10):
            zephyr_response = callZephyr(stream=True)
            zephyr_messages.append(zephyr_response)
            print("Zephyr: " + zephyr_response)
            
            mistral_response = callMistral(stream=True)
            mistral_messages.append(mistral_response)
            print("Mistral: " + mistral_response)
        
        cont = input("Continue? (y/n): ")
        if cont.upper() == "N":
            break
    print("Thank you for debating with me! Goodbye!")

if __name__ == "__main__":
    main()