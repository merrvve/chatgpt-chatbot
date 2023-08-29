# -*- coding: iso-8859-1 -*-

import openai, os
from dotenv.main import load_dotenv

load_dotenv()

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
#question = unicode("E�im uzun zamand�r i�siz. Hi�bir yerde �al��mak istemiyor. E�imin evlilik birli�i i�indeki sorumluluklar� nelerdir? �al��mayan e�ime kar�� bo�anma davas� a�abilir miyim?","utf-8");
question= "zorla sigortas�z �al��t�r�l�yorum. ne yapabilirim?"
docs = vectorstore.similarity_search(question);
#print(len(docs));

#llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
#qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever())
#res=qa_chain({"query": question})


#import logging
   

template = """Sen bir avukats�n. Yaln�zca hukukla ilgili sorulara yan�t ver. Ve yaln�zca T�rkiye kanunlar�na g�re yan�t ver. Bu problemle ilgili hukuki haklar�m nelerdir, bu sorunu ��zmek i�in hangi ad�mlar� atabilirim anlat.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
result = qa_chain({"query": question})
print(result)
print(result["result"])



#logging.basicConfig()
#logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

#retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(),
#                                                  llm=ChatOpenAI(temperature=0))
#unique_docs = retriever_from_llm.get_relevant_documents(query=question)
#len(unique_docs)

##chat = ChatOpenAI()
##conversation = ConversationChain(llm=chat)  
##response=conversation.run("Translate this sentence from English to French: I love programming.")
#messages = [
 #   SystemMessage(content="You are a helpful assistant that translates English to French."),
 #   HumanMessage(content="I love programming.")
#]
#response=chat(messages)
##print(response);
#response=conversation.run("Now, translate it to German.")
#print(response);