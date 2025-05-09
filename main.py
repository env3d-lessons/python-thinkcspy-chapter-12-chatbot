import tkinter as tk
from tkinter import ttk, scrolledtext
from chat import complete
from random import randint

# Your original functions
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



#### USER INTEFACE CODE - DO NOT MODIFY!! ####

# Tkinter UI
def run_completion():
    method = method_var.get()
    prompt = prompt_entry.get()
    try:
        num_tokens = int(tokens_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Please enter a valid integer for number of tokens.")
        return

    if method == "Greedy":
        result = greedy_complete(prompt, num_tokens)
    elif method == "Random":
        result = random_complete(prompt, num_tokens)
    elif method == "Worst":
        result = worst_complete(prompt, num_tokens)
    else:
        result = "Invalid method selected."

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

# Set up window
root = tk.Tk()
root.title("Sentence Completion")

# Prompt input
tk.Label(root, text="Prompt:").grid(row=0, column=0, sticky='w')
prompt_entry = tk.Entry(root, width=50)
prompt_entry.grid(row=0, column=1, columnspan=2, pady=5)

# Number of tokens
tk.Label(root, text="Number of tokens:").grid(row=1, column=0, sticky='w')
tokens_entry = tk.Entry(root, width=10)
tokens_entry.grid(row=1, column=1, sticky='w', pady=5)

# Method selection
tk.Label(root, text="Method:").grid(row=2, column=0, sticky='w')
method_var = tk.StringVar(value="Greedy")
method_menu = ttk.Combobox(root, textvariable=method_var, values=["Greedy", "Random", "Worst"], state="readonly")
method_menu.grid(row=2, column=1, pady=5, sticky='w')

# Run button
run_button = tk.Button(root, text="Complete", command=run_completion)
run_button.grid(row=3, column=0, columnspan=3, pady=10)

# Output display
output_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
output_text.grid(row=4, column=0, columnspan=3, pady=5)

root.mainloop()
