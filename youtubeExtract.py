#Extracting data from youtube

from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError #pip install google-api-python-client
import oauth2client.tools as o2ctools #pip install oauth2client
import pandas as pd #pip install pandas
import matplotlib as plt
#import oauth2client.tools.argparser #pip install oauth2client
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps



def extractYT(game):
    
    reload(o2ctools) # changing argument of argparser did not work

    # Please ensure that you have enabled the YouTube Data API for your project.
    DEVELOPER_KEY = "AIzaSyCgajX4_9JeNgLvk9-6OEbYPVSCBy_2vCc" 
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
 
    o2ctools.argparser.add_argument("--q", help="Search term", default = game)
    #change the default to the search term you want to search
    o2ctools.argparser.add_argument("--max-results", help="Max results", default=50)
    #default number of results which are returned. It can very from 0 - 50
    args =o2ctools. argparser.parse_args()
    options = args
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
     # query term.
    search_response = youtube.search().list(
        q=options.q,
        type="video",
        part="id,snippet",
        maxResults=options.max_results
    ).execute()
    videos = {}
    channels = {}
    channelsName = {}
    # Add each result to the appropriate list, and then display the lists of
     # matching videos.
     # Filter out channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":      
     #videos.append("%s" % (search_result["id"]["videoId"]))
         videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
         channels[search_result["id"]["videoId"]] = search_result["snippet"]["channelId"]
         channelsName[search_result["id"]["videoId"]] = search_result["snippet"]["channelname"]
    #print "Videos:\n", "\n".join(videos), "\n"
    s = ','.join(videos.keys())

    videos_list_response = youtube.videos().list(
        id=s,
        part='id,statistics'
    ).execute()
    #videos_list_response['items'].sort(key=lambda x: int(x['statistics']['likeCount']), reverse=True)
    #res = pd.read_json(json.dumps(videos_list_response['items']))
    res = []
    for i in videos_list_response['items']:
        temp_res = dict(v_id = i['id'], v_title = videos[i['id']],
                        channel_id = channels[i['id']], channel_name = channelsName[i['id']] )
        temp_res.update(i['statistics'])
        res.append(temp_res)
    df = pd.DataFrame.from_dict(res)
    #cleaning
    #argparse.remove_argument('--h1')
    #argparse.remove_argument('--max-results')
    
    return(df)

# Examples of the most popular games
popular_games = ["Counter Strike", "Dota 2", "Hearthstone",
    "League of Legends", "Diablo III","World of Tanks","Minecraft",
    "Battlefield 4", "Smite","Fallout 4", "Grand Theft Auto V",
    "Heroes of the Storm", "ARK: Survival Evolved", "Guild Wars 2",
    "Star Wars: The Old Republic", "Star Craft II", "Spider Solitare",
    "Final Fantasy XIV", "Call of Duty"]
                 

RES = extractYT("World of Warcraft") # initialize final data.frame

for game in popular_games:
    df = extractYT(game)
    RES = RES.append(df, ignore_index = True)

# printing
def printdf(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#RES = RES.sort(['channel_id','likeCount'], ascending=[False,True])
#printdf(RES)

users = RES.groupby(['channel_id','likeCount'].sum())


