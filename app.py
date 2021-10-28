# import flask related
from flask import Flask, request, abort, url_for
from urllib.parse import parse_qsl, parse_qs
import random, joblib
import numpy as np
from linebot.models import events
from line_chatbot_api import *

# create flask server
app = Flask(__name__)

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent)
def handle_something(event):
    if event.message.type=='text':
        recrive_text=event.message.text
        try:
            room_number = float(recrive_text)
            filename = 'linearregression_model.bin'
            loaded_model = joblib.load(filename)
            y_pred = loaded_model.predict(np.array([[room_number]]).T)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f'預測波士頓房價為 ${y_pred[0]:.2f} 千鎂'))
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '請輸入房間數量(數字)，機器人會幫你預測波士頓房價喔!'))

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)