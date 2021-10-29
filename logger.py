#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time


interval = 1
apiurl = "https://discord.com/api/v9"


# メッセージのログを全件取得してくれる。
#   token:      "Bot <BOT Token>"
#   channelID:  チャンネルのID。
#   beforeID:   メッセージIDを渡すと、そのメッセージよりも前のメッセージを取得する（省略可）。
def message_all(token: str, channelID:int, beforeID:int=0) -> list:
    message_count = 0
    messages = []
    while True:
        url = apiurl + "/channels/" + str(channelID) + "/messages?limit=100"
        url += ( "&before="+str(beforeID) if beforeID>0 else "" )
        header = {"authorization":token}
        response = requests.get(url, headers=header)
        res_values = response.json()

        if response.status_code / 100 != 2:
            print("Error: HTTP Status Code: " + str(response.status_code))
            break
        
        messages += res_values
        if len(res_values) < 100:
            message_count += len(res_values)
            break

        message_count += 100

        # # 300件取得で終了する（テスト用）
        # if message_count >= 300:
        #     break

        print( str(message_count) + "件のメッセージを取得済み。" )
        time.sleep(interval)
        
        beforeID = int(res_values[99]['id'])
            
    
    print( str(message_count) + "件のメッセージを取得しました。" )
    return messages


# チャンネルの情報を取得する。
#   token:      "Bot <BOT Token>"
#   channelID:  取得するチャンネルのID。
def channel(token: str, channel_id: int) -> dict:
    print("チャンネル情報を取得中。")
    url = apiurl + "/channels/" + str(channel_id)
    header = {"authorization":token}
    response = requests.get(url, headers=header)
    if response.status_code / 100 != 2:
        print("Error: HTTP Status Code: " + str(response.status_code))
    print("チャンネル情報を取得しました。")
    return response.json()


def guild(token: str, guild_id: int) -> dict:
    print("ギルド情報を取得中。")
    url = apiurl + "/guilds/" + str(guild_id)
    header = {"authorization":token}
    response = requests.get(url, headers=header)
    if response.status_code / 100 != 2:
        print("Error: HTTP Status Code: " + str(response.status_code))
    print("ギルド情報を取得しました。")
    return response.json()
