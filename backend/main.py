from flask import Flask, request, jsonify

from langchain_google_genai import ChatGoogleGenerativeAI

import getpass
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

app = Flask(__name__)

# Initialize ChatGoogleGenerativeAI with Google Gemini Pro model
# Ensure that GOOGLE_API_KEY and LANGCHAIN_API_KEY are set in your environment variables
chat_model = ChatGoogleGenerativeAI(model="gemini-pro")


@app.route("/", methods=["GET"])
def generate_content():
    prompt = "Hi"

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Generate content based on the prompt
    try:
        response = chat_model.invoke(prompt)
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
