from itertools import chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage



try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="../")
except ImportError:
    pass



# ------------------Using Template--------------------------
# template= """translate the following from english into {lang}:
#             {q}"""
# prompt= ChatPromptTemplate.from_template(template)


# ------------------Using message---------------------------
message= "translate the following from english into {lang}"
# prompt definition in langchain site, we notice that .to_message() func is useless 
# prompt = ChatPromptTemplate.from_messages([
#      ("system", message),
#      ("user","{q}"),
#      ]).invoke({"q":"The part of speech used to indicate nouns and to specify their application.","lang":"Arabic"}).to_messages()

#prompt = ChatPromptTemplate.from_messages([
 #    ("system", message),
  #   ("user","{q}"),
   #  ])

#print(prompt)
# Define the model
#model = OllamaLLM(model="llama3.1")
#chain = prompt | model
#print(chain.invoke({"q":"The part of speech used to indicate nouns and to specify their application.", "lang": "Arabic"}))




# ----------Using SystemMessage & HumanMessage--------------
#this method take a static string input's without being able to invoke variables into prompt
prompt = [
    SystemMessage(content= "translate the following from english into Arabic"),
    HumanMessage(content= "how are you?")
]

print(prompt)
model = OllamaLLM(model="llama3.1")
print(model.invoke(prompt))
