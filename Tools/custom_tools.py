from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
from rich import print


def get_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)


model = ChatMistralAI(model="mistral-small")


llm_with_tool = model.bind_tools([get_length])

response = model.invoke("Return the number of the given Text :-> 'hello'")
response2 = llm_with_tool.invoke("Return the number of the given Text :-> 'hello'")

print(response)
print()

print()
print(response2)
