import argparse
import yaml

print("importing")
from src.segment import get_transcript_segments
from src.embedding import get_model, get_sentence_embeddings
from src.helpers import load_sent_embeddings
from src.similarity import get_sim



def main(query: str, model_name: str):
    
    # load shit
    print('loading')
    model, tokenizer = get_model(model_name)
    segments = get_transcript_segments('transcripts')
    sent_embeds, index2id = load_sent_embeddings()
    
    # find similar
    print('computing')
    query_emb = get_sentence_embeddings(query, model, tokenizer)
    pairs = get_sim(query_emb, sent_embeds) # list((index, sim_score))
    
    # print shit
    for idx, sim in pairs[:5]:
        seg = segments[index2id[idx]]
        print(f"{sim:.4f}  |  {seg.text}")
    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query')
    args = parser.parse_args()
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print()
    main(
        args.query,
        config['embedding_model'],
    )
    print()
