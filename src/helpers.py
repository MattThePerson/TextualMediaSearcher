import pickle


_SENT_EMBEDDINGS_PATH = "embeddings/sent_embeddings.pkl"

def load_sent_embeddings():
    with open(_SENT_EMBEDDINGS_PATH, "rb") as f:
        data = pickle.load(f)
    sent_embeddings = data['embeddings']
    index2id = data['index2id']
    return sent_embeddings, index2id


def save_sent_embeddings(sent_embeds, index2id):
    data = {
        "embeddings": sent_embeds,
        "index2id": index2id,
    }
    with open(_SENT_EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(data, f)


PATH_TO_NAME_MAP = {
    '/': '⁄',
    '\\': '⧵',
    ':': '꞉',
}

def path_to_name(x: str):
    """ given path, replace slashes such that can be used as a file/folder name """
    for k, v in PATH_TO_NAME_MAP.items():
        x = x.replace(k, v)
    return x

def name_to_path(x: str):
    for k, v in PATH_TO_NAME_MAP.items():
        x = x.replace(v, k)
    return x

