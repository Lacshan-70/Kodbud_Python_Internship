import datetime
import random

# ------------------------------------------------------
# 1. HELPER FUNCTIONS
# ------------------------------------------------------

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The time is {now} ⏰"

def get_date():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    return f"Today's date is {today} 📅"

def get_joke():
    jokes = [
        "Why don't programmers like nature? Too many bugs! 🐞😂",
        "Why do Python programmers wear glasses? Because they can't C! 🤓",
        "Debugging: Being the detective in a crime movie... where you're also the murderer. 😅",
    ]
    return random.choice(jokes)

def get_quote():
    quotes = [
        "Every day is a new chance to grow 🌱",
        "Believe you can, and you're halfway there ✨",
        "Be unstoppable. Be a force. 💪",
        "Your only limit is you 🚀",
    ]
    return random.choice(quotes)

def weather_info():
    # Simple offline example
    return "Today's weather looks pleasant with clear skies ☀️"

# ------------------------------------------------------
# 2. MAIN CHATBOT LOGIC
# ------------------------------------------------------

def chatbot_response(user_input):

    user_input = user_input.lower()

    # --- EXIT CONDITION ---
    if user_input in ["bye", "quit", "exit"]:
        return "Goodbye! Have a great day 😊"

    # --- HELP MENU ---
    if "help" in user_input:
        return (
            "Here are some things you can ask:\n"
            " - hello\n"
            " - time\n"
            " - date\n"
            " - about you\n"
            " - about me\n"
            " - weather\n"
            " - joke\n"
            " - quote\n"
            " - what can you do\n"
            " - bye\n"
        )

    # --- GREETINGS ---
    if "hello" in user_input or "hi" in user_input:
        return "Hello! I'm your upgraded Python chatbot 🤖✨ How can I help you today?"

    # --- TIME ---
    if "time" in user_input:
        return get_time()

    # --- DATE ---
    if "date" in user_input:
        return get_date()

    # --- ABOUT BOT ---
    if "about you" in user_input:
        return "I'm Lacshan's AI chatbot 🤖, created for the Kodbud Internship! I can answer questions, tell jokes, give weather info, and more."

    # --- ABOUT USER ---
    if "about me" in user_input:
        return "You're Lacshan! A talented Mechatronics student who builds cool projects 😎🔥"

    # --- WEATHER ---
    if "weather" in user_input:
        return weather_info()

    # --- JOKE ---
    if "joke" in user_input:
        return get_joke()

    # --- QUOTE ---
    if "quote" in user_input or "motivate" in user_input:
        return get_quote()

    # --- WHAT CAN YOU DO ---
    if "what can you do" in user_input:
        return (
            "I can tell you the time, date, weather, jokes, quotes, and chat with you.\n"
            "Type 'help' to see everything I can do 😊"
        )

    # --- DEFAULT RESPONSE ---
    return "Hmm… I don't understand that yet 🤔. Try typing 'help'."

# ------------------------------------------------------
# 3. RUN CHATBOT
# ------------------------------------------------------

print("🤖 Chatbot: Hello! Type 'help' for options or 'bye' to exit.\n")

while True:
    user = input("You: ")
    response = chatbot_response(user)
    print("Bot:", response)

    if user.lower() in ["bye", "quit", "exit"]:
        break
