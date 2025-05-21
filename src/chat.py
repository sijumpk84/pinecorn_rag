import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from langchain_community.vectorstores import Pinecone
from langchain import hub

load_dotenv()

# Load prompt
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Set up embeddings and retriever
embeddings = PineconeEmbeddings(
    model='multilingual-e5-large',
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)
docsearch = PineconeVectorStore.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings,
    namespace=os.getenv("PINECONE_NAMESPACE")
)
retriever = docsearch.as_retriever()

# LLM and chain
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name='gpt-4o-mini',
    temperature=0.0
)
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

def get_chat_response(query: str):
    # First call: direct model invocation
    raw_answer = llm.invoke(query)

    # Second call: with knowledge
    answer_with_knowledge = retrieval_chain.invoke({"input": query})

    return {
        "query": query,
        "raw_answer": raw_answer.content,
        "answer_with_knowledge": answer_with_knowledge['answer'],
        "context": answer_with_knowledge['context']
    }
