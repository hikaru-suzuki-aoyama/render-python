from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import subprocess
import id_ope
import os

#生徒の親にしてもらうこと
#①公式アカウントに登録
#②子供の名前を送ってもらう
#それ以降はメッセージを送らないように注意する

#しーちゃんがやること
#①生徒の登録要請がLINEに来たら、push_messageを起動するか
#②LINE_id_itiranに自分で書き込む
#push_messageじゃないと、完了の通知(LINIに)は来ない

#LINE_Botを使うには
#herokuにログイン?(heroku login)が必要？


LINI_id_dict = id_ope.id_read()

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = LINI_id_dict["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = LINI_id_dict["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

kidname = input("登録する子供の名前は？　＞")
line_id = input("子供のLINE_idは？　＞")

try:
    #PCに環境変数を追加(入退室通知のプッシュ通知のために必要)
    id_ope.id_write(kidname,line_id)
    
    line_bot_api.push_message(LINI_id_dict["Hikaru"], TextSendMessage(kidname + "さんの登録が完了しました。"))
    
except LineBotApiError as e:
    # error handle
    ...