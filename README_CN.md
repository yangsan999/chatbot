# Flask聊天机器人Web应用程序

基于ChatGPT非官方API ([revChatGPT](https://github.com/acheong08/ChatGPT))的Flask Web应用程序聊天机器人。

该应用程序提供了一个简单的聊天界面，允许用户输入文本，然后将文本发送到聊天机器人API。聊天机器人API返回一个响应，然后在聊天界面中显示该响应。

该Web应用程序还允许用户重置聊天机器人会话，以便他们希望开始新的对话。

## 要求

- Python 3.x
- Flask
- revChatGPT

## 安装

1. 克隆存储库：

```bash
git clone https://github.com/username/chatbot-webapp.git
```

2. 使用pip安装所需的软件包：

```bash
pip install -r requirements.txt
```

## 配置

1. 在[OpenAI's ChatGPT](https://chat.openai.com/)上创建帐户。
2. 保存您的电子邮件和密码。

### 鉴权方法：（选择其中一种方法）
#### 邮箱/密码
不支持Google/Microsoft帐户
```json
{
  "email": "email",
  "password": "your password"
}
```
#### Session token
来自chat.openai.com上的cookie作为"__Secure-next-auth.session-token"

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

#### 可选配置：

```json
{
  "conversation_id": "UUID...",
  "parent_id": "UUID...",
  "proxy": "...",
  "paid": false
}
```
3. 将config.json.example重命名为config.json，修改相关配置
4. 将其保存为`$HOME/chatbot/config.json`（在类Unix系统（Linux，macOS等）中）。
5. 如果您使用Windows，请将其保存为`$USERPROFILE/chatbot/config.json`。

## 运行应用程序：

测试使用:
```bash
python app.py
```
生产环境可以使用其他WSGI服务器，例如gunicorn：
```bash
gunicorn -b 0.0.0.0:8080 app:app --timeout 200 --worker-class gevent 
```

## 用法

1. 打开Web浏览器并转到`http://localhost:8080`。

2. 在聊天界面中输入您的消息，然后单击“发送”。

3. 聊天机器人API将返回一个响应，该响应将显示在聊天界面中。

4. 要重置会话，请单击“重置”按钮。

## 贡献

如果您在应用程序中发现任何问题或错误，请随时创建拉取请求或在存储库中提出问题。

# 声明
这不是官方OpenAI产品。
本项目的开发目的仅为学习和探索之用。与OpenAI没有任何关系。
使用或修改本项目的任何内容所引发的一切风险应由用户自行承担，与本作者无关。
为保障用户的合法权益，我们郑重提醒您在使用本项目时，请确保符合相关法律法规及政策规定，并承担相应的法律责任。
谢谢您的合作与支持。




## 附录
### 使用Docker Compose
> 以下所有文件放同一目录
1. 将config.json.example重命名为config.json，修改相关配置
2. 新建`docker-compose.yml`配置文件，粘贴以下内容并保存
```bash
services:
  chatgpt:
    image: sheepgreen/chatgpt-html:proxy #如果是arm架构，请换成chatgpt-html:proxyarm
    container_name: chatbot
#    environment:
#      - CHATGPT_BASE_URL=你的代理服务端地址（不填默认使用作者服务器，目前偶尔会不可用）
    volumes:
      - ./config.json:/chatgpt-html/config.json
#      - ./chat.html:/chatgpt-html/templates/chat.html #默认内置我的UI，如需替换自用网页请取消注释
    ports:
      - "9999:8088" #8088为容器内端口，不可更换；9999为外部端口，可自行更换
    restart: always
```
- 输入`docker-compose up -d`即启动成功
## 注意事项
- 访问地址为http://ip:port