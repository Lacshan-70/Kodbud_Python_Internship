"""
Simple CLI Chatbot
"""
import sys
from chatbot_logic import get_response


def main():
    print("Welcome to the Simple CLI Chatbot!")
    print("Type 'help' for suggestions, or 'exit' / 'quit' to leave.\n")

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                print("Bot: I didn't catch that — could you say it again?")
                continue

            response = get_response(user_input)
            print(f"Bot: {response}")

            # If the user asked to exit, break loop
            normalized = user_input.strip().lower()
            if normalized in ("exit", "quit") or normalized.startswith("bye") or normalized.startswith("goodbye"):
                break

    except KeyboardInterrupt:
        print("\nBot: Goodbye!")
        sys.exit(0)


if __name__ == '__main__':
    main()
