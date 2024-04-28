import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from groq import Groq

groq_api_key = os.getenv('groq_API')

st.set_page_config(
    page_title = "AskWiki",
    page_icon = "💬",
    initial_sidebar_state = 'auto',
    menu_items = {
        "Report a Bug" : "mailto:lasithdissanayake.official@gmail.com",
        "About" : "https://dissanayakelyb.github.io/LasithDissanayake.github.io/"
    }
)

# app framework
st.title("AskWiki")
prompt = st.text_input("Mention the topic you need in Wikipedia")

with st.sidebar:
    reset = st.button(
         label = "Reset",
         type="primary"
         )

    model = st.selectbox(
        'Choose a model',
        ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']
    )

# prompt templates
respond_template = PromptTemplate(
    input_variables = ['topic', 'wikipedia_research'],
    template = "Write about the {topic} using {wikipedia_research} and mention the sources and links to them as well."
)

# memory
memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')


# llms
llm = ChatGroq(
    api_key=groq_api_key ,
    model_name=model,
    temperature=0.1
)
respond_chain = LLMChain(llm=llm, prompt=respond_template, verbose=True, memory=memory)

wiki = WikipediaAPIWrapper()

submit = st.button("Submit", key = "Enter")

# response
if submit:
    wiki_research = wiki.run(prompt)
    response = respond_chain.run(topic=prompt , wikipedia_research = wiki_research)

    st.write(response)

    with st.expander('Wikipedia Research') :
        st.info(wiki_research)   

        


