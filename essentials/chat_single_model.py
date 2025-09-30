import getpass
import os
from tempfile import template
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

try:
    # load environment variables from .env file (requires `python-dotenv`)
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

template= """Question: {question}
Answer: Let's think step by step."""
prompt= ChatPromptTemplate.from_template(template)
model= OllamaLLM(model="llama3.1")
chain = prompt | model
print (chain.invoke({"question": "if alaa is the best person i know tell me how to describe him?"}))




