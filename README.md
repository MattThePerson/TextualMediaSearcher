# Audio Transcript Searcher

Program for searching for the most relevant segments withing transcripts of audio files (eg. Podcasts) using BERT model. Can handle English or Finnish. Can use sentence embeddings or weighted word embeddings for different results or types of queries. 

*NB: Can be configured to work with other languages*


## Requirements

1. **Python:** 3.7+
2. **openai-whisper:** This is required for generating transcripts of the audio files. `pipx install openai-whisper`
3. **VLC (optional):** This is required if you want to be able to jump directly to the relevant section of the podcast. 


## Setup

1. **Install requirements.txt**: `pip install -r requirements.txt`. Recommened to install PyTorch separately first
2. **Edit `config.yaml`:** Write path to folder containing your audio files (and optionally alternative HuggingFace BERT model). 
3. **Transcripts:** Generate transcripts using `transcribe.py`. To select language, use `--language [en|fi]`.
4. **Process transcripts:** Run `preprocess.py` to generate sentence and word embeddings. 


## Running

Run: `main.py "search query sentence here"`.

To select language, use `--language [en|fi]`.

