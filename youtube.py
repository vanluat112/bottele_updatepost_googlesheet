from googleapiclient.discovery import build
from datetime import datetime
import urllib.request
import json

# API information
api_service_name = "youtube"
api_version = "v3"
# API key
api_key = "AIzaSyBOCNhndXJAbjYgFrMv3meB357E6C2C7qM"
# API client
youtube = build(api_service_name, api_version, developerKey = api_key)

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()


def video_info(video_response):
    try:
        video_info = {
                    "title":         "",
                    "publish_time":  "",
                    "link_video":    ""
                 
        }
        items = video_response.get("items")[0]
        # get the snippet, statistics & content details from the video response
        snippet                     = items["snippet"]
        # get infos from the snippet
        video_info["title"]         = snippet["title"]
        video_info["publish_time"]  = snippet["publishedAt"]

        # get stats infos
       
    finally:
        return video_info 

def get_info_first_video(channel_id):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(api_key, channel_id)
    video_ids=[]
    video_links = []
    url = first_url
    
    inp = urllib.request.urlopen(url)
    resp = json.load(inp)
    for i in resp['items']:
        if i['id']['kind'] == "youtube#video":
            video_links.append(base_video_url + i['id']['videoId'])
    # split URL parts
    for i in range(len(video_links)):
        link = video_links[i].split("watch?v=")[1]
        video_ids.append(link)
    video_response = get_video_details(youtube, id=video_ids)
    video_info = {
                    "title":         "",
                    "link_video":    ""          
        }
    items = video_response.get("items")[0]
        # get the snippet, statistics & content details from the video response
    snippet                     = items["snippet"]
        # get infos from the snippet
    video_info["title"]         = snippet["title"]
    publish_time = snippet["publishedAt"].split('T')[0]
    video_info["link_video"]  = video_links[0]
    date_time_obj = datetime.strptime(publish_time, '%Y-%m-%d')
    now = datetime.now()
    # if date_time_obj.day==now.day:
    #     return video_info
    # else:
    #     return None
    print(video_info)
get_info_first_video('UCeKrBHxTzAxp4ypgUoauBAQ')