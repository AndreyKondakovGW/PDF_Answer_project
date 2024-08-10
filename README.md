# PDF_Answer_project
A small project on using LLM to search for information in PDF files.

Use LangChanin for RAG and Ollama to get a simple interface for LLMs

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

Adding a file may take some time, especially if you are adding a large file
