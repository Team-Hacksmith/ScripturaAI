import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


import os

from pydantic import SecretStr


def gen_docstring(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        "Please add doc strings to this code {content}. Your responses should only be code, without explanation or formatting"
    )

    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API Key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response
