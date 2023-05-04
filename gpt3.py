import openai

class Gpt3:
    def __init__(self) -> None:
        self._openai = openai
        api = 'API'
        self._openai.api_key = api
        self._model_engine = "text-davinci-003"

    def response(self, resp):
        # Set the model and prompt
        prompt = resp
        # Set the maximum number of tokens to generate in the response
        max_tokens = 2048
        # Generate a response
        completion = openai.Completion.create(
            engine=self._model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

        )
        return completion.choices[0].text
    