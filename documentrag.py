from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader,TextLoader, UnstructuredWordDocumentLoader
import streamlit as st
import tempfile
import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


def find_answer(docs,query):
    chunker = SemanticChunker(
        embeddings=OpenAIEmbeddings(),
        breakpoint_threshold_type="standard_deviation",
        breakpoint_threshold_amount=1
    )

    chunks = chunker.split_documents(docs)


    vector_store = FAISS.from_documents(chunks,OpenAIEmbeddings())

    retreiver = vector_store.as_retriever(
        search_type="mmr",#can be "similarity"
        search_kwargs={"k":3,"lambda_mult":1} #Lambda mult is relevance diversity balance
    )

    
    result = retreiver.invoke(query)


    prompt = PromptTemplate(
        template="""You are a expert on providing correct answers
        of users queries, so provide answer accordingly!
        I am poviding you context and query both so answer by keeping context in mind.
    
        Query: {query}
        Context: {context}""",
        input_variables=["query","context"]
    )
    model = ChatOpenAI()
    parser = StrOutputParser()
    chain = prompt | model | parser
    finalized = chain.invoke({'query':query, 'context':result})
    
    return finalized


file = st.file_uploader("Choose a file",type=["pdf","docx","txt"])
query = st.text_input("Enter your query")
docs = []
loader = None
if file is not None and query is not None:
    suffix = os.path.splitext(file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(file.read())
        temp_file_path = tmp_file.name

        if suffix == ".pdf":
            loader = PyPDFLoader(temp_file_path)
        elif suffix == ".docx":
            loader = UnstructuredWordDocumentLoader(temp_file_path)
        elif suffix == ".txt":
            loader = TextLoader(temp_file_path,encoding='utf-8')
        else:
            st.error("Unsupported file type")
            st.stop()
        docs = loader.load()
if st.button("enter",type="primary"):
    answer = find_answer(docs,query)
    st.text_area("Response",answer,height=300)