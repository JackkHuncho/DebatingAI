# AI Debate

A command-line tool that creates a debate between two AI models (Zephyr and Mistral) using Ollama. The models engage in a structured debate with distinct personalities and perspectives.

## Requirements

1. Python 3.7+
2. Ollama installed and running locally
3. Required Python packages (install via `pip install -r requirements.txt`):
   - openai>=1.0.0 (for Ollama API wrapper)
   - colorama>=0.4.6 (for terminal colors)

## Setup

1. Install Ollama from https://ollama.ai/
2. Pull the required models:
   ```bash
   ollama pull zephyr:7b
   ollama pull mistral:7b
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Make sure Ollama is running locally (default port: 11434)
2. Run the script:
   ```bash
   python DebatingAI.py
   ```
3. Enter a topic when prompted
4. Watch the AI models debate!
5. After 10 exchanges, choose to continue or end the debate

## Features

- Real-time streaming responses with color-coded output
- Natural conversation flow between AI models
- Distinct personalities:
  - Zephyr: Empathetic, focused on understanding and exploration
  - Mistral: Analytical, focused on challenging and improving arguments
- Interactive debate format with user control
- Beautiful CLI interface with colored output and box-drawing characters

## Technical Details

- Uses Ollama's OpenAI-compatible API endpoint
- Implements streaming for real-time response display
- Maintains conversation history for context
- Uses colorama for cross-platform terminal colors
- Implements few-shot prompting for better conversation quality

