## Overview
DebatingAI is a command-line interface (CLI) script that enables you to watch two AI models, Zephyr and Mistral, engage in a debate on any topic of your choice. The AIs use different perspectives and approaches to create an engaging and insightful discussion.

## Features
- Uses local Ollama models (no API keys required)
- Real-time streaming of AI responses
- Color-coded outputs for easy reading
- Interactive debate format
- Supports continuous back-and-forth discussion

## Prerequisites
- Python 3.x
- Ollama installed and running locally
- Required Python packages (install via `pip install -r requirements.txt`):
  - OpenAI
  - subprocess
  - colorama

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/DebatingAI.git
   cd DebatingAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is installed and running with the required models:
   ```bash
   ollama pull zephyr:7b
   ollama pull mistral:7b
   ```

## Usage
1. Run the script:
   ```bash
   python DebatingAI.py
   ```

2. Enter a topic when prompted
3. Watch as Zephyr (cyan) and Mistral (magenta) debate the topic
4. After 10 exchanges, you'll be asked if you want to continue
5. Type 'y' to continue or 'n' to end the debate

## How it Works
- Zephyr is configured to be objective and focused on creating deeper understanding
- Mistral is configured to be more analytical and point out flaws in arguments
- Both models maintain a respectful and constructive dialogue
- The debate continues in rounds of 10 exchanges until you choose to end it

## Contributing
Feel free to open issues or submit pull requests to improve this project.

## License
This project is open source and available under the MIT License.
