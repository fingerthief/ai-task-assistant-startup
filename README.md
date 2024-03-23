# ai-tasks-assistant-startup
A startup file for launching an Open Interpreter session. On startup a list of saved conversations is shown that the user can load and continue to work from. If no selection is made a new conversation will be started.

# Setup
Run `pip install -r requirements.txt`to install any packages needed

create a `env` file with the following keys:

- **GPT_API_KEY**
- **CLAUDE_API_KEY**
- **CONVERSATIONS_DIR** By default the conversation files are stored in `appdata --> open-interpreter` for the user.

Now you should be able to run the file and go on your merry way.
