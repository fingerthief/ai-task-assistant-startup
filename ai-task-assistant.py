
from dotenv import load_dotenv

from interpreter import interpreter
import os               
import json    

isGPT = True
modelSelection = input("\r\n Select a model: \r\n \r\n 1.) GPT-4-Turbo \r\n 2.) Claude 3 Opus ")

if modelSelection == 1:
    isGPT = True;
elif modelSelection == 2:
    isGPT = False

print("Loading conversations...")

load_dotenv()

# Get the list of conversation files and their last modified times
conversations_dir = os.getenv("CONVERSATIONS_DIR")       
conversation_files = os.listdir(conversations_dir)                         
conversation_files_with_times = [(file, os.path.getmtime(os.path.join(conversations_dir, file))) for file in conversation_files]

# Sort the files by last modified time, most recent first
conversation_files_sorted = sorted(conversation_files_with_times, key=lambda x: x[1], reverse=True)

# Display the list of conversations and prompt the user to select one                         
print("Saved conversations:")                         
for i, (filename, _) in enumerate(conversation_files_sorted, start=1):                         
    print(f"{i}. {filename}")                         

selection = input("Enter the number of the conversation to load, or press Enter to continue without loading: ")                         

if selection:                         
    # Load the selected conversation                         
    index = int(selection) - 1                         
    selected_file = conversation_files_sorted[index][0]                         
    conversation_path = os.path.join(conversations_dir, selected_file)                         

    with open(conversation_path, "r") as f:                         
        loaded_messages = json.load(f)                         

    interpreter.messages = loaded_messages                         
    print(f"Loaded conversation from {selected_file}")                         
else:                         
    print("Continuing without loading a conversation")                         

# Rest of the task-assistant.py startup code goes here

if isGPT: 
    interpreter.llm.api_key = os.getenv("GPT_API_KEY")
    interpreter.llm.model = "gpt-4-turbo-preview"
    interpreter.llm.temperature = 0.3
    interpreter.llm.context_window = 128000
    interpreter.llm.supports_vision = True
    interpreter.llm.supports_functions = True
else: #other model you want to use
    interpreter.llm.model = "claude-3-opus-20240229"
    interpreter.llm.api_key = os.getenv("CLAUDE_API_KEY")
    interpreter.llm.temperature = 0.20
    interpreter.llm.context_window = 200000
    interpreter.llm.supports_vision = False
    
interpreter.llm.max_tokens = 4096
interpreter.auto_run = True

messages = interpreter.chat()

interpreter.messages = messages