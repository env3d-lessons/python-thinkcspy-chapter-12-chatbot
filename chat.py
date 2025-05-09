
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Load pre-trained model and tokenizer
model_name = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)



"""
Returns a list of tokens sort by probabilities, highest comes first.
Second argument top_k controls how many possible tokens to return
"""
def complete(sentence, top_k = 10):    
    inputs = tokenizer(sentence, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    last_token_logits = logits[0, -1, :]
    probabilities = torch.nn.functional.softmax(last_token_logits, dim=-1)
    
    top_k_values, top_k_indices = torch.topk(probabilities, top_k)

    # Not decoding automatically
    # top_k_tokens = tokenizer.convert_ids_to_tokens(top_k_indices.tolist())
    # print(top_k_tokens)
    # result = [{"token": token.replace('Ġ', '').replace('Ċ','\n'), "probability": prob.item()} for token, prob in zip(top_k_tokens, top_k_values)]
    
    top_k_tokens = [tokenizer.decode([token_id]) for token_id in top_k_indices.tolist()]    
    result = [{"token": token, "probability": prob.item()} for token, prob in zip(top_k_tokens, top_k_values)]
    
    return top_k_tokens

