# DiscordLogger
Discordのチャット履歴をダウンロードするプログラム。
事前にBotの作成、TOKENの取得、Botのサーバー参加が必要。

## 使用方法
```bash
python3 ./bot.py -t <TOKEN> <チャンネルID> [チャンネルID ...]
```

## その他

### 動作が遅い
download.pyとlogger.pyの上の方にあるintervalの値を変更すればダウンロードの間隔が短くなります。
ただし、あまり短くしすぎるとDiscord側からアクセス制限を食らう可能性があるので注意してください。
