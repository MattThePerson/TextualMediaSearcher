# Textual Media Searcher

**Search Videos and Podcasts using Text**

Basic program for finding relevant sections withing video and audio files using their transcripts. Explore most the relevant transcript sections and even open media to transcript position with VLC! Transcripts generated with **openai-whisper** and language embedding done using **BERT** model. 


## Requirements

### System

- **Python:** 3.7+
- **Whisper:** This is required for generating transcripts of the audio files. Recommended: `pipx install openai-whisper`
- **VLC (optional):** This is required if you want to be able to jump directly to the relevant segment within the media. 


### Python

1. **PyTorch:** recommended to install first
2. **requirements.txt**: `pip install -r requirements.txt`


## Usage

1. **Edit the config:** Insert the paths to your *media_directories* into `config.yaml`. 

2. **Generate transcripts:** Generate transcripts using `transcribe.py`. Optionally: change language in the config (supports translation!)

3. **Generate embeddings:** Run `preprocess.py` to generate embeddings used for relevancy calculation. Optionally: change *embedding_model* in the config to another model from **Hugging Face**. 

4. **Run**: `main.py` and type in some queries!


## Ideas for future additions

- Alternative mode where word embeddings are used, possibly enabling better synonym based search. 

