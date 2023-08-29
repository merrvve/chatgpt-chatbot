from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
import requests,openai,os
from dotenv.main import load_dotenv

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain 
from langchain.document_loaders import TextLoader
# Read the file using the correct encoding
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

#from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


loader = TextLoader("sc.txt", encoding = 'UTF-8')
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)


vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings());


app = Flask(__name__)
CORS(app)
app.debug = True;

load_dotenv()
API = os.environ['OPENAI_API_KEY']

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/legas')
def legas():
    return render_template('legas.html')
    

@app.route('/data', methods=['POST'])
def get_data():
    
    data = request.get_json()
    text=data.get('data')
    openai.api_key = API
    
    user_input = text
    print(user_input)
    try:
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir avukatsın. Yalnızca hukukla ilgili sorulara yanıt ver ve yalnızca Türkiye kanunlarına göre yanıt ver."
                },
                {
                    "role": "user",
                    "content": user_input + " Bu durumla ilgili kanuni haklarım nelerdir? en kolay çözüme ulaşmak için hangi yolları izlemeliyim? Tüm seçenekleri bana söylemeni istiyorum."
                }
            ],
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
       
        model_reply = response.choices[0].message.content
        print(response,model_reply)
        return jsonify({"response":True,"message":model_reply})
    except Exception as e:
        print(e)
        error_message = f'Error: {str(e)}'
        return jsonify({"message":error_message,"response":False})

  
        

@app.route('/chat', methods=['POST'])
def get_response():
    
    data = request.get_json()
    question=data.get('data')
     
    user_input = question
    print(user_input)
    template = """Sen bir avukatsın. Yalnızca hukukla ilgili sorulara Türkiye kanunlarına göre yanıt ver.
    {context}
    Question: {question} Bu soru eğer hukukla ilgiliyse yanıt ver. Bu problemle ilgili hukuki haklarım nelerdir, bu sorunu çözmek için hangi adımları atabilirim anlat. Örnek cevap yapısı: 1. Konuyla ilgili Türkiye kanunlarına göre hukuki haklar 2.Sorunu çözmek için belge, kanıt vs neler gerekli. Bu belgeler nasıl elde edilir. 5. Nerelere nasıl başvurulmalı.
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query": question})
    print(result["result"])
    return jsonify({"message":result["result"],"response":True})



if __name__ == '__main__':
    app.run()
