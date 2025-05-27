from ytmusicapi import YTMusic
import openai

ytmusic = YTMusic()

openai.api_key = 'Open Ai Api here'  

def detect_mood(feelings_text):
    prompt = f"What mood is reflected by the following feelings: '{feelings_text}'? Respond with only one word like 'happy', 'sad', 'energetic', 'romantic', 'relaxed', etc."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in analyzing human emotions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=5
    )

    mood = response['choices'][0]['message']['content'].strip().lower()
    return mood

def get_recommendations(mood):
    search_results = ytmusic.search(query=f"{mood} songs", filter="playlists")

    if not search_results:
        print("⚠️ No playlists found. Try another mood.")
        return []

    playlist_id = search_results[0]['browseId']
    playlist = ytmusic.get_playlist(playlist_id, limit=5)

    songs = []
    for track in playlist['tracks']:
        title = track['title']
        artist = track['artists'][0]['name']
        video_id = track['videoId']
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
        songs.append((f"{title} by {artist}", youtube_link))

    print("\n🎵 YouTube Music Recommendations:")
    for title, link in songs:
        print(f"  - {title}: {link}")

    return songs

def main():
    feelings = input("🧠 Enter how you're feeling right now: ")
    mood = detect_mood(feelings)
    print(f"🔎 Detected Mood: {mood.capitalize()}")
    get_recommendations(mood)

if __name__ == "__main__":
    main()

