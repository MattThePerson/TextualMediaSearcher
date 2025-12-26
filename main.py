from pathlib import Path
import time
import yaml
import readline # this bullshit enabled ctrl+p
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

print("\nimporting libraries")
from src.segment import get_transcript_segments
from src.embedding import get_model_ST, get_sentence_embeddings
from src.helpers import load_sent_embeddings
from src.similarity import get_sim
from src.tui import enter_results_list_tui



def main(model_name: str):

    # transcripts
    segments, transcript_files = get_transcript_segments('transcripts')
    if len(transcript_files) == 0:
        print("\nNo transcript files found, edit media dirs in config.yaml and run transcribe.py")
        return 1
    print(f"\nfound {len(transcript_files)} transcripts (with {len(segments)} segments)\n")
    
    # load embeddings
    try:
        sent_embeds, index2id = load_sent_embeddings()
    except FileNotFoundError:
        print("\nNo segment embeddings found, run preprocess.py (once you have transcripts ready)")
        return 1

    
    # load model
    print(f"Loading model: {model_name}")
    start = time.time()
    model = get_model_ST(model_name)
    print("    took {:.2f}s\n".format(time.time()-start))
    
    
    # session
    kb = KeyBindings()

    @kb.add("c-q")
    def _(event):
        event.app.exit(result=None)
    
    session = PromptSession(key_bindings=kb)
    
    # Welcome
    print("\n #########################################")
    print(  " #                                       #")
    print(  " #   Welcome to Textual Media Searcher   #")
    print(  " #                                       #")
    print(  " #########################################\n\n")
    
    # LOOP
    while True:

        query = session.prompt("(give query) > ")
        if query is None:
            break
        if query == "":
            print("\nPlease provide a non-empty query")
            continue

        query_emb = get_sentence_embeddings(query, model)
        result_pairs = get_sim(query_emb, sent_embeds) # list((index, sim_score))

        enter_results_list_tui(
            segments,
            index2id,
            result_pairs,
        )

    return 0


if __name__ == "__main__":
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        main(
            config['models']['sentence_transformers'],
        )
    except KeyboardInterrupt:
        pass

    print("\n\nThank you, bye! <3\n")
