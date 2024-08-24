import tiktoken
import torch
from torch.utils.data import Dataset, DataLoader

class DatasetV1(Dataset):
    def __init__(self, tokenizer, txt, max_length, stride):
        self.input_ids = []
        self.target_ids = []
        #tokenizer entire txt
        token_ids = tokenizer.encode(txt,allowed_special= {"<|endoftext|>"})
        # Use a sliding window to chunk the book into overlapping sequences of max_length
        for i in range(0,len(token_ids)-max_length, stride):
            input_chunk = token_ids[i:i+max_length]
            target_chunk = token_ids[i+1: i+max_length+1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))
    def __len__(self):
        return len(self.input_ids)
    def __getitem__(self, index):
        return self.input_ids[index], self.target_ids[index]
    

def create_dataloader_v1(txt, batch_size = 4, max_length = 256, stride = 128, 
                         shuffle = True, drop_last = True, num_worker = 0):
    tokenizer = tiktoken.get_encoding('gpt2')
    dataset = DatasetV1(tokenizer, txt,max_length, stride)
    dataloader = DataLoader(dataset, batch_size=batch_size, drop_last=drop_last, shuffle=shuffle)
    return dataloader

with open('the-verdict.txt', 'r') as f:
    raw_text = f.read()

tokenizer = tiktoken.get_encoding("gpt2")
encoded_text = tokenizer.encode(raw_text)

vocab_size = 50257
output_dim = 256
context_length = 1024

token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)

max_length = 4
dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=max_length, stride=max_length)

for (x,y) in dataloader:
    token_embedding = token_embedding_layer(x)
    print('token_embedding: ', token_embedding)
    pos_embedidng = pos_embedding_layer(torch.arange(max_length))
    print('pos_embedding: ', pos_embedidng)
    input_embeddings = token_embedding + pos_embedidng
    print('input_emdefing: ',input_embeddings )
    break
