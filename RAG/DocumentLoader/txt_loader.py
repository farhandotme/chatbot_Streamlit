from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate

prompts = ChatPromptTemplate(
    [
        (
            "system",
            "You are a Expert Rag AI assistent that take the documents data and helps the user to analise and summarise the data and understands the documents data fast and do not answer extra which is not mentioned in the document. Structuly follow the datas and ansnwer only based on that are given below: {data}",
        ),
        ("human", "{userInput}"),
    ]
)
model = ChatGroq(model="llama-3.1-8b-instant")
data = TextLoader(
    "/home/farhan/Desktop/yt-genai/sharians-yt-genai/RAG/DocumentLoader/demo.txt"
)
docs = data.load()

user_input = input("You: ")

prompt = prompts.format_messages(userInput=user_input, data=docs)
# print(docs[0].page_content)

data = docs[0].page_content
response = model.invoke(prompt)

print(response.content)
