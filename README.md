# RAGsearch
Your personal Search Assistant
This App helps you search your documents.

# Requirements
- Python 3.10+
- And various Python packages listed in `requirements.txt`
- A working OpenAI API key

# Installation
run the following:
`pip install -r requirements.txt`

## Adding your OpenAI API key
Add your OpenAI API key to the `.env` file in the src directory of the project. The file should look like this: `.sample-env`. Rename it to `.env`

## Adding your documents and vectors folder
- You need to add your documents to the `documents` folder 
- You need to create a vector_store folder
Both folders should be created under the `src` folder in the project. 
The app will automatically index these documents and make them searchable.

## Choosing a llm model
You can choose a different LLM engine by modifying line 16 of `chat_agent.py`. The default is set to `gpt-3.5-turbo`.
