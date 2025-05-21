import time
import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to existing Pinecone index
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# Optional: Uncomment to print index stats
print("Index after upsert:")
print(index.describe_index_stats())
print("\n")

# Get the namespace from environment variables
namespace = os.getenv("PINECONE_NAMESPACE")

# Iterate over all IDs in the specified namespace
for ids in index.list(namespace=namespace):
    # Query the index by ID with metadata, excluding vector values
    query = index.query(
        id=ids[0],
        namespace=namespace,
        top_k=1,
        include_values=False,
        include_metadata=True
    )
    print(query)
    print("\n---\n")
