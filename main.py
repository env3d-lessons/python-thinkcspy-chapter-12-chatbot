from chat import chat

user = input('What country? ')
while user != 'exit':
    prompt = [
        {"role": "user", "content": "What is the capital of " + user + "?"} 
    ]
    print(chat(prompt))
    user = input('What country? ')

print('Goodbye')