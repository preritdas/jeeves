"""Completion backend using the OpenAI SDK for the GPT applet."""
import openai

from keys import KEYS


# Authennticate OpenAI
openai.api_key = KEYS.OpenAI.api_key


def gpt_response(prompt: str) -> str:
    """Get a completion response from GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0]["message"]["content"]
