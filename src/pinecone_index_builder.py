import time
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_text_splitters import MarkdownHeaderTextSplitter

# Load environment variables from .env file
load_dotenv()

# Read the markdown file into a variable
with open('assets/content.md', 'r', encoding='utf-8') as file:
    markdown_document = file.read()

# Define headers to split on (e.g., level 2 headers)
headers_to_split_on = [
    ("##", "Header 2")
]

# Initialize markdown header splitter
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)

# Split markdown document based on headers
md_header_splits = markdown_splitter.split_text(markdown_document)

# Set embedding model
model_name = 'multilingual-e5-large'
embeddings = PineconeEmbeddings(
    model=model_name,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create Pinecone vector store from split markdown documents
docsearch = PineconeVectorStore.from_documents(
    documents=md_header_splits,
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings,
    namespace=os.getenv("PINECONE_NAMESPACE")
)
