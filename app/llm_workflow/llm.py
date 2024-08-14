from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import OllamaLLM
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager

class StreamingGeneratorCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []

    def on_llm_new_token(self, token: str, *, chunk= None, run_id, parent_run_id = None, **kwargs):
        self.tokens.append(token)

callback_handler = StreamingGeneratorCallbackHandler()
callback_manager = CallbackManager([callback_handler])

model = OllamaLLM(model="llama3.1:8b", callback_manager=callback_manager, temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder(variable_name="system_message"), MessagesPlaceholder(variable_name="human_messages")]
)

chain = prompt| model