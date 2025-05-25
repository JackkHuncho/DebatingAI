from openai import OpenAI # API call wrapping for ollama
from colorama import Fore, Style, init as colorama_init
import time
import sys
from typing import List, Dict, Optional

colorama_init(autoreset=True)           # makes ANSI colours work on Windows, too

MODEL_ZEPHYR = "zephyr:7b" # 7b is the size of the model
MODEL_MISTRAL = "mistral:7b" # using mistral as the second debater
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

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
"That's an interesting point about isolation. I've noticed that too, but I wonder if technology might also be creating new forms of connection? What do you think about online communities bringing people together?"

Example 2:
"I agree that the system needs updates, but I'm curious about which aspects you think are most outdated. Could you share some specific examples of what you'd change first?"

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
"While that's true for some, I'd argue it's created new challenges. Many people struggle with boundaries and feel they're always 'on call.' Plus, what about those who thrive in collaborative office environments?"

Example 2:
"That's one perspective, but consider this: studies show that heavy social media use often correlates with increased feelings of loneliness. Maybe we're confusing quantity of connections with quality?"

Remember: Your goal is to push the conversation forward by offering fresh insights and perspectives."""

class DebateManager:
    def __init__(self):
        self.zephyr_messages: List[str] = []
        self.mistral_messages: List[str] = []
        self.zephyr_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="sk-dummy-key"
        )
        self.mistral_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="sk-dummy-key"
        )

    def call_ai(self, client: OpenAI, model: str, system_prompt: str, 
                user_messages: List[str], ai_messages: List[str], 
                color: str, name: str) -> Optional[str]:
        """Call an AI model with retry logic and proper error handling."""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Build message history in chronological order
        for i in range(max(len(user_messages), len(ai_messages))):
            if i < len(user_messages):
                messages.append({"role": "user", "content": user_messages[i]})
            if i < len(ai_messages) and ai_messages[i]:
                messages.append({"role": "assistant", "content": ai_messages[i]})

        for attempt in range(MAX_RETRIES):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True
                )

                full = ""
                print(f"\n{color}╭─ {name} {Style.RESET_ALL}")
                print(f"{color}│ {Style.RESET_ALL}", end="", flush=True)
                
                for chunk in resp:
                    delta = chunk.choices[0].delta.content or ""
                    delta = delta.replace('\n', ' ')
                    full += delta
                    print(f"{color}{delta}{Style.RESET_ALL}", end="", flush=True)
                
                print(f"\n{color}╰─{Style.RESET_ALL}")
                print()
                return full

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"{Fore.YELLOW}Retrying {name}... (Attempt {attempt + 1}/{MAX_RETRIES}){Style.RESET_ALL}")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"{Fore.RED}Error with {name}'s response: {str(e)}{Style.RESET_ALL}")
                    return None

    def call_zephyr(self) -> Optional[str]:
        """Call Zephyr with the current message history."""
        return self.call_ai(
            self.zephyr_client, 
            MODEL_ZEPHYR, 
            ZEPHYR_SYSTEM_PROMPT,
            self.mistral_messages,  # Zephyr responds to Mistral's messages
            self.zephyr_messages,
            Fore.CYAN,  # Zephyr is CYAN
            "Zephyr"
        )

    def call_mistral(self) -> Optional[str]:
        """Call Mistral with the current message history."""
        return self.call_ai(
            self.mistral_client,
            MODEL_MISTRAL,
            MISTRAL_SYSTEM_PROMPT,
            self.zephyr_messages,  # Mistral responds to Zephyr's messages
            self.mistral_messages,
            Fore.MAGENTA,  # Mistral is MAGENTA
            "Mistral"
        )

    def add_message(self, message: Optional[str], is_zephyr: bool) -> None:
        """Add a message to the appropriate history."""
        if is_zephyr:
            self.zephyr_messages.append(message or "")
        else:
            self.mistral_messages.append(message or "")

def rainbow_text(text: str) -> None:
    """Display text in cycling rainbow colors."""
    colors = [
        Style.BRIGHT + Fore.RED,
        Style.BRIGHT + Fore.YELLOW,
        Style.BRIGHT + Fore.GREEN,
        Style.BRIGHT + Fore.CYAN,
        Style.BRIGHT + Fore.BLUE,
        Style.BRIGHT + Fore.MAGENTA
    ]
    
    for color in colors:
        sys.stdout.write('\r' + color + text)
        sys.stdout.flush()
        time.sleep(0.3)
    print(Style.RESET_ALL)

def main():
    debate = DebateManager()
    
    # Welcome message
    print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
    print(f"│ {Fore.WHITE} Welcome to the AI Debate!  {Fore.YELLOW} │")
    print(f"{Fore.YELLOW}|{Fore.WHITE} Created by Kendrix Henderson {Fore.YELLOW}|")
    print(f"╰──────────────────────────────╯{Style.RESET_ALL}\n")
    
    # Get debate topic
    rainbow_text("Please enter a topic to debate on: ")
    debate_topic = input()
    print(f"\n{Fore.YELLOW}Debating on: {Fore.WHITE}{debate_topic}{Style.RESET_ALL}\n")

    # Initial messages
    initial_zephyr = f"Hi! I'm Zephyr, your debate partner. Let's dive into the topic: {debate_topic}"
    initial_mistral = f"Hi Zephyr, I'm Mistral, your debate partner. What do you have to say about {debate_topic}?"
    
    debate.add_message(initial_zephyr, True)
    debate.add_message(initial_mistral, False)
    
    # Display initial messages
    print(f"{Fore.CYAN}╭─ Zephyr {Style.RESET_ALL}")
    print(f"{Fore.CYAN}│ {initial_zephyr}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╰─{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.MAGENTA}╭─ Mistral {Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}│ {initial_mistral}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}╰─{Style.RESET_ALL}")
    print()

    # Main debate loop
    while True:

        zephyr_response = debate.call_zephyr()
        debate.add_message(zephyr_response, True)
        
        mistral_response = debate.call_mistral()
        debate.add_message(mistral_response, False)

        print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
        cont = input(f"{Fore.YELLOW}│ {Fore.WHITE}Continue debate? (y/n): {Fore.YELLOW}     │\n{Fore.YELLOW}╰──────────────────────────────╯{Style.RESET_ALL} ")
        if cont.upper() == "N":
            break
    
    print(f"\n{Fore.YELLOW}╭──────────────────────────────╮")
    print(f"│ {Fore.WHITE}Thank you for debating! {Fore.YELLOW}     │")
    print(f"╰──────────────────────────────╯{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
