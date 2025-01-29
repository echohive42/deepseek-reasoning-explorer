# Interactive Reasoning Explorer 🤖

A powerful interactive tool that leverages DeepSeek's AI model to provide transparent reasoning processes and answers. This system allows users to explore the AI's thought process, ask follow-up questions, and dive deeper into explanations.

## Features ✨

- Real-time streaming of AI's reasoning process and final answers
- Interactive follow-up options for deeper exploration
- Ability to request detailed explanations of reasoning steps
- Support for concrete examples based on previous responses
- Conversation history management
- Color-coded output for better readability

## Prerequisites 🛠️

- Python 3.7+
- OpenRouter API key

## Installation 📦

1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenRouter API key as an environment variable:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Usage 🚀

Run the explorer:
```bash
python interactive_reasoning.py
```

### Interactive Options:

1. **Ask follow-up question**: Ask a new question based on previous response
2. **Explain reasoning**: Get detailed explanation of the AI's thought process
3. **Show examples**: Request concrete examples related to the reasoning
4. **Start new topic**: Begin a fresh conversation
5. **Exit**: End the session

## Example Session 💭 