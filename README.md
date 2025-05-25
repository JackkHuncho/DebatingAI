# DebatingAI

A Python-based AI debate system that facilitates structured discussions between two AI models (Zephyr and Mistral) using Ollama. The system provides a real-time, interactive debate experience with distinct AI personalities and perspectives.

## Features

- 🤖 **Dual AI Debate**: Engage two different AI models (Zephyr and Mistral) in a structured debate
- 🎨 **Colorful Interface**: Clear visual separation between speakers with color-coded responses
- 💬 **Real-time Streaming**: Watch the debate unfold in real-time with streaming responses
- 🔄 **Robust Error Handling**: Automatic retries and graceful error recovery
- 🎯 **Structured Conversation**: Maintains conversation history and context
- 🎭 **Distinct Personalities**: Each AI has a unique debating style and perspective

## Technical Details

### Architecture
- Object-oriented design with `DebateManager` class for state management
- Type-hinted code for better IDE support and maintainability
- Modular structure for easy extension and modification

### AI Models
- **Zephyr (7B)**: Empathetic and thoughtful debate partner
- **Mistral (7B)**: Dynamic and insightful counter-perspective
- Both models run locally via Ollama

### Error Handling
- Automatic retry mechanism for failed API calls
- Graceful degradation when responses fail
- Clear error messages and status updates

## Requirements

- Python 3.8 or higher
- Ollama installed and running locally
- Required Python packages (see requirements.txt)

## Setup

1. **Install Ollama**:
   ```bash
   # macOS/Linux
   curl https://ollama.ai/install.sh | sh
   ```

2. **Pull Required Models**:
   ```bash
   ollama pull zephyr:7b
   ollama pull mistral:7b
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama**:
   ```bash
   ollama serve
   ```

## Usage

1. Run the script:
   ```bash
   python DebatingAI.py
   ```

2. Enter a debate topic when prompted

3. Watch the AI models debate in real-time

4. Choose to continue or end the debate after each round

## Code Structure

```
DebatingAI/
├── DebatingAI.py      # Main application file
├── requirements.txt   # Python dependencies
└── README.md         # This documentation
```

### Key Components

- `DebateManager`: Core class managing debate state and AI interactions
- `call_ai()`: Generic method for AI model communication
- `add_message()`: Message history management
- `rainbow_text()`: UI enhancement for user prompts
