
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, MessageAction, TemplateSendMessage,TextSendMessage,
    ButtonsTemplate)

import subprocess

import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
Hikaru_LINE_id = os.environ["Hikaru_LINE_id"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
    profile = line_bot_api.get_profile(event.source.user_id)
    
    #子供の名前をアルファベットで送ってもらう
    if(event.message.text.split()[0] == "登録"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(event.message.text.split()[1] + "さんの登録が完了しました！\n\nこちらの公式アカウントから、お子様の入退室のご連絡が入りますので、宜しくお願い致します。\n\n※なお、このメッセージ以降は基本的にメッセージの送信は行わないようにお願いします。"))
        #ipad側に登録完了のお知らせが来る(PC上で処理を行い、herokuに環境変数の追加が必要)
        line_bot_api.push_message(Hikaru_LINE_id, TextSendMessage(event.message.text.split()[1] + "さんの登録要請がありました。\n\n" + event.message.text.split()[1] + "さんのidは、\n" +
                                                                                    profile.user_id + " \nです。\n\n PC上でプログラム「push_massage.py」を起動 or LINE_id_itiran.txt の更新をお願いします。" ))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("無効なリクエストが送信されました。\n\nお名前の登録は\n「登録+空白+お子様のお名前」\nでメッセージを送信してください。"))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
