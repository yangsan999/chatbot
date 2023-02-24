# Flask Chatbot Web Application
A Flask web application chatbot based on ChatGPT unoffical API ([revChatGPT](https://github.com/acheong08/ChatGPT)）.

The application provides a simple chat interface that allows users to enter text, which is then sent to the chatbot API. The chatbot API returns a response, which is then displayed in the chat interface.

The web application also allows users to reset the chatbot conversation if they wish to start a new conversation.

## Requirements

- Python 3.x
- Flask
- revChatGPT

## Installation

1. Clone the repository:

```bash
git clone https://github.com/username/chatbot-webapp.git
```

2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create account on [OpenAI's ChatGPT](https://chat.openai.com/)
2. Save your email and password

### Authentication methods: (Choose one of these methods)
#### Email/Password
Not supported for Google/Microsoft accounts
```json
{
  "email": "email",
  "password": "your password"
}
```
#### Session token
Comes from cookies on chat.openai.com as "__Secure-next-auth.session-token"

```json
{
  "session_token": "..."
}
```
#### Access token
https://chat.openai.com/api/auth/session
```json
{
  "access_token": "<access_token>"
}
```

#### Optional configuration:

```json
{
  "conversation_id": "UUID...",
  "parent_id": "UUID...",
  "proxy": "...",
  "paid": false
}
```

3. Save it as `$HOME/chatbot/config.json` in Unix-like systems (Linux, macOS, etc.)
4. If you are using Windows, save it as `$USERPROFILE/chatbot/config.json`.



## Run the application:

```bash
python app.py
```

or

if you want to use gunicorn
```bash
gunicorn -b 0.0.0.0:8080 app:app --timeout 200 --worker-class gevent 
```

## Usage

1. Open your web browser and go to `http://localhost:8080`.

2. Enter your message in the chat interface and click "Send".

3. The chatbot API will return a response, which will be displayed in the chat interface.

4. To reset the conversation, click the "Reset" button.

## Contributing

If you find any issues or bugs in the application, please feel free to create a pull request or raise an issue in the repository.

# Disclaimers

This is not an official OpenAI product. 
The purpose of developing this project is for learning and exploration only. It is not affiliated with OpenAI in any way. 
Any risks arising from the use or modification of any content in this project should be borne by the user and not the author. 
To protect the legitimate rights and interests of users, we strongly remind you to ensure compliance with relevant laws, regulations and policy provisions when using this project, and to bear corresponding legal responsibilities. 
Thank you for your cooperation and support.