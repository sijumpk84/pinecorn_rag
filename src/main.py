from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from chat import get_chat_response

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat with Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: auto; }
            #chat-box { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; }
            .user { color: blue; margin: 5px 0; }
            .assistant { color: green; margin: 5px 0; }
            input[type=text] { width: 80%; padding: 10px; }
            button { padding: 10px; }
        </style>
    </head>
    <body>
        <h2>Chat Assistant</h2>
        <div id="chat-box"></div>
        <input type="text" id="user-input" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>

        <script>
            async function sendMessage() {
                const input = document.getElementById("user-input");
                const chatBox = document.getElementById("chat-box");
                const userMessage = input.value;
                if (!userMessage.trim()) return;

                chatBox.innerHTML += `<div class='user'><b>You:</b> ${userMessage}</div>`;
                input.value = "";

                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: userMessage })
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class='assistant'><b>Assistant:</b> ${data.answer_with_knowledge}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query", "")
    if not query:
        return JSONResponse(status_code=400, content={"error": "Query is required"})

    response = get_chat_response(query)
    return response
