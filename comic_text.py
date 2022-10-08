import cohere
import os
from dotenv import load_dotenv


# Put your API key in .env file, which CANNOT be uploaded to the github repo
# COHERE_APIKEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
load_dotenv()
COHERE_APIKEY = os.getenv('COHERE_APIKEY')
co = cohere.Client(COHERE_APIKEY)


def comic_text_gen(prompt, max_tokens=20, model='small'):
    response = co.generate(prompt=prompt, max_tokens=max_tokens, model=model)
    return response.generations[0].text


if __name__ == '__main__':
    prompt = 'Once upon a time in a magical land called'
    text = comic_text_gen(prompt)
    print(f'Prompt: {prompt}')
    print(f'Prediction: {text}')
