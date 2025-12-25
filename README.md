# Textual Media Searcher

**Search Videos and Podcasts with Text**

Program for searching for relevant segments withing video and audio files given a text query. Generates transcripts with **openai-whisper** and processes them with **BERT** model. 

*Supports English and Finnish.*


## Requirements

- **Python:** 3.7+
- **openai-whisper:** This is required for generating transcripts of the audio files. `pipx install openai-whisper`
- **VLC (optional):** This is required if you want to be able to jump directly to the relevant segment within the media. 


## 1. Setup

1. **Install requirements.txt**: `pip install -r requirements.txt`. Recommened to install PyTorch separately first
2. **Edit `config.yaml`:** Write paths to folders containing your audio files. Optionally, change langage or embeddings model. 


## 2. Preprocess

1. **Transcripts:** Generate transcripts using `transcribe.py`. To select language, use `--language [en|fi]`.
2. **Process transcripts:** Run `preprocess.py` to generate sentence and word embeddings. 


## 3. Usage (search)

Run: `main.py "search query sentence here"` to perform segments search and open TUI with navigable results. 

Can use `--mode` to switch between using sentence or word embeddings for the searching. 

