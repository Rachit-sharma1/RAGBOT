import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
load_dotenv()

# Set the API key directly in the code
os.environ["GROQ_API_KEY"] = "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"

def get_llm_chain(vectorstore):
    from langchain_groq.chat_models import ChatGroq
    llm = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model_name="llama3-8b-8192"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
