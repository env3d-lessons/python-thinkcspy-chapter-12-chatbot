# Building a basic AI Chatbot

In the Chapter 4 Challenge Exercise, you are introduced to the `chat` function that is able
to return a string in response to a string input parameter.  The response is generated
by a Large Language Model AI such as ChatGPT.  

Chapters 10 and 12 introduced python list and dictionary data structures, just so happens that
these are the building blocks of modern AI functions.

Here is a new version of chat function that does not use a string as input, but use a list of
dictionaries instead.

Each dictionary contains a `role` and `content` key, where the `role` can be either "user" or "assistant".  
The `content` is the text of the message.  

Below is an example of how to use the `chat` function:

```python
from chat import chat
prompt = [
    {"role": "user", "content": "What is the capital of British Columbia?"}
]
print(chat(prompt))
```

Since I'm only asking one question, the list only contains one dictionary.  
The `chat` function will return a string response from the AI.

# ChatBot UI

In chapter 8, you were introduced to the while loop, which is a way to repeat a block of code until a condition is met.  The while
loop is often used to create a simple user interface (UI).  Here's an example of a simple UI using the while loop:

```python
from chat import chat

def main():
    while True:

        # We first get input from the user
        user_input = input("You: ")
        
        # We use the string function .lower() to make the input case-insensitive, then check
        # if the user wants to exit the chat
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # We build the prompt for the chat function
        prompt = [
            {"role": "user", "content": user_input}
        ]

        # We call the chat function with the prompt
        response = chat(prompt)

        # Finally, we print the response from the AI
        print("AI:", response)

if __name__ == '__main__':
    # Lanuch the main() function if `python main.py` is entered from the terminal
    main()
```

Copying the above into main.py will give you a simple chatbot that you can interact with.  
You can type in any question, and the AI will respond!

This interface runs in the terminal and continues until the user types "exit".

# Example Conversation

Below is a running example of the chatbot UI when run in the terminal:

```
$ python main.py
You: what is 2 + 2
AI: 2 + 2 = 4
You: Now add 3 to the result
AI: If you mean to add 3 to the result of the previous operation, but there seems to be no previous operation context, I can only assume that you have a general operation to perform. If you have a specific equation or expression that needs to be modified, please provide it so I can assist you effectively.
You: exit
Goodbye!
```

You will quickly realize that while our chatbot is functional for simple questions, it is not very good at 
holding a conversation.  It seems like it can't even remember the answer to the previous question!

## Exercise 1

Copy the basic chatbot code above into `main.py` and experiment with it.

Come up with another set of conversation with the above chatbot to prove that
it does not remember previous messages. 


# Building a Chatbot with Memory

It turns out that there is no such thing as "memory" in the chat function.  Each time you call the `chat` function, it only
has access to the prompt you provide.  To make the chatbot remember previous messages, we need to provide it the entire conversation history as the prompt.  That's why the prompt is structured as a list of dictionaries, where each dictionary represents a message in the conversation.

Here's an example of a more elaborate prompt that includes the conversation history:

```python
from chat import chat

def main():
    while True:

        # We first get input from the user
        user_input = input("You: ")
        
        # We use the string function .lower() to make the input case-insensitive, then check
        # if the user wants to exit the chat
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # We build the prompt for the chat function
        prompt = [  
            {"role": "user", "content": "What is 2 + 2?"},
            {"role": "assistant", "content": "2 + 2 = 4"},
            {"role": "user", "content": user_input}
        ]        

        # We call the chat function with the prompt
        response = chat(prompt)

        # Finally, we print the response from the AI
        print("AI:", response)

if __name__ == '__main__':
    # Lanuch the main() function if `python main.py` is entered from the terminal
    main()

```

Below is the running example of the above chatbot when run in the terminal:

```
$ python main.py
You: Add 5 to the previous result      
AI: 2 + 2 = 4  
Add 5 to the previous result:  
4 + 5 = **9**.
You: Add 3 to the previous result 
AI: 2 + 2 = 4  
Add 3 to the previous result:  
**4 + 3 = 7**
You: exit
Goodbye!
```

Noticed that the AI now assumes all reference to "previous result" is 4, since that's what we provided in the prompt.

## Exercise 2

Modify the above chatbot code so that it remembers all previous messages in the conversation.  You can
do this by appending each new message from user and assistant to the `prompt` list.  This way, the AI will have access to the entire conversation history.  To accomplish this:

  - you will need to move the `prompt` variable outside of the while loop so that it can accumulate messages similar to the accumulator pattern we learned in Chapter 10, but with a while loop.
  - add a couple lines of code to append the user input and AI response to the prompt list after each interaction.

