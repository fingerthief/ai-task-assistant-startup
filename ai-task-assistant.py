
import os
import json
from dotenv import load_dotenv
from interpreter import interpreter
# Load environment variables
load_dotenv()

# Configuration for model selection
model_configurations = {
    1: {"model": "gpt-4-turbo-preview", "temperature": 0.15, "context_window": 128000, "max_tokens": 4096, "api_key": os.getenv("GPT_API_KEY")},
    2: {"model": "claude-3-opus-20240229", "temperature": 0.15, "context_window": 200000, "max_tokens": 4096, "api_key": os.getenv("CLAUDE_API_KEY")},
    3: {"model": "claude-3-sonnet-20240229", "temperature": 0.15, "context_window": 200000, "max_tokens": 4096, "api_key": os.getenv("CLAUDE_API_KEY")},
    4: {"model": "claude-3-haiku-20240307", "temperature": 0.15, "context_window": 200000, "max_tokens": 4096, "api_key": os.getenv("CLAUDE_API_KEY")},
    5: {"model": "openai/x", "temperature": 0.15, "context_window": 16000, "max_tokens": 4096, "api_base": "http://localhost:1234/v1", "api_key": "lm-studio"}
}

def load_conversation(conversations_dir):
    """Load a conversation from the specified directory."""
    
    conversation_files = [f for f in os.listdir(conversations_dir) if f.endswith('.json')]
    conversation_files_sorted = sorted(conversation_files, reverse=True)

    for i, file in enumerate(conversation_files_sorted, start=1):
        print(f"{i}. {file}")

    selection = input("Enter the number of the conversation to load, or press enter to continue without loading: ")
    if selection:
        index = int(selection) - 1
        selected_file = conversation_files_sorted[index]
        conversation_path = os.path.join(conversations_dir, selected_file)
        
        with open(conversation_path, "r") as f:
            loaded_messages = json.load(f)
            
        print(f"Loaded conversation from {selected_file}")
        return loaded_messages
    else:
        print("Continuing without loading a conversation")
        return []

def configure_model(model_selection):
    """Configure the model based on user selection."""
    
    if model_selection in model_configurations:
        config = model_configurations[model_selection]
        
        # Assuming 'interpreter' and 'llm' are predefined objects in the script
        interpreter.llm.model = config["model"]
        interpreter.llm.temperature = config["temperature"]
        interpreter.llm.context_window = config["context_window"]
        interpreter.llm.max_tokens = config["max_tokens"]
        interpreter.llm.api_key = config["api_key"]
        
        if "api_base" in config:
            interpreter.llm.api_base = config["api_base"]
            
        print(f"Configured model: {config['model']}")
    else:
        print("Invalid model selection. Please restart and select a valid option.")

def main():
    conversations_dir = os.getenv("CONVERSATIONS_DIR")
    loaded_messages = load_conversation(conversations_dir)
    interpreter.messages = loaded_messages

    print("Select the model to use:")
    for key, value in model_configurations.items():
        print(f"{key}: {value['model']}")
        
    model_selection = int(input("Enter the model number: "))
    configure_model(model_selection)

    interpreter.auto_run = True
    messages = interpreter.chat()
    interpreter.messages = messages

if __name__ == "__main__":
    main()
