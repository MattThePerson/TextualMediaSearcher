import argparse
import yaml
import os

from src.segment import get_transcript_segments
from src.embedding import get_sentence_embeddings_batched, get_model
from src.helpers import save_sent_embeddings



def main(model_name: str):
    
    os.makedirs('embeddings', exist_ok=True)
    
    # process transcripts into usable form
    segments, _ = get_transcript_segments('transcripts')

    ids = list( segments.keys() )
    # id2index = { id_: idx for idx, id_ in enumerate(ids) }
    index2id = { idx : id_ for idx, id_ in enumerate(ids) }
    sents = [ segments[id_].text for id_ in ids ]
    
    # compute sentence embeddings
    model, tokenizer = get_model(model_name)
    sent_embeds = get_sentence_embeddings_batched(sents, model, tokenizer)
    
    save_sent_embeddings(sent_embeds, index2id)

    # compute word embeddings
    ...




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--language', default='fi', choices=['en', 'fi'], help='')
    args = parser.parse_args()
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    main(
        config['embedding_model'],
    )
