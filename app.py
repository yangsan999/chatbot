from flask import Flask, render_template, request, session
from revChatGPT.V1 import Chatbot

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


chatbot = Chatbot(config={
    "email": "",
    "password": ""
})


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_conversation' not in session:
        session['user_conversation'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = ''
        prev_text = ''
        for data in chatbot.ask(user_input):
            message = data["message"][len(prev_text):]
            response += message
            prev_text = data["message"]

        user_conversation = session['user_conversation']
        user_conversation.append(('user', user_input))
        user_conversation.append(('chatbot', response))
        session['user_conversation'] = user_conversation

        return render_template('home.html', conversation=session['user_conversation'])
    else:
        return render_template('home.html', conversation=session.get('user_conversation', []))


if __name__ == '__main__':
    # Modify host and port accordingly
    app.run(host='172.31.22.91', port='80', debug=True)
