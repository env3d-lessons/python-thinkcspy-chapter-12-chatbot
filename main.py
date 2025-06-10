from chat import chat

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