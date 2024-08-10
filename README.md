# PDF_Answer_project
Small project to use LLM for finding information inside pdf files.

Use LangChanin for RAG and Ollama to get easy interaface for LLMs

# Start
1) Install Ollama for your system: https://ollama.com/download
2) Install models from ollama. Current version uses mistral:latest and mxbai-embed-large
```
ollama pull mxbai-embed-large
ollama pull mistral:latest
```
3) Install dependeces
```
pip install -r ./requirements.txt
```
4) Run StreamLit app
```
streamlit run .\app.py
```
