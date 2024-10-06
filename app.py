import os
import sys
import openai  # Import the openai module
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Path to the client_secrets.json file for OAuth 2.0
client_secrets_file = "client_secrets.json"

# OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up the OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# YouTube API scopes
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_credentials():
    # Perform the OAuth 2.0 flow for authentication
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    
    # Use run_local_server for the authentication process
    credentials = flow.run_local_server(port=0)
    return credentials

def create_playlist(youtube, playlist_name, description):
    # Create a new playlist
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": description,
                "tags": ["sample playlist", "API call"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"  # Set to 'public' if you want the playlist to be public
            }
        }
    )
    response = request.execute()
    return response["id"]

def video_exists(youtube, video_id):
    # Check if the video exists
    request = youtube.videos().list(
        part="id",
        id=video_id
    )
    response = request.execute()
    return len(response['items']) > 0

def add_song_to_playlist(youtube, playlist_id, video_id):
    # Check if the video exists before adding it
    if not video_exists(youtube, video_id):
        print(f"Video not found: {video_id}")
        return None
    
    # Add a song to the playlist
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

def get_similar_songs(song_name, num_songs=5):
    # Generate a list of similar songs using the latest OpenAI API
    prompt = f"List {num_songs} songs similar to {song_name}:"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for generating music playlists."},
            {"role": "user", "content": prompt}
        ]
    )

    # Process the response
    similar_songs = response.choices[0].message.content.strip().split('\n')
    # Clean up the list of songs
    similar_songs = [s.strip() for s in similar_songs if s.strip()]  # Remove empty lines and spaces
    similar_songs = similar_songs[1:-1]  # Remove the first and last elements of the list

    # Remove numbering from the beginning of each song
    similar_songs = [s.split('. ', 1)[-1] for s in similar_songs]

    return similar_songs

def load_playlists_from_file():
    # Load playlists from the .playlists file
    if os.path.exists('.playlists'):
        with open('.playlists', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_playlist_to_file(playlist_name, playlist_url, songs):
    # Load existing playlists
    playlists = load_playlists_from_file()
    
    # Add the new playlist
    playlists.append({
        "name": playlist_name,
        "url": playlist_url,
        "songs": songs
    })
    
    # Save the updated playlists to the file
    with open('.playlists', 'w') as file:
        json.dump(playlists, file, indent=4)

def delete_all_playlists(youtube):
    # Load playlists from file
    playlists = load_playlists_from_file()

    # Delete each playlist using the YouTube API
    for playlist in playlists:
        playlist_id = playlist["url"].split("list=")[-1]
        try:
            youtube.playlists().delete(id=playlist_id).execute()
            print(f"Deleted playlist: {playlist['name']}")
        except googleapiclient.errors.HttpError as e:
            print(f"Failed to delete playlist {playlist['name']}: {e}")

    # Clear the playlists file
    with open('.playlists', 'w') as file:
        file.write('[]')  # Write an empty JSON array

def search_songs_and_add_to_playlist(song_name, num_songs=5):
    # Get a list of similar songs using OpenAI
    similar_songs = get_similar_songs(song_name, num_songs)

    # List to store song names and video IDs
    songs_and_links = []

    # Authenticate and build the YouTube API client
    credentials = get_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Create a new playlist
    playlist_name = f"Playlist for {song_name}"
    description = f"Automatically generated playlist with songs similar to {song_name}"
    playlist_id = create_playlist(youtube, playlist_name, description)
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    
    # Add songs to the playlist and store their names
    for index, song in enumerate(similar_songs):
        # Search for the song on YouTube and get its URL
        request = youtube.search().list(
            part='snippet',
            q=song,
            type='video',
            maxResults=1
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id']['videoId']
            add_song_to_playlist(youtube, playlist_id, video_id)
            songs_and_links.append((f"song {index + 1}: {song}", video_id))
    
    # Display the results
    for song, video_id in songs_and_links:
        print(song)
    print(f"playlist: {playlist_url}")
      
    # Save playlist information to a file
    save_playlist_to_file(playlist_name, playlist_url, [song for song, _ in songs_and_links])

# Usage example
if __name__ == "__main__":
    # Check for the --clean flag
    if '--clean' in sys.argv:
        # Authenticate and build the YouTube API client
        credentials = get_credentials()
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
        delete_all_playlists(youtube)
    else:
      # Get user input for the song name and number of songs
      song_name = input("Enter the name of the song: ")
      num_songs = int(input("Enter the number of songs to add to the playlist: "))
      search_songs_and_add_to_playlist(song_name, num_songs)
