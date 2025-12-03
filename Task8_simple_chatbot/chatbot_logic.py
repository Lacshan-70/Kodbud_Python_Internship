"""
Simple rule-based chatbot logic module
"""
from datetime import datetime
import re


def normalize_text(text: str) -> str:
    """Lowercase, strip, and remove extra punctuation for simple matching."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    # remove repeated whitespace
    text = re.sub(r"\s+", " ", text)
    # remove surrounding punctuation
    text = text.strip("""'\".?!,;:""")
    return text


def get_response(user_input: str) -> str:
    """Return a rule-based response for the given user input."""
    text = normalize_text(user_input)

    if not text:
        return "I didn't catch that — could you say it again?"

    # Greetings
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(text.startswith(g) or text == g for g in greetings):
        return "Hello! How can I help you today?"

    # Farewells
    farewells = ["bye", "goodbye", "see you", "quit", "exit"]
    if any(text.startswith(f) or text == f for f in farewells):
        return "Goodbye! Have a great day!"

    # Thanks
    thanks = ["thanks", "thank you", "thx"]
    if any(t in text for t in thanks):
        return "You're welcome! Happy to help."

    # How are you
    if text in ("how are you", "how are you?", "how're you"):
        return "I'm a simple chatbot, but I'm doing great — thanks for asking!"

    # Name
    if "your name" in text or text.startswith("what are you called") or text.startswith("who are you"):
        return "I'm a simple CLI chatbot created to demonstrate rule-based responses."

    # Capabilities / Help / FAQ
    help_queries = ["help", "what can you do", "what do you do", "how can you help"]
    if any(h in text for h in help_queries):
        return (
            "I can respond to greetings, farewells, simple FAQs, and give the current time.\n"
            "Try: 'hello', 'what is the time', 'what can you do', 'bye'"
        )

    # Time request
    if "time" in text or "current time" in text or text.startswith("what time"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Current time: {now}"

    # Weather FAQ (rule based stub)
    if "weather" in text:
        return "I don't have live weather access in this simple version, but I can tell you how to fetch it using APIs."

    # Small talk
    if "joke" in text:
        return "Why did the programmer quit his job? Because he didn't get arrays."

    # Fallback
    return "Sorry, I don't know the answer to that. Try asking something else or type 'help'."
