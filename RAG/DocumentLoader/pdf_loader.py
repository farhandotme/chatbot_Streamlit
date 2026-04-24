from langchain_community.document_loaders import PyPDFLoader


file_path = (
    "/home/farhan/Desktop/yt-genai/sharians-yt-genai/RAG/DocumentLoader/michael.pdf"
)
loader = PyPDFLoader(file_path)


data = loader.load()


print(data[0].page_content)
