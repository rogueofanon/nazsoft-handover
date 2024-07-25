# Test 3 of SQL and Langchain where I try implementing chat history context.

import os

from langchain_community.utilities import SQLDatabase

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

import streamlit as st

def generateCompletion(prompt, db, message_history):
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    write_query = create_sql_query_chain(llm,db)
    execute_query = QuerySQLDataBaseTool(db=db)

    combined_prompt = "\n".join([msg["content"] for msg in message_history]) + "\n" + prompt

    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user's question.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )

    answer = answer_prompt | llm |StrOutputParser()
    chain = (RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
        )
        | answer
    )

    return chain.invoke({"question": combined_prompt})

os.environ["OPENAI_API_KEY"] = "OPEN AI KEY"
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
MAX_HISTORY_SIZE = 10

st.title("Query Bot")

#Initializing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display chat messages on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your query."):
    with st.chat_message("user"):
        st.markdown(prompt)
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.session_state.messages = st.session_state.messages

    completion = generateCompletion(prompt,db,st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(completion)
    #Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": completion})

    if len(st.session_state.messages) > 10:
        messages = st.session_state.messages
        st.session_state.messages = messages[-10:]
