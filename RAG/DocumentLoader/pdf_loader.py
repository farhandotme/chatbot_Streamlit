from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_groq import ChatGroq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind · RAG Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #0d0e11;
    --surface:   #141519;
    --border:    #22242b;
    --accent:    #c8a96e;
    --accent2:   #6e9ec8;
    --text:      #e8e4dc;
    --muted:     #666a77;
    --success:   #6ec8a0;
    --radius:    10px;
}

/* ── Global overrides ── */
.stApp { background: var(--bg) !important; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1100px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }

/* ── Logo / Header ── */
.logo-block {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2.5rem;
}
.logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 20px rgba(200,169,110,.25);
    flex-shrink: 0;
}
.logo-text { font-family: 'DM Serif Display', serif; font-size: 1.3rem; line-height: 1.1; }
.logo-text span { color: var(--accent); }
.logo-sub { font-size: 0.7rem; color: var(--muted); font-family: 'DM Mono', monospace; letter-spacing: .08em; }

/* ── Sidebar labels ── */
.sidebar-label {
    font-size: 0.65rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin: 1.5rem 0 0.5rem;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: .04em;
    margin-top: 0.5rem;
}
.status-pill.ready { background: rgba(110,200,160,.12); color: var(--success); border: 1px solid rgba(110,200,160,.25); }
.status-pill.idle  { background: rgba(102,106,119,.12); color: var(--muted);   border: 1px solid rgba(102,106,119,.25); }
.status-pill.warn  { background: rgba(200,169,110,.12); color: var(--accent);  border: 1px solid rgba(200,169,110,.25); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* ── Main page title ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    line-height: 1.1;
    margin-bottom: 0.3rem;
    background: linear-gradient(120deg, var(--text) 0%, var(--accent) 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.page-sub {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Input box ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color .2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,169,110,.12) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #b8903e) !important;
    color: #0d0e11 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity .2s, transform .1s !important;
    letter-spacing: .02em;
    width: 100%;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Answer card ── */
.answer-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-top: 1.5rem;
    line-height: 1.75;
    font-size: 0.95rem;
    animation: fadeUp .35s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Metadata row ── */
.meta-row {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-bottom: 1rem;
}
.meta-chip {
    background: rgba(110,158,200,.1);
    border: 1px solid rgba(110,158,200,.2);
    color: var(--accent2);
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 3px 10px;
    letter-spacing: .04em;
}

/* ── Source docs ── */
.source-block {
    background: rgba(255,255,255,.03);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-top: 0.75rem;
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.6;
    font-family: 'DM Mono', monospace;
}
.source-title {
    font-size: 0.68rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Expander ── */
details > summary {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-family: 'DM Mono', monospace !important;
    cursor: pointer;
    letter-spacing: .04em;
}
[data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Selectbox / file uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Helpers ──────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def load_model():
    return ChatGroq(model="llama-3.1-8b-instant")


def get_prompt():
    return ChatPromptTemplate(
        [
            (
                "system",
                "you are an Expert AI Assistent and you are a RAG based AI that helps the user to get details about the uploaded documents and do not give any extra information which is not given in the datas just give the infomation which is mentioned in the documents or the given datas.The data will be given to you and you need to explain it easily that the user will understand easily....so the datas are this : {context}",
            ),
            ("human", "{query}"),
        ]
    )


def get_or_create_vectorstore(file_path, collection_name, embeddings):
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections().collections
    collection_exists = any(c.name == collection_name for c in collections)

    if collection_exists:
        return (
            Qdrant.from_existing_collection(
                embedding=embeddings,
                url="http://localhost:6333",
                collection_name=collection_name,
            ),
            False,
        )  # (store, is_new)
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        loader = PyPDFLoader(file_path)
        data = loader.load()
        chunks = splitter.split_documents(data)
        store = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            url="http://localhost:6333",
            collection_name=collection_name,
        )
        return store, True  # (store, is_new)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div class="logo-block">
        <div class="logo-icon">◈</div>
        <div>
            <div class="logo-text">Doc<span>Mind</span></div>
            <div class="logo-sub">RAG · v1.0</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">Document Source</div>', unsafe_allow_html=True
    )
    file_path = st.text_input(
        "PDF FILE PATH",
        value="/home/farhan/Desktop/yt-genai/sharians-yt-genai/RAG/DocumentLoader/michael.pdf",
        help="Absolute path to the PDF file on this machine",
        label_visibility="collapsed",
    )
    st.caption("Enter the absolute path to your PDF file")

    st.markdown(
        '<div class="sidebar-label">Collection Name</div>', unsafe_allow_html=True
    )
    collection_name = st.text_input(
        "QDRANT COLLECTION",
        value="michael_data",
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-label">Retrieval</div>', unsafe_allow_html=True)
    k_docs = st.slider(
        "Top-K chunks",
        min_value=1,
        max_value=8,
        value=3,
        help="Number of relevant chunks to retrieve",
    )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-label">Qdrant Status</div>', unsafe_allow_html=True
    )
    if st.button("◎  Ping Qdrant"):
        try:
            QdrantClient(url="http://localhost:6333").get_collections()
            st.markdown(
                '<div class="status-pill ready"><span class="dot"></span>Connected</div>',
                unsafe_allow_html=True,
            )
        except Exception:
            st.markdown(
                '<div class="status-pill warn"><span class="dot"></span>Unreachable</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="sidebar-label">Model</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="status-pill idle"><span class="dot"></span>llama-3.1-8b-instant</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-label">Embeddings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="status-pill idle"><span class="dot"></span>all-MiniLM-L6-v2</div>',
        unsafe_allow_html=True,
    )


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Ask Your Document</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">RAG-powered assistant — answers drawn strictly from your PDF, nothing more.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

query = st.text_input(
    "YOUR QUESTION",
    placeholder="e.g.  What is the main topic of this document?",
    label_visibility="visible",
)

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    ask_btn = st.button("Ask ◈")

if ask_btn and query.strip():
    if not file_path.strip():
        st.warning("Please enter a PDF file path in the sidebar.")
    else:
        with st.spinner("Thinking…"):
            try:
                embeddings = load_embeddings()
                model = load_model()
                prompt = get_prompt()

                vectorstore, is_new = get_or_create_vectorstore(
                    file_path, collection_name, embeddings
                )

                retriever = vectorstore.as_retriever(
                    search_kwargs={"k": k_docs}, search_type="mmr"
                )
                relevant_docs = retriever.invoke(query)
                context = "\n\n".join([d.page_content for d in relevant_docs])
                final_prompt = prompt.invoke({"context": context, "query": query})
                response = model.invoke(final_prompt)

                # ── Answer ──
                ingestion_badge = (
                    "◈ New collection created"
                    if is_new
                    else "◈ Loaded existing collection"
                )
                st.markdown(
                    f"""
                <div class="meta-row">
                    <span class="meta-chip">{ingestion_badge}</span>
                    <span class="meta-chip">{len(relevant_docs)} chunks retrieved</span>
                    <span class="meta-chip">{collection_name}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="answer-card">{response.content}</div>',
                    unsafe_allow_html=True,
                )

                # ── Source chunks ──
                with st.expander("◎  View source chunks", expanded=False):
                    for i, doc in enumerate(relevant_docs, 1):
                        pg = doc.metadata.get("page", "?")
                        st.markdown(
                            f'<div class="source-title">Chunk {i} · Page {pg}</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="source-block">{doc.page_content}</div>',
                            unsafe_allow_html=True,
                        )

            except Exception as e:
                st.error(f"Error: {e}")

elif ask_btn and not query.strip():
    st.warning("Please type a question before hitting Ask.")

# ── Empty state ───────────────────────────────────────────────────────────────
if not query.strip():
    st.markdown(
        """
    <div style="text-align:center; padding: 4rem 0; color: var(--muted);">
        <div style="font-size:2.5rem; margin-bottom:1rem; opacity:.4;">◈</div>
        <div style="font-family:'DM Mono',monospace; font-size:.78rem; letter-spacing:.1em; text-transform:uppercase;">
            Enter a question above to begin
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
