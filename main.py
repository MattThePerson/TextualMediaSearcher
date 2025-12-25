import argparse
import yaml
from pathlib import Path

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
    if True:
        for idx, sim in pairs[:5]:
            seg = segments[index2id[idx]]
            file = Path(seg.src).name
            print(" file={:<20}  |  start={:<6}  |  sim={:.4f}  |  text='{}'".format(file[:37], seg.start, sim, seg.text))


    # print segment neighbors
    if False:
        seg = segments[index2id[pairs[0][0]]]
        for i in range(5):
            print(seg.text)
            seg = segments[seg.next]


    # open segment in vlc
    if False:
        import subprocess
        print(seg.text)
        cmd = [
            "vlc",
            f"--start-time={seg.start}",
            seg.src,
        ]
        print(cmd)
        subprocess.Popen(cmd)



def time_to_seconds(t):
    parts = t.split(":")
    return sum(int(p) * 60 ** i for i, p in enumerate(reversed(parts)))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True)
    args = parser.parse_args()
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print()
    main(
        args.query,
        config['embedding_model'],
    )
    print()

