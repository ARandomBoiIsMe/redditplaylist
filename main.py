import re

from helpers import reddit, config, argparser, youtube

YOUTUBE_ID_REGEX = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|shorts\/|(?:(?<=youtu.be\/)))(?P<id>[\w-]{11})(?:\S+)?"
CONFIG = config.load_config()

def main():
    parser = argparser.initialize_argparse()
    args = parser.parse_args()

    reddit_ = reddit.initialize_reddit(CONFIG)

    subreddit = reddit.validate_subreddit(reddit_, args.subreddit)
    if not subreddit:
        print(f"r/{args.subreddit} does not exist.")
        exit()

    posts = reddit.fetch_youtube_posts(subreddit, args)
    if posts == []:
        print(f"No YouTube links found.")
        exit()

    video_ids = [re.search(YOUTUBE_ID_REGEX, post.url).group("id") for post in posts]

    youtube_ = youtube.initialize_youtube(CONFIG)
    youtube.add_to_playlist(
        youtube_,
        args.playlist_name or args.subreddit,
        args.playlist_type,
        video_ids,
        args.quota
    )

main()