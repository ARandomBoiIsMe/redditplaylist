# redditplaylist
Script to generate YouTube playlists from Reddit posts.

## Installation
- [Install Python](https://www.python.org/downloads/). Add to PATH during the installation.
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Unzip the ZIP file.
- Open your command prompt and change your directory to that of the unzipped files ```cd unzippedfoldername```.
- Install the required packages  :
  ```
  pip install -r requirements.txt
  ```

## Configuration
- [Create a Reddit App](https://www.reddit.com/prefs/apps/)(script) and get your ```client_id``` and ```client_secret```.
- Edit the ```config.ini``` file with your details:
  ```
  [REDDIT]
  CLIENT_ID = your_client_id
  CLIENT_SECRET = your_client_secret
  ```
- Visit [Google's guide to using their developer platform](https://developers.google.com/workspace/guides/get-started)
  - Create a Google Developer account
  - Create a new project
  - Enable the 'YouTube Data API v3' library
  - Set up OAuth and download the client_secrets json file
  - Store the file in this project's directory
  - Replace the XXXX value with the name of the client secret json file you downloaded:
```
[YOUTUBE]
CLIENT_SECRET_FILE = file_name.json
```

## Running the script
The script uses a command system to carry out actions:
```
usage: python main.py [-h] [-f {new,top,hot}] [-n NUMBER] [-pn PLAYLIST_NAME] [-pt {private,public,unlisted}] [-q]
                      subreddit

Generates YouTube playlists from Reddit posts

positional arguments:
  subreddit             The target subreddit

options:
  -h, --help            show this help message and exit
  -f {new,top,hot}, --filter {new,top,hot}
                        The filter for posts
  -n NUMBER, --number NUMBER
                        The number of posts
  -pn PLAYLIST_NAME, --playlist-name PLAYLIST_NAME
                        The name of the playlist
  -pt {private,public,unlisted}, --playlist-type {private,public,unlisted}
                        The playlist type
  -q, --quota           See current quota usage (This is just an estimate. Go to
                        https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas to view your actual
                        quota value.)
```

A  `subreddit` value is required by the script. All other values are optional with default values:
```
-f {new,top,hot}, --filter {new,top,hot}
                      Default: new
-n NUMBER, --number NUMBER
                      Default: 10
-pn PLAYLIST_NAME, --playlist-name PLAYLIST_NAME
                      Default: subreddit
-pt {private,public,unlisted}, --playlist-type {private,public,unlisted}
                      Default: private
-q, --quota           Default: false
```

## Some examples:
Creating a private playlist from the YouTube links found among the 10 newest posts in [r/TrueDoomMetal](https://www.reddit.com/r/TrueDoomMetal/):
```
python main.py TrueDoomMetal
```

Creating an unlisted playlist called 'Mine' from the YouTube links found among the 20 hottest posts in [r/Buckethead](https://www.reddit.com/r/Buckethead/):
```
python main.py Buckethead -f hot -n 20 -pn Mine -pt unlisted
```

Creating an public playlist from the YouTube links found among the top 7 posts in [r/Buckethead](https://www.reddit.com/r/Buckethead/), while checking quota usage:
```
python main.py Buckethead -f top -n 7 -pt public --quota
```

## Additional notes
- The `number` value does not specify how many videos will be in a playlist. It specifies how many posts will be scanned in the subreddit.
- YouTube's API limits requests via [quotas](https://developers.google.com/youtube/v3/determine_quota_cost). Each account is limited to 10,000 quotas per day.
