import os
import string
import openai


class conversation:
    def __init__(self):
        self.prompt = "You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend: Yes, I watched some great old movies."
        openai.api_key = os.getenv("OpenAPIKey")

    def query(self, Input: str) -> str:
        """This takes in the query of the user and submits it to GPT-3 for a response

        Args:
            Input (str): What the user has asked the robot

        Returns:
            str: The robots response
        """
        self.prompt + "\nYou: " + Input
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.prompt,
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["You:"]
        )
        return response
