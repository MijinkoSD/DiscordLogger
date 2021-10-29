# DiscordLogger
Discordのチャット履歴をダウンロードするプログラム。  
事前にBotの作成、TOKENの取得、[Botのサーバー参加](#Botのサーバー参加)が必要。

## Botのサーバー参加
プログラムを使うには、あらかじめBotを作成してサーバーに参加させておく必要がある。  
以下のURLからBotの招待ができる。
```
https://discord.com/api/oauth2/authorize?client_id=<Client ID>&permissions=66560&scope=bot
```
※`<Client ID>`の部分は適宜置き換える。

## 使用方法
Python 3.9.7以上で動かしてください。
```bash
$ python3 ./bot.py -t <TOKEN> <チャンネルID> [チャンネルID ...]
```

コマンドライン引数の詳しい説明を見るには、以下のように記述してください。
```bash
$ python3 ./bot.py --help
```

## その他

### 動作が遅い
download.pyとlogger.pyの上の方にあるintervalの値を変更すればダウンロードの間隔が短くなります。  
ただし、あまり短くしすぎるとDiscord側からアクセス制限を食らう可能性があるので注意してください。  
