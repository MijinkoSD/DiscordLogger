import json

# おまけで用意したやつ。
# メッセージオブジェクトが保存された.jsonファイルからメッセージの内容だけを取り出して.txtに保存する。

messages = []

with open("messages.json", mode='rt', encoding='utf_8') as f:
    data = json.load(f)
    
    print("メッセージ件数: " + str(len(data)))
    
    for i in range(len(data)):
        author = data[i]["author"]["username"]
        content = data[i]["content"].replace("\n", "\\n")

        # 文章がない場合（画像のみ貼り付けとか）
        if not content:
            attachments = data[i]["attachments"]
            if len(attachments) > 0:
                messages.append(author + "：" + attachments[0]["url"])
            else:
                messages.append(author)

        else:
            messages.append(author + "「" + content + "」")
    

with open("messages.txt", mode='wt', encoding='utf_8') as f:
    for message in messages:
        f.write("%s\n" % message)

