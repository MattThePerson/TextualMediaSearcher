import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np



# Finnish language embedding model
def get_model(model_name):
    # model_name = "TurkuNLP/bert-base-finnish-cased-v1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return model, tokenizer



def get_sentence_embeddings(sents: list[str]|str, model, tokenizer) -> np.ndarray:
    """ For a list of sentences return their BERT embeddings (numpy) """
    if not isinstance(sents, list):
        sents = [sents]
    inputs = tokenizer(sents, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.cpu().numpy()


# get sentence embeddings
def get_sentence_embeddings_batched(sents: list[str], model, tokenizer, batch_size=16) -> np.ndarray:
    """ For a list of sentences, process in batches and return their BERT embeddings (numpy) """
    sent_embeddings = np.zeros((len(sents), model.config.hidden_size), dtype="float32")
    for i in range(0, len(sents), batch_size):
        print(" {:>3}/{}".format(i, len(sents)))
        batch = sents[i : i+batch_size]
        batch_embeds = get_sentence_embeddings(batch, model, tokenizer)
        sent_embeddings[i:i+batch_size, :] = batch_embeds
    return sent_embeddings

