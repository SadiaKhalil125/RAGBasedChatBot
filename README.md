Live Demo: https://ragbasedchatbot-ixz5tvmptnqnu68jp34x6a.streamlit.app/


I recently spent two weeks learning and implementing Gen AI using langchain and its components.
I discovered various concepts including how langchain helps in building LLM based applications, how it provides uniformity in diff interfaces to help developers.
I discovered difference about LLMs and ChatModels. Open source llms and closed source llms. How can we use open source models locally. I learned about prompts and can we play with prompts
to get exactly what we want. How can we use structured outputs, which models support structured output by default and which don't. Learned pydantic library for data validation. Discovered different
type of output parsers including string, json, pydantic. I learned how chains are formed and how they make code so easy and for me it was most interesting part. I learned about runnables,
their types and what was the need of them and how runnable sequence is so popular so it gets simple chain like interface to provide ease to developers. I learned how to build different scenario
suitable chains like sequential, parallel, conditional. Then I moved forward to RAG. Understood every letter. Indexing like how to retreive data from external source, chunking it, create embeddings,
storing in vector dbs like Chroma, FAISS, Pinecome,etc, (Inshort, I learned about different types of loaders, splitters, chunkers and vector stores).Then, today I developed my first simple rag based 
bot where you upload your file in (pdf/docx/txt) and can question about anything and it will answer accordingly.

Techs:
-Langchain 
-Semantic Chunker
-PyPDFLoader, unstructuredworddocloader, textloader
-retreiver (technique Maximal Marginal Relevance)
-OpenAI API
-Prompt templates
-Streamlit for UI

Flow:
-User uploads file + write query + press enter
-receiving file and query, load documents, break into chunks, embeddings stored in faiss vector store, then retreiver retreives the top 3 matches using MMR, then a structured prompt is 
created and sent to open ai chat model, then through chain invoke model and parses output string
-user gets to see result 
