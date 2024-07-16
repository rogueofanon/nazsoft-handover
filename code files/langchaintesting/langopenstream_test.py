# Test 2 of SQL with Langchain where I try implementing streamlit to create an UI.

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

def generateCompletion(prompt, db):
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm,db)

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

    return chain.invoke({"question": prompt})

os.environ["OPENAI_API_KEY"] = "OPENAI KEY"
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

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

    completion = generateCompletion(prompt,db)
    with st.chat_message("assistant"):
        st.markdown(completion)
    #Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": completion})
