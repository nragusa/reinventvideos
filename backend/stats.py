import boto3
import json
import os
import re
import sys
import threading
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

HERE = os.path.dirname(os.path.realpath(__file__))
SITE_PKGS = os.path.join(HERE, 'site-packages')
sys.path.append(SITE_PKGS)

from apiclient.discovery import build
from apiclient.errors import HttpError
from algoliasearch import algoliasearch

"""Configuration from environment variables"""
YOUTUBE_DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
ALGOLIA_DEVELOPER_KEY = os.environ['ALGOLIA_DEVELOPER_KEY']
ALGOLIA_APP = os.environ['ALGOLIA_APP']
ALGOLIA_INDICIES = os.environ['ALGOLIA_INDICIES']
PODCAST_TABLE = os.environ['PODCAST_TABLE']
ddb = boto3.resource('dynamodb')
PODCAST_TABLE_CLIENT = ddb.Table(PODCAST_TABLE)

"""Other global variables"""
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

PLAYLISTS = {
    '2018': ['PLWaYLZud5zZm15KUkMPY8o3AC-wGshVU2'],
    '2017': ['PLhr1KZpdzukdagfQxs6WdIigw0XwG2kr8', 'PLhr1KZpdzukc-1lMQ8iugc82jaVUt_Nej',
             'PLhr1KZpdzukewxjrgeVIGw49tiIbkqt0Z', 'PLhr1KZpdzukf6N6R1cmRWj2BvqvXDyBYo',
             'PLhr1KZpdzukeKUChZG8SdYipk7INwphQm', 'PLhr1KZpdzukeZRZzU9Mi6rWgVFFBRbeK6',
             'PLhr1KZpdzukdHl2gKK09p6PihKNkA-5yC', 'PLhr1KZpdzukf34vxrO18JKjMLT_5tGNJi',
             'PLhr1KZpdzukcNitpsUCr-_oQJ9HSQT8Vg', 'PLhr1KZpdzuketnzOgclLSIXCacM84ryFX',
             'PLhr1KZpdzukdLDsITEkaUyqaygujHolVc', 'PLhr1KZpdzukeiPpqZ3C7r-6DDqr0pWTow',
             'PLhr1KZpdzukdDwiKgdXe4uQHt7H9BiaR3', 'PLhr1KZpdzukem5E3-TgQARED4qu4-TnPf',
             'PLhr1KZpdzukckLI_fQMQagOsAWFfzsGKa', 'PLhr1KZpdzukcGVzIVFTy-j358ZoK9cvrF',
             'PLhr1KZpdzukc6GguNSQ9W0ylmx5Rckll7', 'PLhr1KZpdzuke7G4Ab6M2JbMiG5-I7unN0',
             'PLhr1KZpdzukcJMsbdeLy_8eBaLIxtHy7p', 'PLhr1KZpdzukfUH7X77qjz1jU3suHhkE_I',
             'PLhr1KZpdzukdYX4C4FN3EJ6DOMqyDiO6y', 'PLhr1KZpdzuke9Y-Kv0RiJx4ZPfXr0AG4a',
             'PLhr1KZpdzukeTKB5jxl-qFuQTFTIlRlmp', 'PLhr1KZpdzukeKA9qHeVYr8kSXpwEwUgHx',
             'PLhr1KZpdzukfHOEEc7pQT14-fZDCK1Fto', 'PLhr1KZpdzukedIiqJhiIt8tKFfUouGV9u',
             'PLhr1KZpdzukdV5yMZ04eOFuyYTHKHLXRI', 'PLhr1KZpdzukdBIUJUjtUbUiXlhGqsy4M-',
             'PLhr1KZpdzukeIL3FuDSNCXgouZz_SHKF-', 'PLhr1KZpdzukcsHg8KGlmUKrzYDhXTEsZA',
             'PLhr1KZpdzukcXiSxwmBQ-Al4nl7gZj_kT', 'PLhr1KZpdzukftFAHnh0_7VffqL_D4i-29',
             'PLhr1KZpdzukfnwHQ7RG6tQ6hh7zHUEnME', 'PLhr1KZpdzukeNslXGpXVR3r8OohMbP8W6',
             'PLhr1KZpdzukfetXNIwkp6X09JaA2h2s4L'],
    '2016': ['PLhr1KZpdzukekjWDduFy6zLmefzpkpql5', 'PLhr1KZpdzukexYSNcIj9iBbmn9jYKu2pu',
             'PLhr1KZpdzukefNs5YEKzQF26RhKxFOMeI', 'PLhr1KZpdzukcLUKD2ej8AKYR-nryjGGnF',
             'PLhr1KZpdzukcDSfiAaLhdx9IlIDw82tIt', 'PLhr1KZpdzukfYBoBNGKS3axyHW9-JClQb',
             'PLhr1KZpdzukf7b2uO2wkjM7fiQ-dPGvLe', 'PLhr1KZpdzukdi1XNNdkDwQqOWObl5FDsV',
             'PLhr1KZpdzukdWnKfVrKU7hItlHAxhOqCN', 'PLhr1KZpdzukc97mkL2-TOE-vJtp22c1yc',
             'PLhr1KZpdzukfuH92ynLBeCo0tpH68z7ul', 'PLhr1KZpdzukfcsAHiuuTdBPWpeDZTVm_M',
             'PLhr1KZpdzukdog-d8yT5L7xSlROlj9_tg', 'PLhr1KZpdzukdg8fpf-GPZmIDeBa-iY6Nl',
             'PLhr1KZpdzukdPNwdTvedPlGp90Qbz1VVB', 'PLhr1KZpdzukccE_5SXE-sTKoxtcT5vaKQ',
             'PLhr1KZpdzukdAg4bXtTfICuFeZFC_H2Xq', 'PLhr1KZpdzukcqTmgvR6QpFg7gr0tqQTKg',
             'PLhr1KZpdzukeLjYUf65Fxe3m0AlpsgjEi', 'PLhr1KZpdzukdqHFnM5eaLWUDYmt4C4iYR',
             'PLhr1KZpdzukeSc8-VFvtw-6ZadA8r3LQ1', 'PLhr1KZpdzukdE6cOC8P9Wj5YkrVi68Giq',
             'PLhr1KZpdzukd_MAdql2hk3NeB63iTzuWr', 'PLhr1KZpdzukeM5wqWm-OjaG7L8Jp5F74U',
             'PLhr1KZpdzukdTeIj4DEIZ-OO2EkzDHPPr', 'PLhr1KZpdzukd0NNTmnX6Ba8k7xxWYc87R',
             'PLhr1KZpdzukf0LNFkQu6e_gsuYts0dips', 'PLhr1KZpdzukfBiT0JXadXiAZPoikh5luq'],
    '2015': ['PLhr1KZpdzukdTMmq1gkXs7g6WIIXtL5r9', 'PLhr1KZpdzukccVDO15MGT3EZRCA9XZvcn',
             'PLhr1KZpdzukc9aw8-gnLmyralfsBv7zcR', 'PLhr1KZpdzukcjwZgFBBTmSNPjf_gImgfx',
             'PLhr1KZpdzukcaPbx7Hsn4tsspfubBIGlc', 'PLhr1KZpdzukf_f41uFoQtqnDGIVqaureL',
             'PLhr1KZpdzukeH9VMPbNHMCXl_NrVc1JGe', 'PLhr1KZpdzuke5pqzTvI2ZxwP8-NwLACuU',
             'PLhr1KZpdzukeMbjRqGswHX38DCqOHZ5GA', 'PLhr1KZpdzukfVW6NrpDzdT6Sej0p5POkN',
             'PLhr1KZpdzukdsblOEVXrCYtvUsDakzYJI', 'PLhr1KZpdzukdRxs_pGJm-qSy5LayL6W_Y',
             'PLhr1KZpdzukcBfuUdMOKc94mnrQhBpdmw'],
    '2014': ['PLhr1KZpdzukeRu_nW7dakrbU8LuP3EhER', 'PLhr1KZpdzukf6YADEpM6nFEZs7VDhEs5U',
             'PLhr1KZpdzukeELGlIL-jJgvzjiZ_wR9tN', 'PLhr1KZpdzukcYj6y9nm5jVtt5fQ1-XClr',
             'PLhr1KZpdzukcJvl0e65MqqwycgpkCENmg', 'PLhr1KZpdzukfOfdstfSQVAvUrjBvnGd4i',
             'PLhr1KZpdzukeZzTZ7Cn0_4a02AnBbAUNu', 'PLhr1KZpdzukcavcJM0hxMixqs9C1-KnHH',
             'PLhr1KZpdzukcbGxX4i__0ftN65PNgltDm', 'PLhr1KZpdzukeiCFgRccZ677GhHoP1OD8S',
             'PLhr1KZpdzukc-h3mgX4RHG0qFSH4SXxlW', 'PLhr1KZpdzukfrGo6YLeysVFZvwJw6gUya',
             'PLhr1KZpdzukfGd-Raw2TT6XKbSRkpJifG', 'PLhr1KZpdzukeEDdaSY-HHJuX30WsoGhuW',
             'PLhr1KZpdzukdFPw42zUAWjbqtFwKTxaKy', 'PLhr1KZpdzukd8KRz4wQd5VB9DMxrV-QLp',
             'PLhr1KZpdzukdoUVMT6VYIC7ByzqOsT9Ok', 'PLhr1KZpdzuketO0VQtLwchbqJLO4vDjAq',
             'PLhr1KZpdzukcMN8ixupMLwz4isu-KAf0D', 'PLhr1KZpdzukezLULL9sbvOLNLLiTu5zKu',
             'PLhr1KZpdzukdxQFD0-7BM3yaQVrCWrIzW'],
    '2013': ['PLhr1KZpdzukfOvujPQP1mK48v-417DB8o'],
    '2012': ['PLhr1KZpdzukfA3m0jEQmkeGU4SHkSoPZZ']}

