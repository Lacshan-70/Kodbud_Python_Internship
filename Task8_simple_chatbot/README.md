# Simple CLI Chatbot

A tiny rule-based chatbot implemented for the command line. It uses simple if/elif rules to respond to greetings, farewells, FAQs and a few other inputs.

## Files
- `Chatbot.py` - CLI application that runs the chatbot loop.
- `chatbot_logic.py` - Logic module with `get_response()` and helper `normalize_text()`.
- `test_chatbot.py` - Unit tests for the logic module.

## Usage
Run the chatbot from the `Task8_simple_chatbot` folder:

```powershell
&C:\path\to\workspace\.venv\Scripts\python.exe Chatbot.py
```

Or, if your environment is already set up:

```bash
python Chatbot.py
```

Type messages and press Enter. To exit, type `exit`, `quit`, `bye`, or press Ctrl+C.

## Examples
- You: `hello` → Bot: `Hello! How can I help you today?`
- You: `what can you do` → Bot: displays capabilities
- You: `what is the time` → Bot: returns current time
- You: `bye` → Bot: says goodbye and exits

## Tests
Run unit tests with:

```powershell
&C:\path\to\workspace\.venv\Scripts\python.exe test_chatbot.py
```

Or:

```bash
python test_chatbot.py
```

The tests validate greetings, farewells, help responses, time, and fallback behavior.
