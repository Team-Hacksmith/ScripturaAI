import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from fileIO import write_files

import os

from pydantic import SecretStr


def gen_docstring(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are an advanced and professional programmer with in depth knowledge in all the programming languages. Please add doc strings to this code {content}. Your responses should only be code, without explanation or formatting"
    )

    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API Key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response


def gen_algorithm(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are a advanced and professional programmer with in depth knowledge in all the programming languages. {content} Please write me algorithm for this code, explaining all the steps of how this code works. And if there is more than more function or classes explain them all differently. Also give the output in the markdown format."
    )
    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        api_key=key,
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"content": content})
    write_files([{"filename": "algorithm.md", "content": response}], False)

    return response
