# 🛠️ RAG Chatbot - Quick Start Guide

A simple Retrieval-Augmented Generation (RAG) chatbot using FastAPI, OpenAI, and Pinecone.

---

## ✅ Requirements

- Python 3.9 or higher
- OpenAI & Pinecone API keys
- [Ngrok](https://ngrok.com/) (for public access)

---

## 📁 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://your-repo-url.git
cd your-repo-directory
```


### 2. Create a .env File

Make a copy of .env.example:

```bash
cp .env.example .env
```

Edit the .env file and add your secret values:

```ini
OPENAI_API_KEY=your-openai-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=your-namespace
```



### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```


## 🚀 Running the App Locally

Before starting the FastAPI development server, you must initialize the Pinecone index and populate it with your content.
### 1. Create the Pinecone Index

Run the setup script to create the Pinecone index (if it doesn't already exist):

```bash
python src/pinecone_index_setup.py
```

### 2. Add Content to the Index

After creating the index, populate it with data from your markdown file:

```bash
python src/pinecone_index_builder.py
```

### 3. Start the FastAPI Server

Now launch the development server:

```bash
fastapi dev src/main.py
```

The app will be accessible at:
👉 http://127.0.0.1:8000/


## 🌐 Exposing the App with Ngrok

### 1. Install Ngrok

Run the following command to install Ngrok on Ubuntu:

```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
```

### 2. Set Up Ngrok

  - Create an account at Ngrok Dashboard

  - Generate your auth token and add it:

```bash
ngrok config add-authtoken  <TOKEN>
```

  - Register a subdomain by visiting:
    https://dashboard.ngrok.com/domains


### 3. Start Ngrok Tunnel

From your project root directory, run:

```bash
ngrok http --url=your-subdomain.ngrok-free.app 8000 --traffic-policy-file=traffic-policy.yml
```
Replace your-subdomain with the actual subdomain you registered.

## 🔐 Basic Authentication

If you're using traffic-policy.yml to secure your app, access will prompt for credentials:

  - Username: admin

  - Password: password

Then open your app in a browser:

👉 https://your-subdomain.ngrok-free.app

