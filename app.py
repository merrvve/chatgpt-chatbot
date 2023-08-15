from flask import Flask, jsonify, request
from flask_cors import CORS
import openaiService

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/api/data', methods=['POST'])
def api_data():
    data = {
        'reply': 'Hello from Flask REST API!',
        'data': 'Some data to be sent to the Angular frontend'
    }
    return jsonify(data)

@app.route('/getResponse', methods=['POST'])
def getResponse():
    user_message = request.get_json()
    
    if 'message' in user_message:
        message = user_message['message']  # Access 'message' attribute from the JSON data
        
        response=openaiService.getChatGPTResponse(message)
        print(response)
        data = {
            'reply': response,
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Missing or incorrect data'}), 400


if __name__ == '__main__':
    app.run()
