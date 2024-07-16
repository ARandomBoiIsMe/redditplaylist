import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from .quota import get_quota, update_quota

CURRENT_QUOTA = get_quota()

def initialize_youtube(config):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = config["YOUTUBE"]["CLIENT_SECRET_FILE"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()

    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

def add_to_playlist(youtube, playlist_name, playlist_type, video_ids, see_quota):
    global CURRENT_QUOTA

    playlist_id = _find_playlist(youtube, playlist_name, see_quota)
    if playlist_id == None:
        playlist_id = _create_playlist(youtube, playlist_name, playlist_type, see_quota)

    print("Adding videos to playlist...")
    for id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": id
                    }
                }
            }
        )

        try:
            request.execute()
            CURRENT_QUOTA -= 50

            if see_quota:
                print("Current quota: ", CURRENT_QUOTA)
        except googleapiclient.errors.HttpError as error:
            if error.reason == "playlistContainsMaximumNumberOfVideos":
                print("The playlist has reached its video limit. No more videos can be added here.")
            elif error.reason == "videoNotFound":
                print("Video not found. Skipping.")
                continue
            elif error.reason == "playlistOperationUnsupported":
                print("This action is not supported on the chosen playlist.")
            elif error.reason == "quotaExceeded":
                print("You have exhausted your quota limit for the day.\nNo more videos can be added until "\
                       "the quota has been refreshed on the next day.")

            update_quota(CURRENT_QUOTA)
            exit()

    print("Videos added.")
    update_quota(CURRENT_QUOTA)

def _find_playlist(youtube, playlist_name, see_quota):
    global CURRENT_QUOTA

    print("Checking if playlist exists...")

    request = youtube.playlists().list(
        part="snippet",
        maxResults=50,
        mine=True
    )

    response = None
    try:
        response = request.execute()
        CURRENT_QUOTA -= 1

        if see_quota:
            print("Current quota: ", CURRENT_QUOTA)
    except googleapiclient.errors.HttpError as error:
        print("Exception occured: ", error.reason)

        update_quota(CURRENT_QUOTA)
        exit()

    id = None
    for item in response.get("items"):
        if playlist_name == item.get("snippet").get("title"):
            id = item.get("id")
            break

    if id:
        return id

    # Iterates over all pages
    # While less efficient, this approach uses far less quotas (1 quota per request) over
    # using the Search API (100 quotas per request)
    while True:
        if not response.get("nextPageToken"):
            return None

        request = youtube.playlists().list(
            part="snippet",
            maxResults=50,
            mine=True,
            pageToken=response.get("nextPageToken")
        )

        response = None
        try:
            response = request.execute()
            CURRENT_QUOTA -= 1

            if see_quota:
                print("Current quota: ", CURRENT_QUOTA)
        except googleapiclient.errors.HttpError as error:
            print("Exception occured: ", error.reason)

            update_quota(CURRENT_QUOTA)
            exit()

        id = None
        for item in response.get("items"):
            if playlist_name == item.get("snippet").get("title"):
                id = item.get("id")
                break

        if id:
            return id

def _create_playlist(youtube, playlist_name, playlist_type, see_quota):
    global CURRENT_QUOTA

    print(f"{playlist_name} does not exist. Creating...")

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": playlist_name
          },
          "status": {
            "privacyStatus": playlist_type
          }
        }
    )

    response = None
    try:
        response = request.execute()
        CURRENT_QUOTA -= 50

        if see_quota:
            print("Current quota: ", CURRENT_QUOTA)
    except googleapiclient.errors.HttpError as error:
        if error.reason == "maxPlaylistExceeded":
            print("You have reached the maximum number of playlists for your channel.")
        else:
            print("Exception occured: ", error.reason)

        update_quota(CURRENT_QUOTA)
        exit()

    return response.get("id")