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
        "You are an advanced and professional programmer with in depth knowledge in all the programming languages. Please add doc strings to this code {content}. If and only if the given content is in language C/C++ add doxygen not docstring. If the language is python or Javascript then add docstring. Your responses should only be code, without explanation or formatting, and if and only if you don't get any code or only get one or two lines of code which isn't suitable for making docstrings such as codes without functions. You will then say The given codebase is very small we cannot provide docstrings for this. Do not overwrite any existing code at any cost only write things above the functions and etc. do not change them or overwrite them at any cost and at any cost don't remove the whole main function."
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
    print(response)
    return response


def gen_algorithm(content) -> str:
    from fileIO import write_files

    prompt = ChatPromptTemplate.from_template(
        "You are a advanced and professional programmer with in depth knowledge in all the programming languages. {content} Please write me algorithm for this code, explaining all the steps of how this code works. And if there is more than more function or classes explain them all differently. Also give the output in the markdown format."
    )
    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        api_key=key,
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"content": content})
    write_files([{"filename": "algorithm.md", "content": response}], False)
    return response

def gen_mermaid(text) -> str:
    
    content = gen_algorithm(text)
    
    prompt = ChatPromptTemplate.from_template(
        "Please make a mermaid file using this algorithm: {content}. Your response should only be in mermaid no text is needed."
    )

    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API Key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response

def gen_mermaid(text) -> str:
    
    content = gen_algorithm(text)
    
    prompt = ChatPromptTemplate.from_template(
        "Please make a mermaid file using this algorithm: {content}. Your response should only be in mermaid no text is needed."
    )

    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API Key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response

def gen_guide(content) -> str:
    from fileIO import write_files

    prompt = ChatPromptTemplate.from_template(
        "Please analyse this code: {content}. Find patterns and return a markdown response for this explaining this code like a documentation you can refer popular documentation pages and then try to explain the code using markdown."
    )
    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        api_key=key,
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"content": content})
    write_files([{"filename": "userGuide.md", "content": response}], False)
    return response

def gen_markdown(content) -> str:
    from fileIO import write_files
    import os

    prompt = ChatPromptTemplate.from_template(
        "Please analyse this code: {content} and generate corresponding markdown for this code, summarizing everything in this code"
    )
    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))
    if not key:
        raise Exception("Gemini API key not set")

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        api_key=key,
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"content": content})
    # write_files([{"filename": f"{os.path.splitext(filename)[0]}.md", "content": response}], False)
    return response
