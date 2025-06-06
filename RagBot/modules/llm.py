import os
from dotenv import load_dotenv

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

os.environ["GROQ_API_KEY"] = "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"

def get_llm_chain(vectorstore):
    from langchain_groq.chat_models import ChatGroq

    llm = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model_name="llama3-8b-8192"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Prompt for rephrasing with chat history
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question which might reference context in the chat history, "
        "formulate a standalone question which can be understood without the chat history. "
        "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # Prompt for answering the question using retrieved docs
    qa_system_prompt = (
        "You are an expert AI assistant. Use ONLY the following context to answer the user's question. "
        "If the answer is not contained in the context, say you don't know.\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # Create the history-aware retriever chain (returns docs based on chat history)
    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_q_prompt
    )

    # Create the QA chain that takes docs and answers the question
    question_answer_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    # Compose the final retrieval chain
    chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain
    )

    return chain
