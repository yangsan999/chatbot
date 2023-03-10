import secrets

from flask import Flask, render_template, request, session, redirect
from revChatGPT.V1 import Chatbot
from OpenAIAuth import Error


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# create empty conversation dictionary
conversations = {}

@app.route("/")
def index():
    if 'email' in session and 'password' in session:
        # User is logged in, so display the chat page
        if 'user_id' in session and session['user_id'] in conversations:
            return redirect("/chat")
        else:
            return render_template("index.html")
    else:
        # User is not logged in, so redirect to the login page
        return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Store the email and password in the session
        session['email'] = email
        session['password'] = password
        # Initialize the chatbot with the session credentials
        global chatbot
        try:
            chatbot = Chatbot(config={
                "email": email,
                "password": password
            })
        except Error as e:
            return "Authentication error {}".format(str(e))
        return redirect('/')
    else:
        return render_template('login.html')


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
            response = "对不起，我忙不过来了，请稍后重试...\nSorry, I am too busy. Please try again later."

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
        return redirect("/chat")
    except Exception as e:
        return redirect("/chat")


if __name__ == '__main__':
    # Modify host and port accordingly
    app.run(host='0.0.0.0', port='8080', ssl_context=('cert.pem', 'key.pem'))
