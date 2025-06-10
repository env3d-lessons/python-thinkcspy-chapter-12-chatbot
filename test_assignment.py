import pytest
from unittest.mock import patch
from main import main

# Helper to simulate input() and capture print()
def run_main_with_inputs(inputs):
    output = []
    def fake_input(prompt=None):
        return inputs.pop(0)
    def fake_print(*args, **kwargs):
        output.append(' '.join(str(a) for a in args))
    with patch('builtins.input', side_effect=fake_input), \
         patch('builtins.print', side_effect=fake_print):
        main()
    return output

def test_main_exit():
    # Should print goodbye and exit immediately
    out = run_main_with_inputs(['exit'])
    assert any('Goodbye!' in line for line in out)

def test_main_chat():
    # Should call chat and print AI response, then exit
    out = run_main_with_inputs(['hello', 'exit'])    
    # Should see the prompt and the AI response
    assert any('hello' in line for line in out)
    assert any('Goodbye!' in line for line in out)

def test_main_chat_with_memory():
    # Should call chat and print AI response, then exit
    commands = ['hello', 'test', 'exit']
    out = run_main_with_inputs(commands[:])    
    # Make sure the entire conversation history is on one of the lines    
    # Use regex to check if all commands are present in the output
    regex = '.*'.join(commands[:-1])  # Exclude 'exit'
    import re
    assert any(re.search(regex, line) for line in out)        
    assert any('Goodbye!' in line for line in out)    

def test_main_chat_with_fake_history():
    # Should call chat and print AI response, then exit
    commands = ['hello', 'exit']
    out = run_main_with_inputs(commands[:])    
    # Make sure we have some additional history after first command
    # we do this by counter the number of the words 'content' in the output
    assert out[0].count('content') > 1
