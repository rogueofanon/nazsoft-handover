# Test 1 of using langchain with SQL.

import os

from langchain_community.utilities import SQLDatabase

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

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

def main():
    os.environ["OPENAI_API_KEY"] = "OPENAIKEY HERE"
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    prompt = input("Enter your query: ")
    completion = generateCompletion(prompt,db)
    print("Completed generation: ")
    print(completion)

if __name__ == "__main__":
    main()
