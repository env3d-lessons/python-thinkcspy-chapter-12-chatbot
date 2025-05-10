import gradio as gr
from chat import complete
from random import randint

# Original functions
def greedy_complete(sentence, num_tokens):    
    for _ in range(num_tokens):
        sentence += complete(sentence)[0]        
    return sentence

def random_complete(sentence, num_tokens):
    for _ in range(num_tokens):
        choices = complete(sentence)
        sentence += choices[randint(0, len(choices)-1)]        
    return sentence

def worst_complete(sentence, num_tokens):
    for _ in range(num_tokens):
        sentence += complete(sentence)[-1]        
    return sentence



### DO NOT MODIFY - UI Code ###

# Wrapper to pick method
def complete_text(prompt, num_tokens, method):
    if method == "Greedy":
        return greedy_complete(prompt, num_tokens)
    elif method == "Random":
        return random_complete(prompt, num_tokens)
    elif method == "Worst":
        return worst_complete(prompt, num_tokens)
    else:
        return "Invalid method selected."

# Gradio UI setup
with gr.Blocks() as demo:
    gr.Markdown("## Sentence Completion Tool")
    prompt = gr.Textbox(label="Prompt", value="It's the best of times, it's the worst of")
    num_tokens = gr.Slider(1, 50, value=10, step=1, label="Number of Tokens")
    method = gr.Radio(choices=["Greedy", "Random", "Worst"], value="Greedy", label="Completion Method")
    output = gr.Textbox(label="Completed Sentence")

    run_button = gr.Button("Complete Sentence")
    run_button.click(fn=complete_text, inputs=[prompt, num_tokens, method], outputs=output)

demo.launch()
