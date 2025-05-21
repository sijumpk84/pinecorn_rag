from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone client with API key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Set embedding model
model_name = 'multilingual-e5-large'
embeddings = PineconeEmbeddings(
    model=model_name,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

# Configure serverless index spec with default cloud and region
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'
spec = ServerlessSpec(cloud=cloud, region=region)

# Get index name from environment
index_name = os.getenv("PINECONE_INDEX_NAME")

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=embeddings.dimension,
        metric="cosine",
        spec=spec
    )

# Print index stats before upserting any data
print("Index before upsert:")
print(pc.Index(index_name).describe_index_stats())
print("\n")
