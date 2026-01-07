from api_client import MistralClient

def main():
    client = MistralClient()
    messages = []
    
    print("Welcome to the Mistral CLI Chat! (Type 'exit' to quit)")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            # Add user message to history
            messages.append({"role": "user", "content": user_input})

            print("Bot: Thinking...", end="\r")
            
            # Get response
            response = client.send_prompt(messages)
            
            # Clear "Thinking..."
            print(" " * 20, end="\r")
            
            print(f"Bot: {response}")

            # Add assistant message to history to maintain context
            messages.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
