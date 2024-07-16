import argparse

def initialize_argparse():
    parser = argparse.ArgumentParser(
        prog='redditplaylist',
        description='Generates YouTube playlists from Reddit posts'
    )

    parser.add_argument('subreddit', help='The target subreddit')
    parser.add_argument('-f', '--filter', help='The filter for posts',
                        default='new', choices=['new', 'top', 'hot'])
    parser.add_argument('-n', '--number', help='The number of posts', default=10, type=int)
    parser.add_argument('-pn', '--playlist-name', help='The name of the playlist')
    parser.add_argument('-pt', '--playlist-type', help='The playlist type',
                        default='private', choices=['private', 'public', 'unlisted'])
    parser.add_argument('-q', '--quota', help='See current quota usage (This is just an estimate. Go to https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas to view your actual quota value.)',
                        action='store_true')

    return parser