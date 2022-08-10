import os
import string
import openai


class text_to_text:
    def __init__(self):
        self.prompt = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they'd come and take me away.\nYou: What is the meaning of life?\nMarv: I'm not sure. I'll ask my friend Google."
        openai.api_key = os.getenv("OpenAPIKey")

    def query(self, Input: str) -> str:
        """This takes in the query of the user and submits it to GPT-3 for a response

        Args:
            Input (str): What the user has asked the robot

        Returns:
            str: The robots response
        """
        # submition = self.prompt + "\nYou: " + Input + "\nMarv: "
        self.prompt += "\nYou: " + Input + "\nMarv: "
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.prompt,
            temperature=0.5,
            max_tokens=60,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        self.prompt += response.choices[0].text
        return response.choices[0].text