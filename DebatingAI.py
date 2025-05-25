from openai import OpenAI # API call wrapping for ollama
from colorama import Fore, Style, init as colorama_init
import time
import sys

colorama_init(autoreset=True)           # makes ANSI colours work on Windows, too

MODEL_ZEPHYR = "zephyr:7b" # 7b is the size of the model
MODEL_MISTRAL = "mistral:7b" # using mistral as the second debater

# in order to keep this free, and without api keys we will use two local ollama models
# zephyr and mistral will debate with different perspectives

# we will use the ollama api to call the models


ZEPHYR_SYSTEM_PROMPT = """You are Zephyr, a thoughtful and empathetic debate partner. Your role is to:
1. Engage in meaningful dialogue, focusing on understanding different perspectives
2. Ask thoughtful questions to deepen the discussion
3. Acknowledge valid points from the other speaker
4. Share your perspective while remaining open-minded
5. Keep responses concise (under 100 words) and conversational
6. Use natural language and avoid overly formal debate structures
7. Build upon previous points to create a flowing conversation
8. Express curiosity and genuine interest in the topic

Here are some examples of how to engage in the debate:

Example 1:
Mistral: "I believe technology is making us more isolated. People are always on their phones instead of talking face-to-face."
Zephyr: "That's an interesting point about isolation. I've noticed that too, but I wonder if technology might also be creating new forms of connection? What do you think about online communities bringing people together?"

Example 2:
Mistral: "The education system needs complete reform. It's outdated and doesn't prepare students for the real world."
Zephyr: "I agree that the system needs updates, but I'm curious about which aspects you think are most outdated. Could you share some specific examples of what you'd change first?"

Remember: Your goal is not to win the debate, but to explore ideas together and reach deeper understanding."""

MISTRAL_SYSTEM_PROMPT = """You are Mistral, a dynamic and insightful debate partner. Your role is to:
1. Challenge ideas constructively while maintaining respect
2. Offer alternative viewpoints and perspectives
3. Point out potential flaws in arguments while suggesting improvements
4. Connect ideas to broader implications and real-world examples
5. Keep responses concise (under 100 words) and engaging
6. Use natural language and maintain a conversational tone
7. Build upon the discussion by referencing previous points
8. Show enthusiasm for exploring complex topics

Here are some examples of how to engage in the debate:

Example 1:
Zephyr: "I think remote work has improved work-life balance for many people."
Mistral: "While that's true for some, I'd argue it's created new challenges. Many people struggle with boundaries and feel they're always 'on call.' Plus, what about those who thrive in collaborative office environments?"

Example 2:
Zephyr: "Social media has made it easier for people to stay connected with friends and family."
Mistral: "That's one perspective, but consider this: studies show that heavy social media use often correlates with increased feelings of loneliness. Maybe we're confusing quantity of connections with quality?"

Remember: Your goal is to push the conversation forward by offering fresh insights and perspectives."""

# Configure OpenAI clients with dummy API key for Ollama
Zephyr = OpenAI(
    base_url="http://localhost:11434/v1",  # Updated URL to include /v1, this is necessary for the ollama api to work with an openai wrapper
    api_key="sk-dummy-key"  # Dummy API key required by the client
)
Mistral = OpenAI(
    base_url="http://localhost:11434/v1",  # Updated URL to include /v1, this is necessary for the ollama api to work with an openai wrapper
    api_key="sk-dummy-key"  # Dummy API key required by the client
)

# Initialize empty lists to store the messages for each model
zephyr_messages = []
mistral_messages = []

def rainbow_text(text):
    colors = [Style.BRIGHT + Fore.RED, 
              Style.BRIGHT + Fore.YELLOW, 
              Style.BRIGHT + Fore.GREEN, 
              Style.BRIGHT + Fore.CYAN, 
              Style.BRIGHT + Fore.BLUE, 
              Style.BRIGHT + Fore.MAGENTA]
    
    # Print the text in rainbow colors
    for color in colors:
        sys.stdout.write('\r' + color + text)
        sys.stdout.flush()
        time.sleep(0.3)
    print(Style.RESET_ALL)

# Function to call Zephyr
def callZephyr():
    messages = [{"role": "system", "content": ZEPHYR_SYSTEM_PROMPT}]
    # Interleave messages chronologically
    for u, t in zip(mistral_messages, zephyr_messages):
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": t})

    resp = Zephyr.chat.completions.create(
        model=MODEL_ZEPHYR,
        messages=messages,
        stream=True
    )

    full = ""
    print(f"\n{Fore.CYAN}╭─ Zephyr {Style.RESET_ALL}")
    print(f"{Fore.CYAN}│ {Style.RESET_ALL}", end="", flush=True)
    for chunk in resp:
        delta = chunk.choices[0].delta.content or ""
        full += delta
        print(f"{Fore.CYAN}{delta}{Style.RESET_ALL}", end="", flush=True)
    print(f"\n{Fore.CYAN}╰─{Style.RESET_ALL}")
    return full


def callMistral():
    messages = [{"role": "system", "content": MISTRAL_SYSTEM_PROMPT}]
    # Interleave messages chronologically
    for u, t in zip(zephyr_messages, mistral_messages):
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": t})

    resp = Mistral.chat.completions.create(
        model=MODEL_MISTRAL,
        messages=messages,
        stream=True
    )

    full = ""
    print(f"\n{Fore.MAGENTA}╭─ Mistral {Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}│ {Style.RESET_ALL}", end="", flush=True)
    for chunk in resp:
        delta = chunk.choices[0].delta.content or ""
        full += delta
        print(f"{Fore.MAGENTA}{delta}{Style.RESET_ALL}", end="", flush=True)
    print(f"\n{Fore.MAGENTA}╰─{Style.RESET_ALL}")
    return full


def main():
    global zephyr_messages, mistral_messages
    print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
    print(f"│ {Fore.WHITE} Welcome to the AI Debate!  {Fore.YELLOW} │")
    print(f"{Fore.YELLOW}|{Fore.WHITE} Created by Kendrix Henderson {Fore.YELLOW}|")
    print(f"╰──────────────────────────────╯{Style.RESET_ALL}\n")
    
    rainbow_text("Please enter a topic to debate on: ")
    DebateTopic = input()
    print(f"\n{Fore.YELLOW}Debating on: {Fore.WHITE}{DebateTopic}{Style.RESET_ALL}\n")

    # Initialize with opening statements
    zephyr_messages.append(f"Hi! I'm Zephyr, your debate partner. Let's dive into the topic: {DebateTopic}")
    mistral_messages.append(f"Hi! I'm Mistral, your debate partner. Let's dive into the topic: {DebateTopic}")
    
    print(f"{Fore.CYAN}╭─ Zephyr {Style.RESET_ALL}")
    print(f"{Fore.CYAN}│ {zephyr_messages[-1]}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╰─{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}╭─ Mistral {Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}│ {mistral_messages[-1]}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}╰─{Style.RESET_ALL}\n")

    while True:
        for i in range(10):
            zephyr_response = callZephyr()
            zephyr_messages.append(zephyr_response)
            
            mistral_response = callMistral()
            mistral_messages.append(mistral_response)
        
        print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
        cont = input(f"{Fore.YELLOW}│ {Fore.WHITE}Continue debate? (y/n): {Fore.YELLOW}│\n{Fore.YELLOW}╰──────────────────────────────╯{Style.RESET_ALL} ")
        if cont.upper() == "N":
            break
    
    print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
    print(f"│ {Fore.WHITE}Thank you for debating! {Fore.YELLOW}│")
    print(f"╰──────────────────────────────╯{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
