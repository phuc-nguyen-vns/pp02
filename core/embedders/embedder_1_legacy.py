# import os, sys

# import tiktoken
# import torch
# import torch.nn.functional as F
# from transformers import AutoTokenizer, AutoModel
# from pathlib import Path
# sys.path.append(Path(os.getcwd(),"PP02").as_posix())
# from api_configs import configs

# embedder_config = configs.embedder_1
# # Initialize tiktoken encoding
# encoding = tiktoken.get_encoding(embedder_config['encoder'])

# # Initialize embedding model
# # device = torch.device("mps")
# model = AutoModel.from_pretrained(embedder_config['pretrained_model'])
# tokenizer = AutoTokenizer.from_pretrained(embedder_config['tokenizer_model'])


# # Function to average pool the embeddings
# def average_pool(last_hidden_states, attention_mask):
#     last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
#     return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


# # Function to generate embeddings
# def embedding(text):
#     task_description = 'Represent this document for retrieval'
#     input_text = f'Instruct: {task_description}\nQuery: {text}'
    
#     # Tokenize the input text
#     batch_dict = tokenizer(input_text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    
#     # Generate embeddings
#     with torch.no_grad():
#         outputs = model(**batch_dict)
    
#     embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
    
#     # Normalize embeddings
#     embeddings = F.normalize(embeddings, p=2, dim=1)
    
#     return embeddings[0].tolist()


