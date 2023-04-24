from flask import Flask
import openai
from urllib.parse import unquote
import argparse

app = Flask(__name__)
openai.api_key = ""


@app.route('/generate-emojis/<prompt>', methods=['GET'])
def generate_emojis(prompt):
    decoded_prompt = unquote(prompt)
    input_text = decoded_prompt + "                                                                                  I need 2 emoji's that describe this text and would work well at the end. The return output should be the text(unchanged and unformatted) and the two emojis:"
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=input_text, 
        max_tokens=1024,    
    )
    return_response = response.choices[0].text.strip()
    return return_response  

@app.route('/generate-text/<prompt>', methods=['GET'])
def generate_text(prompt):
    decoded_prompt = unquote(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt="You are a prompt answerer. You take whatever prompt I give, and give the best answer that fits the main idea and this is the prompt:" + decoded_prompt,
        max_tokens=1024,
    )
    return_response = response.choices[0].text.strip()
    return return_response

@app.route('/generate-multiple-response/<prompt>', methods=['GET'])
def generate_query_response(prompt):
    decoded_prompt = unquote(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=decoded_prompt, 
        max_tokens=1024,
    )
    return_response = response.choices[0].text.strip()
    return return_response

def parse_args():
    parser =argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000,
                        help='port number.')
    return parser.parse_args()

if __name__ == '__main__': 
    args = parse_args()
    app.run(host = '0.0.0.0', port=args.port)