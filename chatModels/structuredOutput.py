import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")


class Movie(BaseModel):
    title: str
    release_year: int
    director: str
    cast: List[str]
    genre: List[str]
    plot_summary: str
    rating: Optional[float]


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a movie data extractor.

Return ONLY valid JSON.
Do NOT explain anything.
Do NOT return schema.

{format_instructions}
""",
        ),
        ("human", "{input}"),
    ]
)

# 🔥 Chain (best way)
chain = prompt | model | parser

# UI
st.title("🎬 Movie Data Extractor")

user_input = st.text_area("Enter movie paragraph:")

if st.button("Extract"):
    if user_input.strip():
        try:
            result = chain.invoke(
                {
                    "input": user_input,
                    "format_instructions": parser.get_format_instructions(),
                }
            )
            st.json(result.model_dump())
        except Exception as e:
            st.error("Parsing error")
            st.text(str(e))
    else:
        st.warning("Please enter some text")
