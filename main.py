from flask import Flask, render_template, request
from flask_cors import CORS
import openaiService

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('index.html')

@app.route('/getResponse', methods=['POST'])
def getResponse(message):
    user_message = request.get_json()
    response_text = user_message

    return jsonify(response_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)