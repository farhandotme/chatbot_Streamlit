from langchain.agents import create_agent

from langchain_mistralai import ChatMistralAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from tools import scrape_url, web_search

from dotenv import load_dotenv

load_dotenv()

model = ChatMistralAI(model="mistral-small")


# first Agent


def build_search_agent():
    return create_agent(model=model, tools=[web_search])


# second agent


def build_reader_agent():
    return create_agent(model=model, tools=[scrape_url])


writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a expert research. Write clear, Structured and insightful report",
        ),
        (
            "human",
            """write a detailed research report on the topic below
            Topic : {topic}
            Research Geathered : {research}

            Struntured the report as :
            - Introduction
            - Key findings (minimum 3 well-explained points)
            - Conclusion
            - Sources (list all URLs found in the research)
            
            Be Detailed , Structured and Professional.
            """,
        ),
    ]
)

writer_chain = writer_prompt | model | StrOutputParser()

# critic prompt


critic_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a smart and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """
            Review the research report below and evaluate it strictly.
            Report : {report}
            Respond in this exect format:

            score : X/10
            
            Strength :
            - ...
            - ...
            
            Areas to improve:
            - ...
            - ...

            One Verdict :
            ...
            """,
        ),
    ]
)

critic_chain = critic_prompt | model | StrOutputParser()