"""Compile regular expressions once for frequent reuse"""
REMOVE_SPACE = re.compile(r'\s+')
REMOVE_NONALPHA = re.compile(r'[\W_]+')
SESSION_REGEX = re.compile(r'\(?[A-Z]{2,6}[0-9]{2,3}R?(-R[0-9])?\)?')
YEAR_REGEX = re.compile(r'20[1-9]{1}[0-9]{1}')

class Playlist(object):
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    def __str__(self):
        return self.pid


class Video(Playlist):
    def __init__(self, vid, title, description, playlist_id):
        self.vid = vid
        self.title = title
        self.description = description
        self.views = 0
        self.likes = 0
        self.dislikes = 0
        self.playlist_id = playlist_id
        self.thumbnail = ''
        self.published = ''
        self.tags = []
        self.session_id = ' '
        self.podcast_url = ''
        stripped_title = re.sub(REMOVE_SPACE, '', self.title)
        session = re.search(SESSION_REGEX, stripped_title)
        if session:
            self.session_id = REMOVE_NONALPHA.sub('', session.group())

    def __str__(self):
        return self.title

    def get_published_year(self):
        """Calculates published year. Sometimes published_year from
            youtube API does not line up with title. Prefer the title
            year over the published_year from YouTube.
        """
        stripped_title = re.sub(REMOVE_SPACE, '', self.title)
        year = re.search(YEAR_REGEX, stripped_title)
        if year:
            # Found year in title
            if year.group() == self.published.split('-')[0]:
                return self.published.split('-')[0]
            else:
                # Year in title doesn't match YouTube's published year
                print('Found {} in title {}, but published year is {}'.format(
                    year.group(), self.title, self.published.split('-')[0]
                ))
                return year.group()
        else:
            # Stick with year published from YouTube
            return self.published.split('-')[0]

    def get_level(self):
        """Determines the level of the session that's found in the 
            title of the YouTube video. Returns No Level if a level
            was not found in the title.
        """
        stripped_title = re.sub(REMOVE_SPACE, '', self.title)
        session = re.search(SESSION_REGEX, stripped_title)
        if session:
            # Found session in title
            level = re.sub(r'\D', '', session.group().split('-')[0])
            if len(level) == 3:
                # Return level like 100, 200, etc.
                return level[0] + '00'
            else:
                # Sub-100 level found
                return '< 100'
        else:
            # No level was found
            return 'No Level'

