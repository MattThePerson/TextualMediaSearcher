# Textual Media Searcher

**Search Videos and Podcasts using Text**

Basic program for finding relevant sections in videos and podcasts by doing semantic search of transcripts. Explore the most relevant transcript segments and even open the media at that position with VLC!

Semantic search is done with a **sentence transformers** model, of which there are several options to chose from. Transcripts are generated using **Whisper**. 


## Requirements

### System

- **Python:** 3.7+
- **Whisper:** Transcript generation. Recommended: `pipx install openai-whisper`
- **VLC (optional):** Required if you want to be able to directly open the relevant segment within the media. 


### Python

1. **PyTorch:** recommended to install first
2. **requirements.txt**: `pip install -r requirements.txt`


## Usage

1. **Edit the config:** Insert the paths to your *media_directories* into `config.yaml` (if multiple directories, make list with hyphens `-`)

2. **Generate transcripts:** Generate transcripts using `transcribe.py`. Optionally: change language in the config (supports translation!)

3. **Generate embeddings:** Run `preprocess.py` to generate embeddings used for relevancy calculation. Optionally: switch to another sentence transformer model in the config. 

4. **Run**: `main.py` and start typing!


## Ideas for future additions

- Alternative mode where word embeddings are used (eg. Word2Vec, FastText, GloVe), possibly enabling better synonym based search. 
- Add searching of generated transcript files in the TUI. 
