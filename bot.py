import os
import sys
import json
import argparse

import logger
import download


# コマンド引数の設定
module_description='''

Discordのテキストチャンネル内のメッセージ履歴を取得して保存します。

起動にはBotトークンが必要です。
環境変数'DISCORD_TOKEN'に値が設定されていればトークンとして使用します。

また、使用するBotには以下の権限が付与されている必要があります。
・チャンネルを見る (View Channels)
・メッセージ履歴を読む (Read Message History)

'''
parser = argparse.ArgumentParser(description=module_description, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-t", "--token", type=str, help="トークンを設定します。")
parser.add_argument("-f", "--force-download-image", action="store_true", help="画像を上書きしてダウンロードします（このオプションに関わらずメッセージデータは常に上書きします）。")
parser.add_argument("-u", "--use-usertoken", action="store_true", help="トークンをユーザートークンとして解釈します。")
parser.add_argument("channel_id", nargs='+', type=int, help="ログを取得するチャンネルIDを設定します（複数指定可）。")

if len(sys.argv) <= 1:
    parser.print_help()
    exit()
args = parser.parse_args()


'''


呼び出し方の例
$ python bot.py <チャンネルID> -t <トークン>


環境変数にトークンを設定している場合は引数のトークンを省略できる。

環境変数の設定例
Windows PowerShell:
> $env:DISCORD_TOKEN="<トークン>"
Linux:
$ export DISCORD_TOKEN="<トークン>"


'''
print(args.force_download_image)

USER_TOKEN="Bot "
if args.use_usertoken:
    USER_TOKEN=""

if args.token is None:
    USER_TOKEN+=os.environ['DISCORD_TOKEN']
else:
    USER_TOKEN+=args.token

CHANNEL_ID = args.channel_id


# フォルダを作成する関数
def makefolder(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass        # 既に作成されていた場合はエラーとなるが無視。


def logging_channel(channel_id:int):
    # logフォルダの作成。
    log_dir = "log/"
    makefolder(log_dir)


    # チャンネル情報を保存する。
    channel = logger.channel(token=USER_TOKEN, channel_id=channel_id)
    guild_id = channel["guild_id"]      # ついでにギルドIDも取得
    guild_log_dir = log_dir+str(guild_id)+"/"
    makefolder(guild_log_dir)

    channel_filename = "channel_"+str(channel_id)+"_channel.json"

    with open(guild_log_dir+channel_filename, mode='wt', encoding='utf_8') as f:
        json.dump(channel, f, ensure_ascii=False, indent=2)


    # ギルド情報を取得する。
    guild = logger.guild(token=USER_TOKEN, guild_id=guild_id)
    guild_filename = "guild_"+str(guild_id)+"_guild.json"

    with open(guild_log_dir+guild_filename, mode='wt', encoding='utf_8') as f:
        json.dump(channel, f, ensure_ascii=False, indent=2)
    
    
    # メッセージ履歴を保存する。
    messages = logger.message_all(token=USER_TOKEN, channelID=channel_id)
    message_filename = "channel_"+str(channel_id)+"_messages.json"

    with open(guild_log_dir+message_filename, mode='wt', encoding='utf_8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    

    # 画像を保存する。
    attachments_dir = guild_log_dir + str(channel_id)+"_attachments/"
    makefolder(attachments_dir)
    download.image(jsonfile=guild_log_dir+message_filename, savedir=attachments_dir, force_download=args.force_download_image)



if __name__ == "__main__":
    for i in range(len(CHANNEL_ID)):
        print("チャンネル"+str(CHANNEL_ID[i])+"の取得を開始("+str(i+1)+"/"+str(len(CHANNEL_ID))+")")
        logging_channel(CHANNEL_ID[i])

