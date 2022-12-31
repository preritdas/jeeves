"""Completion backend using the OpenAI SDK for the GPT applet."""
import openai

import keys


# Authennticate OpenAI
openai.api_key = keys.OpenAI.API_KEY


def gpt_response(prompt: str, tokens: int = 200) -> str:
    """Get a completion response from GPT."""
    assert isinstance(tokens, int), "`tokens` must be an integer."

    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = tokens,
        n = 1,
        temperature = 0.7
    )

    return str(completions.choices[0].text)
