import streamlit as st
from PIL import Image
import os
from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


st.title('Conoce lo que van hacer tus candidatos segun las plataformas electorales')


if 'imagen' not in st.session_state:
    st.session_state.imagen = 'imgs/libertadAvanza.jpeg'


if 'respuesta' not in st.session_state:
    st.session_state.respuesta = ''

if 'password' not in st.session_state:
    st.session_state.password = ''


def langChain(option, query):
    

    persist_directory = f'vectorstores/{option}/'
    embedding = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding, )
   

    # PROMPT
    template = """Responder la pregunta en base al contexto provisto. 
                Si no sabes la respueta, solo responde que no sabes la 
                respuesta, no la inventes. Responde en español. Responde de manera completa.
                No termines con una oracion cortada.
                 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # CHAIN
    qa_chain = RetrievalQA.from_chain_type(
                llm= OpenAI(temperature=0),
                retriever=vectordb.as_retriever(search_type='similarity', search_kwargs= {'k': 3}),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )
    
    result = qa_chain({"query": query})
            
    st.session_state.respuesta = result['result']



option = st.selectbox(
'PLATAFORMA',
('libertadAvanza', 'juntosxcambio','partidoObrero', 'patriaGrande')) 

col1, col2 = st.columns(2)

with col1:
    if option == 'libertadAvanza':
        imagen = Image.open('imgs/libertadAvanza.jpeg')
    elif option == 'juntosxcambio':
        imagen = Image.open('imgs/juntosXcambio.png')
    elif option == 'partidoObrero':
        imagen = Image.open('imgs/partidoObrero.png')
    elif option == 'patriaGrande':
        imagen = Image.open('imgs/patriaGrande.jpeg')
    
    st.image(imagen)
        

with col2:
    query = st.text_input('PREGUNTA')
    st.button("PREGUNTAR!", on_click=langChain, args=(option, query))

if st.session_state.respuesta:
    st.write(st.session_state.respuesta)


with st.sidebar:

    st.text("Conectarse a OPENAI:")
    password = st.text_input('SECRET KEY', type="password")
    st.session_state.password = password

    os.environ['OPENAI_API_KEY'] = st.session_state.password
