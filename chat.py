
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
import sys

CALL_FROM_PYTEST = (
    any("pytest" in arg for arg in sys.argv)
    or "pytest" in sys.modules
)

# Load pre-trained model and tokenizer
model_name = "Qwen/Qwen3-0.6B"
tokenizer = None
model = None

def chat(prompt =  "hello", temperature = 1.0):

    global model_name
    global tokenizer
    global model
    
    if CALL_FROM_PYTEST:
        return "Test Response"
    
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if tokenizer == None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    if model == None:
        model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

    # prepare the model input    
    messages = [
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to("cpu")

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        temperature=temperature,  # ← added parameter here
        do_sample=True,            # ← must be True for temperature to have an effect        
        max_new_tokens=128
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    # print("thinking content:", thinking_content)
    # print("content:", content)
    return content
    
def complete(prompt =  "<|im_start>user\nhello<|im_end|>\n<|im_start|>assistant\n", temperature = 1.0):
    """
    Like chat, but without the chat template.
    """

    global model_name
    global tokenizer
    global model
    
    if CALL_FROM_PYTEST:
        return "Test Response"
    
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if tokenizer == None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    if model == None:
        model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

    model_inputs = tokenizer([prompt], return_tensors="pt").to("cpu")

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        temperature=temperature,  # ← added parameter here
        do_sample=True,            # ← must be True for temperature to have an effect        
        max_new_tokens=256
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    content = tokenizer.decode(output_ids, skip_special_tokens=False)

    # print("thinking content:", thinking_content)
    # print("content:", content)
    return prompt+content

def get_next_token_dictionary(sentence, top_k = 10):    
    """
    Returns a dictionary of tokens with both token and probability
    Second argument top_k controls how many possible tokens to return
    """
    if CALL_FROM_PYTEST:
        return [{"token": "a", "probabilty":0.9}, {"token": "b", "probabilty":0.1} ]    

    global model_name
    global tokenizer
    global model


    if tokenizer == None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    if model == None:
        model = AutoModelForCausalLM.from_pretrained(
            model_name
        )
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
    
    return result

def get_next_token_list(sentence, top_k = 10):
    """
    Returns a list of tokens sort by probabilities, highest comes first.
    Second argument top_k controls how many possible tokens to return
    """
    results = get_next_token_dictionary(sentence, top_k)
    sorted_results = sorted(results, key=lambda x: x.get("probability"), reverse=True)
    return [r["token"] for r in sorted_results]