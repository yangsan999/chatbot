import secrets
import os
import json

from flask import Flask, render_template, request, session, redirect
from revChatGPT.V1 import Chatbot


# Load the JSON data from the config file
with open("config.json", 'r') as f:
    config_data = json.load(f)

# email = config_data['email'] # email and password
# password = config_data['password']
# session_token = config_data['session_token'] # or session_token
access_token = config_data['access_token']  # or access_token


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

chatbot = Chatbot(config={
    # "email": email,
    # "password": password,
    # "session_token": session_token,
    "access_token": access_token
})

# create empty conversation dictionary
conversations = {}


@app.route("/")
def index():
    if 'user_id' in session and session['user_id'] in conversations:
        return redirect("/chat")
    else:
        return render_template("index.html")


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)

    if session['user_id'] in conversations:
        user_conversation = conversations[session['user_id']]
    else:
        user_conversation = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = ''
        prev_text = ''
        try:
            for data in chatbot.ask(user_input):
                message = str(data["message"][len(prev_text):])
                response += message
                prev_text = str(data["message"])
        except Exception as e:
            response = "对不起，我忙不过来了，请稍后重试...\nSorry, I am too busing. Please try again later."

        user_conversation.append(('user', user_input))
        user_conversation.append(('chatbot', response))
        conversations[session['user_id']] = user_conversation

    return render_template('chat.html', conversation=user_conversation)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if 'user_id' in session and session['user_id'] in conversations:
        del conversations[session['user_id']]
    try:
        # Delete the current conversation from the dictionary
        chatbot.delete_conversation(chatbot.conversation_id)

        # Reset the chatbot conversation and parent IDs
        chatbot.reset_chat()

        # Redirect to the index page
        return redirect("/")
    except Exception as e:
        # error_message = "对不起，因流量过多，重置会话超时了，正在重载页面"
        # return render_template("error.html", message=error_message)
        return redirect("/")


if __name__ == '__main__':
    # Modify host and port accordingly
    app.run(host='0.0.0.0', port='8080', debug=False)
