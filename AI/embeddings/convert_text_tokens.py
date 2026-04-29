from transformers import BertTokenizer,BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

text ="Gravity on Mars"

#1. Tokenize

token = tokenizer.tokenize(text)
print("Tokens:", token)

#2.Convert to IDs
ids = tokenizer.convert_tokens_to_ids(token)
print("Toeken IDs:", ids)

###############################
model =  BertModel.from_pretrained('bert-base-uncased')

#Convert IDS to tensor
inputs = tokenizer(text, return_tensors="pt")

#Get hidden states
outputs = model(**inputs)
last_hidden = outputs.last_hidden_state

print("Last hidden state:", last_hidden.shape)

sentence_embedding = last_hidden.mean(dim=1).squeeze()
print("Sentence embedding:", sentence_embedding.shape)
print("Emebedding Vector(first 10 dims):",sentence_embedding[:10])
