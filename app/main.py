
from flask import Flask, render_template, request
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

import os
import openai

openai.api_key = "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"
def getChatGPTResponse(message):
    print(message)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir avukatsın. Yalnızca hukukla ilgili sorulara yanıt ver. Yalnızca Türk kanunlarına göre yanıt ver. "
                },
                {
                    "role": "user",
                    "content": message
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return "Error"
        





@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('index.html')

@app.route('/getResponse', methods=['POST'])
def getResponse(message):
    user_message = request.get_json()
    response_text = user_message

    return jsonify(response_text)



