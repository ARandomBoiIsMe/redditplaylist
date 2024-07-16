import praw
import prawcore

def initialize_reddit(config):
    client_id = config['REDDIT']['CLIENT_ID']
    client_secret = config['REDDIT']['CLIENT_SECRET']

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='YouTube Playlist Generator by ARandomBoiIsMe'
    )

def validate_subreddit(reddit, sub_name):
    print("Checking if subreddit exists...")
    
    if sub_name.strip() == '' or sub_name is None:
        return None

    try:
        print(f"r/{sub_name} exists.")
        return reddit.subreddits.search_by_name(sub_name, exact=True)[0]
    except prawcore.exceptions.NotFound:
        return None

def fetch_youtube_posts(subreddit, args):
    print("Fetching posts with YouTube links from subreddit...")

    posts = []

    if args.filter == 'new':
        posts = subreddit.new(limit=args.number)
    elif args.filter == 'top':
        posts = subreddit.top(limit=args.number)
    elif args.filter == 'hot':
        posts = subreddit.hot(limit=args.number)

    posts = [post for post in posts if "youtube" in post.url or "youtu.be" in post.url]

    return posts