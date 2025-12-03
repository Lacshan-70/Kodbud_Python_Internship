"""
Unit tests for the simple chatbot logic
"""
import unittest
from chatbot_logic import get_response


class TestChatbotLogic(unittest.TestCase):
    def test_greeting(self):
        self.assertIn("Hello", get_response("Hello"))
        self.assertIn("Hello", get_response("hi"))

    def test_farewell(self):
        self.assertIn("Goodbye", get_response("bye"))
        self.assertIn("Goodbye", get_response("goodbye"))

    def test_thanks(self):
        self.assertIn("You're welcome", get_response("thanks"))
        self.assertIn("You're welcome", get_response("thank you"))

    def test_help(self):
        resp = get_response("what can you do?")
        self.assertIn("I can respond", resp)

    def test_name(self):
        resp = get_response("what is your name")
        self.assertIn("simple CLI chatbot", resp)

    def test_time(self):
        resp = get_response("what is the time")
        self.assertIn("Current time:", resp)

    def test_unknown(self):
        resp = get_response("asdlkfjasdf")
        self.assertIn("Sorry, I don't know", resp)

    def test_empty(self):
        resp = get_response("")
        self.assertIn("didn't catch", resp)


if __name__ == '__main__':
    unittest.main()
