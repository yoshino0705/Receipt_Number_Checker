from flask import Flask, request, abort
import os

from Checker import Receipt_Numbers
from Utilities_Functions import filter_inputs, parse_results

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['Channel_Access_Token'])
handler = WebhookHandler(os.environ['Channel_Secret'])
rn = Receipt_Numbers()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('Received', event.message.text)
    filtered_text = list(map(filter_inputs, event.message.text.split()))
    batch = [single_check(t) for t in filtered_text if t] # if t isn't ''
    batch = '\n\n'.join(batch)
    if batch == '':
        batch = '請輸入數字'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=batch))
    
def single_check(input_text):    
    result = rn.check(input_text)
    msg = list(map(parse_results, result))
    msg = '\n'.join(msg)
    return '號碼{}:\n{}'.format(input_text, msg[:8])

if __name__ == "__main__":
    app.run()
