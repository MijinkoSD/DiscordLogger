#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メッセージデータから画像をダウンロードするモジュール。

使い方(例):
>>> download.image(<path of messages.json)>)
"""

import os
import json
import requests
import time
from typing import Union

interval = 1


def image(jsonfile: str, savedir:str="attachments/", force_download:bool=False):
    """
        メッセージデータが入っているjsonファイルのパスを渡せば、
        自動でメッセージの添付ファイルをダウンロードしてくれる関数。
        
        ちなみに、関数名はimageだが別に画像じゃなくてもまとめてダウンロードする。

        Parameters
        --------
        jsonfile: str
            メッセージデータが入ったjsonファイルのパス。
        savedir: str, default "attachments/"
            ダウンロードした添付ファイルを保存する場所。
        force_download: bool, default False
            Falseの場合、既にダウンロード済みの画像はダウンロードしない。
    """
    by_url(extract_attach_urls(openjson(jsonfile)),dir=savedir, force_download=force_download)


def openjson(file, encoding='utf_8') -> list:
    """jsonで保存されたメッセージデータを読み込んで辞書型が格納されたリストで返す関数。"""
    with open(file, mode='rt', encoding=encoding) as f:
        data = json.load(f)
    return data


def extract_attach_urls(messagedata):
    """メッセージデータから添付ファイルのURLだけ抽出する関数。"""
    urls = []
    for i in range(len(messagedata)):
        # attachmentsの中身を覗いて、urlが入っていればurlsに入れる。
        if not("attachments" in messagedata[i]): break  # attachmentsが入ってなければbreak

        attaches = messagedata[i]["attachments"]
        for j in range(len(attaches)):
            if not("url" in attaches[j]): continue      # urlが入ってなければcontinue
            urls.append(str(attaches[j]["url"]))
    
    return list(set(urls))          # 重複要素を削除してreturn。


def extract_id(url:str="", urls:list=None) -> Union[dict, list]:
    """
    添付ファイルのURLからIDやファイル名を抽出する関数。
    urlを渡した場合はdict、urlsを渡した場合はdictを要素に持つlistが返る。

    現状、https://cdn.discordapp.com/attachments/ から始まるURLにしか対応していない。
    
    Parameters
    --------
    url: str
        単体のURL。
        urlsを省略した場合は必須。
    urls: list
        複数のURL。

    Returns
    --------
    添付ファイル(attachments)のURLの場合:
        ["type"]: 固定で"attachments"が格納される。
        ["channel_id"]: URLに含まれているチャンネルID
        ["attachments_id"]: 添付ファイルのID
        ["filename"]: ファイル名
    """

    def extracter(url):
        """URL文字列からID等を抜き取り辞書型で返す。"""
        match = "https://cdn.discordapp.com/attachments/"
        index = url.find(match)
        if index == -1 : return       # attachments/で始まるURLでなければreturn
        url = url[index+len(match):]    # url文字列から"attachments/"以降のみを切り出す。

        #idを切り出してdata変数に突っ込む。
        ids = url.split("/")
        try:
            return {"type":"attachments", "channel_id":int(ids[0]), "attachments_id":int(ids[1]), "filename":ids[2]}
        except:
            return #渡されたURLの形式が間違っていたことによりエラーを吐いても無視する。
            

    # 配列が渡されたか変数が渡されたかで処理を変える。
    if not(urls is None):
        # 配列引数
        data = []

        for i in range(len(urls)):
            data.append(extracter(urls[i]))
        
        return data

    elif (url!=""):
        # 単体文字列引数
        return extracter(url)
    else:
        # 引数が渡されてない。
        return
    

    return data


def by_url(urls:list, dir:str="attachments/", force_download:bool=False):
    """
        渡されたURLを元にファイルをダウンロードする。

        Parameters
        --------
        urls: str
            `extract_id`で生成したlistの値。
        dir: str, default "attachments/"
            ダウンロードした添付ファイルを保存する場所。
        force_download: bool, default False
            Falseの場合、既にダウンロード済みの画像はダウンロードしない。
    """
    if not urls: return     # urlsの中身が空なら何もしない。

    # 保存するファイル名を生成する。
    ids = extract_id(urls=urls)     # IDだけじゃなくファイル名も入ってる。
    filenames = []
    for i in range(len(ids)):
        metadata = ids[i]
        if metadata["type"] != "attachments": continue

        # <channel_id>_<attachments_id>_<filename>
        filenames.append(str(metadata["channel_id"]) + "_" + str(metadata["attachments_id"]) + "_" + metadata["filename"])


    # ダウンロードする。
    for i in range(len(urls)):
        # フォルダを作成
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass        # 既に作成されていた場合はエラーとなるが無視。
        
        if os.path.isfile(dir + filenames[i]) and not force_download:
            # ファイルが既に存在していて、かつforce_downloadがFalseのとき。
            print("スキップ("+str(i+1)+"/"+str(len(urls))+"): " + urls[i])
            continue
        else:
            print("ダウンロード中("+str(i+1)+"/"+str(len(urls))+"): " + urls[i])

        # ファイルをダウンロードして保存。
        with open(dir + filenames[i], "wb") as f:
            try:
                response = requests.get(urls[i], timeout=(6.0, 12.0))
            except requests.exceptions.Timeout:
                print( "接続がタイムアウトしました。" )
                print( "　URL: " + urls[i])
                continue

            if response.status_code != 200:
                print( "ファイルを正常に取得できませんでした。")
                print( "　HTTP Status: " + str(response.status_code))
                continue

            f.write(response.content)

        time.sleep(interval)    # 連続で通信しないように間隔を置く。

    # 終了
    print("画像のダウンロードが完了しました。")





if __name__ == "__main__":

    # メッセージオブジェクトが入った.jsonのファイル名を入れないと起動しないよ。
    file=""
    image(file)

