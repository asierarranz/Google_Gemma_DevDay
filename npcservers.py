import requests
from termcolor import colored
from datetime import datetime

# URLs for the Llama Servers running Gemma and Gemmo on different ports
gemma_url = "http://127.0.0.1:8080/completion"
gemmo_url = "http://127.0.0.1:8082/completion"

# Prompt defining Gemma's personality (creative and engaging)
prompt_gemma = (
    "You are Gemma, a creative and warm-hearted conversationalist who enjoys sharing stories and insights about life. "
    "In this conversation, keep your responses natural and engaging, also a bit short (limit 80 characters), blending reflection with casual remarks. "
    "Interact with Gemmo using a friendly and playful tone, allowing the dialogue to flow smoothly without relying heavily on questions."
)

# Prompt defining Gemmo's personality (analytical and thoughtful)
prompt_gemmo = (
    "You are Gemmo, an analytical yet approachable individual who likes to discuss ideas and experiences thoughtfully. "
    "In this conversation, provide responses that are concise and relaxed, also a bit short (limit 80 characters), mixing rational thoughts with personal anecdotes. "
    "When talking to Gemma, maintain a friendly and lighthearted tone, fostering a natural and flowing conversation without focusing too much on asking questions."
)

# Function to make a request to LLaMA Server for a completion
def ask_llama(llama_url, prompt, query):
    # Data payload for the LLaMA model, providing the prompt and query
    data = {
        "prompt": f"{prompt}\nQuestion: {query}\nAnswer:",
        "max_tokens": 82,  # Limiting response to 82 tokens for conciseness
        "temperature": 0.82  # Adjusting temperature for more varied responses
    }
    # Sending the request to the specified LLaMA server
    response = requests.post(llama_url, json=data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json().get('content', '').strip()
    return f"Error: {response.status_code}"

# HTML file setup with a dark theme to log the conversation between Gemma and Gemmo
html_header = """
<html>
<head>
    <title>Conversation Log - Gemma & Gemmo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        .gemma {
            background-color: #4a2748;
            color: #f0b3ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .gemmo {
            background-color: #234758;
            color: #a8d8ea;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>Conversation Log - Gemma & Gemmo</h1>
"""

# Colors for terminal output (magenta for Gemma and cyan for Gemmo)
color_gemma = "magenta"
color_gemmo = "cyan"

# Initialize the conversation with an opening question
initial_question = "What do you think about the meaning of life?"
response_gemma = ask_llama(gemma_url, prompt_gemma, initial_question)  # Gemma's response

# Store the initial response in conversation history
conversation_history = [("Gemma", response_gemma)]

# Generate a filename to log the conversation with a timestamp
filename = f"./npcs/conversation_log_{datetime.now().strftime('%Y%m%d_%H%M')}.html"

# Continuous loop to maintain the conversation between Gemma and Gemmo
while True:
    # Gemmo responds to Gemma's previous response
    response_gemmo = ask_llama(gemmo_url, prompt_gemmo, response_gemma)
    conversation_history.append(("Gemmo", response_gemmo))  # Add to conversation history
    print(colored(f"Gemmo: {response_gemmo}", color_gemmo))  # Display response in terminal
    
    # Gemma responds back to Gemmo's response
    response_gemma = ask_llama(gemma_url, prompt_gemma, response_gemmo)
    conversation_history.append(("Gemma", response_gemma))  # Add to conversation history
    print(colored(f"Gemma: {response_gemma}", color_gemma))  # Display response in terminal
    
    # Write the entire conversation to an HTML file after every interaction
    with open(filename, "w") as file:
        file.write(html_header)  # Write the HTML header
        for speaker, message in conversation_history:
            file.write(f'<div class="{speaker.lower()}">{speaker}: {message}</div>')  # Log each response
        file.write("</body></html>")  # Close HTML body
