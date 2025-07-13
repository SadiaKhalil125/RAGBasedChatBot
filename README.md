# 📄 RAG-Based Chatbot

🚀 **Live Demo of files based rag**: https://ragbasedchatbot-ixz5tvmptnqnu68jp34x6a.streamlit.app/

🚀 **Live Demo of yt transcript based rag**: https://ragbasedchatbot-hg6db9drjh3czwpybcyg5p.streamlit.app/


main.py is for youtube transcript based rag (who answers with a single youtube video id about its content)
documentrag.py is for uploading files and get answers

## 📚 What I Learned

Over the past two weeks, I’ve been diving deep into **Generative AI** using **LangChain** and its ecosystem. Here's a summary of what I explored and implemented:

### 🔹 LangChain Fundamentals

* Differences between **LLMs** vs. **ChatModels**
* Usage of **open-source** and **closed-source** LLMs (local & cloud)
* Uniform interfaces provided by LangChain to ease development
* Understanding and experimenting with **prompts** to fine-tune responses

### 🔹 Structured Outputs

* Learned to work with:

  * `pydantic` for schema validation
  * Output parsers: `StrOutputParser`, `JsonOutputParser`, `PydanticOutputParser`
* Which models support structured output natively vs. with parsing

### 🔹 Chains and Runnables

* Built **sequential**, **parallel**, and **conditional chains**
* Explored **Runnables** and their types
* Understood `RunnableSequence` for building modular pipelines

### 🔹 RAG (Retrieval-Augmented Generation)

* What it means (Retrieve + Augment + Generate)
* Concepts covered:

  * **Document indexing**
  * **Chunking strategies**
  * Creating **embeddings**
  * Using **vector databases**: FAISS, Chroma, Pinecone
  * Explored different loaders, chunkers, and vector store integrations

---

## 🤖 Project Overview

A simple **RAG-based chatbot** that lets you upload a document (`.pdf`, `.docx`, or `.txt`) and ask questions about its content. The model retrieves the relevant parts and answers intelligently using an LLM.

---

## 🛠️ Tech Stack

* **LangChain**
* **Streamlit** – for the UI
* **OpenAI API** – as the LLM backend
* **FAISS** – vector store for similarity search
* **SemanticChunker** – for intelligent document splitting
* **Document Loaders**:

  * `PyPDFLoader`
  * `UnstructuredWordDocumentLoader`
  * `TextLoader`
* **Retriever**: Maximal Marginal Relevance (MMR) technique
* **Prompt Templates** – to control model behavior

---

## 🔁 How It Works (Flow) (documentrag.py)

1. **User uploads** a file and enters a query
2. The app:

   * Loads the document
   * Chunks the content using `SemanticChunker` 
   * Converts chunks into embeddings
   * Stores embeddings in **FAISS**
3. A **Retriever** uses **MMR** to find top 3 relevant chunks
4. A structured **PromptTemplate** is created with query + context
5. The **LLM (ChatOpenAI)** is invoked using a **Chain**
6. The output is parsed and displayed to the user

---
## 🔁 How It Works (Flow) (main.py)

1. **User uploads** a youtube video id and enters a query
2. The app:

   * Loads the transcript with youtube-transcript-api
   * Chunks the content using `Recursive text splitter` 
   * Converts chunks into embeddings
   * Stores embeddings in **FAISS**
3. A **Retriever** uses **cosine similarity method** to find top 3 relevant chunks
4. A structured **PromptTemplate** is created with query + context
5. The **LLM (ChatOpenAI)** is invoked using a **Chain**
6. The output is parsed and displayed to the user
## ✅ Features

* Upload support for `youtube video id`,`.pdf`, `.docx`, and `.txt`
* Clean Streamlit UI
* Uses modern LangChain features (like `RunnableSequence`,`RunnableParallel`,`Runnablelambda`,RunnablePassthrough`)
* Emphasizes **retrieval quality** using MMR,Cosine similarity
* Easy to deploy and extend
