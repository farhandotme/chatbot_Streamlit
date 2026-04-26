from dotenv import load_dotenv

load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from langchain_groq import ChatGroq

model = ChatGroq(model="llama-3.1-8b-instant")

# user query------
user_query = input("Ask about the document : ")

# Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


# prompt template-------

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "you are an Expert AI Assistent and you are a RAG based AI that helps the user to get details about the uploaded documents and do not give any extra information which is not given in the datas just give the infomation which is mentioned in the documents or the given datas.The data will be given to you and you need to explain it easily that the user will understand easily....so the datas are this : {context}",
        ),
        ("human", "{query}"),
    ]
)


# the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

# loading the file
file_path = (
    "/home/farhan/Desktop/yt-genai/sharians-yt-genai/RAG/DocumentLoader/michael.pdf"
)
loader = PyPDFLoader(file_path)

data = loader.load()

chunks = splitter.split_documents(data)
print("Total Chunks : ", len(chunks))

# created the vactor store
vactorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="michael_data",
)

similar_datas = vactorstore.similarity_search(user_query, k=2)

context = "\n\n".join([doc.page_content for doc in similar_datas])


finalPrompt = prompt.invoke({"context": context, "query": user_query})

response = model.invoke(finalPrompt)

print(response.content)
