"""Completion backend using the OpenAI SDK for the GPT applet."""
import openai

import keys


# Authennticate OpenAI
openai.api_key = keys.OpenAI.API_KEY


def gpt_response(prompt: str) -> str:
    """Get a completion response from GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0]['message']['content']