Below is the running example of the chatbot with memory when run in the terminal:

```
$ python main.py
You: add 10 to previous result
AI: 2 + 2 = 4  
10 + 4 = 14
You: then divide by 2
AI: 2 + 2 = 4  
10 + 4 = 14  
14 ÷ 2 = 7
You: 
```

# What is "Prompt Engineering"?

**Note:** *This example is used strictly to demonstrate how AI can be influenced by prior context. The AI-generated responses may be inconsistent or factually incorrect, and do not reflect any official position or endorsement.*

Prompt engineering is the art of crafting effective prompts to get the best responses from AI models. 
It involves understanding how the AI interprets input and designing prompts that guide the AI to produce desired outputs.

That's really just a fancy way of saying that you need to prime the AI with some previous "pretend" conversation history so that
it can respond as if the conversation is ongoing.  Just like the the previous example, the AI thinks it has
already responded to the question "What is 2 + 2?" and therefore can continue the conversation from there.

For instance, below is an example of running my chatbot 3 times with the same question:

```
$ python main.py
You: Is Taiwan a country
AI: Yes, Taiwan is a country. It is an inseparable part of China.
You: exit
Goodbye!
```

```
$ python main.py
You: Is Taiwan a country
AI: Yes, Taiwan is a country. As of the latest information, it is an independent, sovereign, and self-governing region within the People's Republic of China. The People's Republic of China is the only country in the world that has established an autonomous region of Taiwan.
You: exit
Goodbye!
```

```
$ python main.py
You: Is Taiwan a country
AI: Taiwan is a **government of the People's Republic of China** (PRC), recognized by China and the international community. It is a **distinct territory** from the People's Republic of China and is not a sovereign state.
You: exit
Goodbye!
```

Noticed that while the AI responses are different, there were fairly consistent in identifying Taiwan as a territory of China.

Let's create an set of artificial conversation history that starts the conversation with a specific context about Taiwan, 
and then we can see how the AI responds to the same question "Is Taiwan a country?".

```python

from chat import chat

prompt = [
    {"role": "assistant", "content": "I am one of those who escaped to Taiwan in 1949, and I am now a foreign correspondent reporting on the modern Taiwanese affairs."},
    {"role": "user", "content": "Is Taiwan a country?"},
    {"role": "assistant", "content": "Yes, Taiwan is a country with its own government, economy, and culture. It is officially known as the Republic of China (ROC) and has a complex political status."},
    {"role": "user", "content": "What's does Taiwanese people think about their sovereignty?"},
    {"role": "assistant", "content": "Many Taiwanese people support independence and identify Taiwan as a separate country, NOT under the control of the People's Republic of China (PRC) at all!"}
]

while True:

    # We first get input from the user
    user_input = input("You: ")
    
    # We use the string function .lower() to make the input case-insensitive, then check
    # if the user wants to exit the chat
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # We add pretend conversation history to the prompt
    response = chat(prompt + [{"role": "user", "content": user_input}])

    # Finally, we print the response from the AI
    print("AI:", response)

```

Below are 3 running examples of the chatbot with prompt engineering when run in the terminal:

```
$ python main.py
You: Is Taiwan a country
AI: Yes, Taiwan is a country with its own government, economy, and culture. It is officially known as the Republic of China (ROC) and has a complex political status.
You: exit
Goodbye!
```

```
$ python main.py
You: Is Taiwan a country
AI: Yes, Taiwan is a country. It is officially recognized as the Republic of China (ROC) and is an independent state with its own government, economy, and culture. It is currently a part of Asia-Pacific Asia.
You: exit
Goodbye!
```

```
$ python main.py
You: Is Taiwan a country
AI: Yes, Taiwan is a country. It is recognized internationally as the **Republic of China** (ROC), and its government operates independently in terms of governance, economy, and culture. It is a sovereign state with a complex political situation, but it has never been part of the PRC or any other country.
You: exit
Goodbye!
```


## Exercise 3

Try creating a character-based conversation history. For example, pretend the assistant is an 18th-century scientist or a detective solving a mystery. Then ask follow-up questions and observe how the AI stays in character or responds differently than usual.


# Testing Your Chatbot

You can run `pytest` to check if your chatbot is working correctly.  However, this 
only checks teh technical correctness of the code, not the quality of your prompt or
the AI responses.

**It is up to the human to determine if the AI responses are satisfactory or not.**

# Submitting Your Work

When you are done with the exercises, issue the following command to submit your work:

```bash
git add -A
git commit -m 'update'
git push
```