def update_podcast_url(video):
    """Query the DDB table for this video. If found, it means
    we have a podcast m4a stored in S3. Otherwise, return no
    podcast.
    """
    try:
        response = PODCAST_TABLE_CLIENT.query(
            KeyConditionExpression=Key('session').eq(video.session_id) & Key('year').eq(video.get_published_year())
        )
    except ClientError as error:
        print('Problem getting data from DynamoDB: {}'.format(error))
        return False
    else:
        if response['Count'] == 1:
            video.podcast_url = response['Items'][0]['url']
            return True

def work_on_playlist(playlist_year):
    """Iterates over the playlists from a specific year, gets details
    about the playlist, then gets individual video detail about each video
    within the playlist. Video detail information is formatted and stored
    in DynamoDB, and also written to a local json file to be uploaded later
    to S3 as a cache."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_DEVELOPER_KEY)
    videos = {}
    playlists = []
    for playlist in PLAYLISTS[playlist_year]:
        playlists.append(Playlist(playlist, playlist_year))
    for playlist in playlists:
        """Get details about this playlist, including all the videos"""
        print('Working on playlist {} from year {}'.format(
            playlist.pid, playlist_year))
        try:
            playlistitems_list_request = youtube.playlistItems().list(
                part='contentDetails',
                maxResults=50,
                playlistId=str(playlist.pid)
            )
        except HttpError as error:
            print('Problem getting playlist items for playlist {}: {}'.format(
                playlist.pid, error))
        while playlistitems_list_request:
            videos_response = playlistitems_list_request.execute()
            for item in videos_response.get('items', []):
                if 'contentDetails' in item:
                    vid = item['contentDetails'].get('videoId', '')
                    if vid != '':
                        """Get details about this video"""
                        try:
                            video_response = youtube.videos().list(
                                part='snippet,statistics',
                                id=vid
                            ).execute()
                        except HttpError as error:
                            print('Problem getting video statistics for video {}: {}'
                                .format(vid, error))
                        for item in video_response.get('items', []):
                            if 'snippet' in item:
                                video = Video(
                                    vid=item['id'],
                                    title=item['snippet'].get('title', ''),
                                    description=item['snippet'].get(
                                        'description', ''),
                                    playlist_id=playlist.pid
                                )
                                video.thumbnail = item['snippet']['thumbnails']['high']['url']
                                video.published = item['snippet']['publishedAt']
                                video.tags = item['snippet'].get('tags', [])
                                if 'statistics' in item:
                                    video.views = int(
                                        item['statistics'].get('viewCount'))
                                    video.likes = int(
                                        item['statistics'].get('likeCount'))
                                    video.dislikes = int(
                                        item['statistics'].get('dislikeCount'))
                                if video.session_id != ' ':
                                    update_podcast_url(video)
                                videos[item['id']] = video
                            else:
                                print('No snippet found in video')
                    else:
                        print('No video id found')
                else:
                    print('No content found for video')
            playlistitems_list_request = youtube.playlistItems().list_next(
                        playlistitems_list_request, videos_response)

    """Added all video information into DynamoDB"""
    cache = []
    print('Adding playlist from year {} to local cache'.format(playlist_year))
    for video in videos.values():
        cache.append(
            dict(
                vid=video.vid,
                title=video.title,
                description=video.description,
                published_year=video.get_published_year(),
                thumbnail=video.thumbnail,
                views=video.views,
                likes=video.likes,
                dislikes=video.dislikes,
                tags=video.tags,
                level=video.get_level(),
                podcast=video.podcast_url
            )
        )
    """Write this data to a local file to create a cache in S3"""
    with open('/tmp/videos-{}.json'.format(playlist_year), 'w') as f:
        json.dump(cache, f)


def main(event, context):
    """Create a seperate thread for each year with playlists"""
    threads = []
    for year in PLAYLISTS.keys():
        t = threading.Thread(target=work_on_playlist, args=(year,))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()

    """Aggregate all cache files into a single file"""
    cache = dict(data=[])
    print('Aggregate files into single cache')
    with open('/tmp/videos.json', 'w') as final:
        for year in PLAYLISTS.keys():
            with open('/tmp/videos-{}.json'.format(year), 'r') as f:
                local = json.load(f)
                cache['data'].extend(local)
        json.dump(cache['data'], final)
    
    """Read local cache and replace objects in indicies"""
    print('Updating Algolia indicies')
    client = algoliasearch.Client(ALGOLIA_APP, ALGOLIA_DEVELOPER_KEY)

    all_indicies = ALGOLIA_INDICIES.replace(' ', '').split(',')
    with open('/tmp/videos.json', 'r') as cache:
        # Load data from cache
        objects = json.load(cache)
        print('Loaded objects from cache')
        for index in all_indicies:
            client_index = client.init_index(index)
            request_options = algoliasearch.RequestOptions({'safe': True})
            try:
                print('Updating index {}'.format(index))
                client_index.replace_all_objects(objects, request_options)
            except Exception as error:
                print('Problem updating index: {}'.format(error))

