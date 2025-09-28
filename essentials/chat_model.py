import getpass
import os
from langchain.chat_models import init_chat_model


if not os.environ.get("DEEPSEEK_API_KEY"):
  os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter API key for DeepSeek: ")


model = init_chat_model("deepseek-chat", model_provider="deepseek")
model.invoke("Hello, world!")