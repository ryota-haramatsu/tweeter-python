import tweepy
import json
import requests

"""
外部ファイルからAPI接続に必要な情報をimportする

main.pyと同じ階層にconfig.pyを配置
"""
from config import consumer_key, consumer_secret, access_token, access_token_secret

"""
Tweepyを使ってAPIを使うための準備
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def show_public_tweets():
  """
  公開タイムラインのツイートを取得

  おそらく日本?の全ユーザの公開ツイートが対象となる。
  ツイート取得件数は最新20件

  Getting started — tweepy 3.8.0 documentation
  http://docs.tweepy.org/en/latest/getting_started.html#hello-tweepy
  """
  public_tweets = api.home_timeline()
  for tweet in public_tweets:
      print(tweet.text)

def show_user_profile():
  """
  ユーザのプロフィール情報を表示

  http://docs.tweepy.org/en/latest/getting_started.html#models
  """
  user = api.get_user('FUKADA0318')
  print(user.screen_name)
  print(user.followers_count)

def show_media_url():
  """
  深田えいみのタイムラインからツイートを読み込む

  user_timelineの使い方
  http://docs.tweepy.org/en/latest/api.html?highlight=user_timeline#API.user_timeline
  """
  user_id = "FUKADA0318"
  statuses = api.user_timeline(id=user_id, count=4)

  count = 1
  for status in statuses:
    """
    コメントアウトしている部分はデバッグに使ったコードです。動画ではカットした部分も含みます
    """
    # if count < 4:
    #   count = count + 1
    #   continue
    # print(status)
    # print(json.dumps(status._json))
    for entity in status.extended_entities["media"]:
      img_url = entity["media_url"]
      print(img_url)
    # print(media)
    # print(media[0]["media_url"])
    break

"""
urlからファイルをダウンロードする

以下のコードは覚える必要はないです。コピペでOKです。
"""
def download_image(url, file_path):
  r = requests.get(url, stream=True)

  if r.status_code == 200:
    with open(file_path, "wb") as f:
      f.write(r.content)

def main():
  """
  深田えいみのツイートを読み込み、添付画像をダウンロードする

  Cursor Tutorial — tweepy 3.8.0 documentation
  http://docs.tweepy.org/en/latest/cursor_tutorial.html

  例外（try,excpet）の使い方
  とほほのPython入門 - 制御構文 - とほほのWWW入門
  http://www.tohoho-web.com/python/control.html
  """
  user_id = "FUKADA0318"
  for page in tweepy.Cursor(api.user_timeline, id=user_id).pages(20):
    for status in page:
      try:
        for media in status.extended_entities["media"]:
          media_id = media["id"]
          img_url = media["media_url"]
          print(media_id)
          print(img_url)

          download_image(url=img_url, file_path="/Users/haramatsuryota/images/{}.jpg".format(media_id))
      except Exception as e:
        print(e)


if __name__ == "__main__":
    main()