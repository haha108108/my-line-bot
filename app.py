from flask import Flask, request
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 从环境变量读取 LINE Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    
    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"你說: {event.message.text}")
                )
    
    return 'OK'

@app.route("/", methods=['GET'])
def hello():
    return "LINE Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
