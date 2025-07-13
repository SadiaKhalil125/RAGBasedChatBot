from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
import streamlit as st

load_dotenv()


def giveTranscriptOfVideo(video_id):
# video_id = "LPZh9BOjkQs"
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id,languages=["en"])

        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript

    except TranscriptsDisabled:
        print("No captions available for this video")

#step 1 
#indexing
def return_required_answer(transcript,query):
    chunker = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = chunker.create_documents([transcript])

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks,embeddings)

    retreiver = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={'k':4}
    )
    

    # retreived = retreiver.invoke(query)

    llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.5)

    parser = StrOutputParser()

    prompt = PromptTemplate(
        template="""Your are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.
    
        {context}
        Question: {question}""",
        input_variables=["context","question"]
    )

    def format_docs(retreived_docs):
        context_text = "\n\n".join(doc.page_content for doc in retreived_docs)
        return context_text

    parallelchain = RunnableParallel({
        'context':  retreiver | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })
    # sequentialchain = prompt | llm | parser
    chain = parallelchain | prompt | llm | parser
    result = chain.invoke(query)
    return result

video_id = st.text_input("Enter youtube video id")
query = st.text_input("Enter your query")
if video_id and query:
    transcript = giveTranscriptOfVideo(video_id)
    result = return_required_answer(transcript,query)
if st.button("enter",type="primary"):
    st.text_area("Response",result,height=200)