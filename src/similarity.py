import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def get_sim(query_emb: np.ndarray, sent_embeds: np.ndarray, top_n: int=100):
    # query_emb = get_sentence_embeddings(text)
    sims = cosine_similarity(sent_embeds, query_emb).squeeze()
    sorted_idx = np.flip( np.argsort(sims, axis=0) )[:top_n].squeeze()
    pairs = np.array((sorted_idx, sims[sorted_idx])).T
    return pairs

