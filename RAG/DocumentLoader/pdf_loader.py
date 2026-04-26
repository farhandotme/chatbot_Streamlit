from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


# Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# BAAI/bge-small-en-v1.5


# prompt template
prompt = ChatPromptTemplate(
    [
        (
            "system",
            "you are an Expert AI Assistent that helps the user to get details about the documents",
        ),
        ("human", ""),
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
