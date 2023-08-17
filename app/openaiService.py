import os
import openai

openai.api_key = ""
def getChatGPTResponse(message):
    print(message)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir hukuk danışmanısın. Yalnızca hukukla ilgili sorulara yanıt ver."
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
        
