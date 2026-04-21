from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

print("Choose Your Response Mode...")
print("Choose 1 for Angry Mode")
print("Choose 2 for Funny Mode")
print("Choose 3 for Sad Mode")
print("----------choose----------")
modeInput = int(input("Enter the Mode: "))

match modeInput:
    case 1:
        mode = "You are a Angry Ai Agent who reply with Angry Tone..."
    case 2:
        mode = "You are a Funny Ai Agent Who reply Funny way...."
    case 3:
        mode = "You are a sad Ai agent who reply sadly"
messages = [SystemMessage(content=mode)]

while True:
    query = input("You: ")
    messages.append(HumanMessage(content=query))
    if query == "exit":
        break
    response = model.invoke(messages)
    print("Bot: ", response.content)
