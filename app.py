import secrets
import os
import json
import redis

from flask import Flask, render_template, request, session, redirect
from revChatGPT.V1 import Chatbot


# Get the path to the config file
if os.name == 'posix':  # Unix-like systems (Linux, macOS, etc.)
    config_path = os.path.join(os.environ['HOME'], 'chatbot', 'config.json')
elif os.name == 'nt':  # Windows
    config_path = os.path.join(
        os.environ['USERPROFILE'], 'chatbot', 'config.json')

# Load the JSON data from the config file
with open(config_path, 'r') as f:
    config_data = json.load(f)

# email = config_data['email'] # email and password
# password = config_data['password']
# session_token = config_data['session_token'] # or session_token
access_token = config_data['access_token']  # or access_token

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379)


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

chatbot = Chatbot(config={
    # "email": email,
    # "password": password,
    # "session_token": session_token,
    "access_token": access_token
})


@app.route("/")
def index():
    if 'user_id' in session and redis_client.exists(f'user_conversation:{session["user_id"]}'):
        return redirect("/chat")
    else:
        return render_template("index.html")


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)

    if redis_client.exists(f'user_conversation:{session["user_id"]}'):
        user_conversation = json.loads(redis_client.get(
            f'user_conversation:{session["user_id"]}'))
    else:
        user_conversation = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = ''
        prev_text = ''
        for data in chatbot.ask(user_input):
            message = str(data["message"][len(prev_text):])
            response += message
            prev_text = str(data["message"])

        user_conversation.append(('user', user_input))
        user_conversation.append(('chatbot', response))
        redis_client.set(
            f'user_conversation:{session["user_id"]}', json.dumps(user_conversation))

        return render_template('chat.html', conversation=user_conversation)
    else:
        return render_template('chat.html', conversation=user_conversation)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    # Delete the current conversation from Redis
    chatbot.delete_conversation(chatbot.conversation_id)
    if 'user_id' in session:
        redis_client.delete(f'user_conversation:{session["user_id"]}')

    # Reset the chatbot conversation and parent IDs
    chatbot.reset_chat()

    # Redirect to the index page
    return redirect("/")


if __name__ == '__main__':
    # Modify host and port accordingly
    app.run(host='0.0.0.0', port='8080', debug=True)
