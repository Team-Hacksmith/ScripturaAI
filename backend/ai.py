from openai import OpenAI
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from fileIO import write_files

import os

from pydantic import SecretStr


def gen_docstring(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are an advanced and professional programmer with in depth knowledge in all the programming languages. Please add doc strings to this code {content}. If and only if the given content is in language C/C++ add doxygen not docstring. If the language is python or Javascript then add docstring. Your responses should only be code, without explanation or formatting, and if and only if you don't get any code or only get one or two lines of code which isn't suitable for making docstrings such as codes without functions. You will then say The given codebase is very small we cannot provide docstrings for this. Do not overwrite any existing code at any cost only write things above the functions and etc. do not change them or overwrite them at any cost and at any cost don't remove the whole main function."
    )

    key = SecretStr(os.getenv("OPENAI_API_KEY", ""))

    if key == "":
        raise Exception("OpenAI API Key not set")

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response


def gen_algorithm(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are an advanced and professional programmer with in-depth knowledge of all programming languages. Given the code provided in {content}, write an algorithm explaining each step of how the code works. If there are multiple functions or classes, explain them separately with clarity. Return the explanation in markdown format only, without any additional summaries or interpretations. Do not provide any content other than the markdown explanation."
    )
    key = SecretStr(os.getenv("OPENAI_API_KEY", ""))

    if key == "":
        raise Exception("OpenAI API key not set")

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4,
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
        """Generate a concise and clear Mermaid diagram that visually represents the logical flow of the given algorithm. Break down the algorithm into simple, understandable steps while maintaining a clear structure. Focus on showing the primary actions, decisions, and loops in the algorithm. Keep the flowchart as minimal as possible, without excessive steps or complexity.
        
        The flowchart should include:

        - Initialization (setup or starting point)
        - Input/Setup (any datasets, parameters, or configurations)
        - Main Processing (core actions or logic of the algorithm)
        - Include any loops, iterations, or decision points.
        - Group related steps together using subgraphs if necessary.
        - Output/Result (final outcome, return values, or results to display)
        - End (completion of the algorithm)
        - Use simple shapes and clear connections, avoiding unnecessary details. Focus on the logical flow of the algorithm, from start to end.

        Algorithm: {content}"""
    )

    key = SecretStr(os.getenv("OPENAI_API_KEY", ""))

    if key == "":
        raise Exception("OpenAI API Key not set")

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.6,
        api_key=key,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"content": content})
    return response

def gen_guide(content) -> str:
    prompt = ChatPromptTemplate.from_template(
        """ Generate a concise documentation for a given codebase, similar to popular API or language docs. The documentation should cover:

            Overview: Briefly describe the purpose of the code.
            Prerequisites: List required libraries or setup steps.
            Class & Function Details:
            For each class/function:
            Description of its purpose.
            Parameters and Return Values.
            Code Example for usage.
            Main Workflow: Explain the main function and core logic.
            Output: Describe expected output with examples.
            Usage: Provide a quick start guide for running the code.
            Extensions (Optional): Mention potential improvements.
            Ensure clarity, conciseness, and use code blocks where necessary to aid readability.

            Content: {content}
"""
    )
    key = SecretStr(os.getenv("GEMINI_API_KEY", ""))

    if key == "":
        raise Exception("Gemini API key not set")

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4,
        api_key=key,
    )
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"content": content})
    write_files([{"filename": "userGuide.md", "content": response}], False)
    return response