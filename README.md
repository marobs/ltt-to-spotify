# ltt-to-spotify
A web app that adds a little bit of functionality and integration between the front page of reddit.com/r/listentothis and Spotify.

### Features and Routes


#### ltt-to-spotify

r/listentothis to Spotify page, which allows the user to add songs from reddit.com/r/listentothis to their spotify playlists. This page works by querying reddit for songs from the subreddit (query will be specifiable), displaying these songs and associated data (if the user has saved the song, its genre, if it is already part of the selected paylist, etc.). Full features hoping to be included are:

1. List all user playlists along with associated data (image, name, description, etc.)
2. Display songs from r/listentothis with associated data, including:
   1. Artist/song is present on the playlist
   2. If if the song is saved
   3. If the song has been listened to before
   4. Album art
   5. Genre
   6. Artist genre, description, if followed by user, etc.
   7. Top song by artist
3. Color-coding/styling of genre tags
4. Ability to organize r/listentothis songs by genre or reddit order
5. Support multiple reddit searches (based on reddit API)
6. **Stretch Goal**: Give ability to stream related songs from Spotify


#### playlists

List all playlists with images, descriptions, etc., allowing selection of one playlist. Selecting a playlist brings up a page giving a visualization of the playlist, including:

1. Genre composition
2. Average plays
3. History
4. Graph of when songs were added
5. Anything else exposed by Spotify


#### history

Visualize data for last X songs listened to--could mirror playlist data visualization. Possibly includes which playlists the song is part of in the user's library.


#### search

Allows the user to search across all of their playlists, hopefully using elastic search for responsive, flexibile searching. Searches for all possible Spotify entities like song, artist, etc. to determine which playlists include that artist/song/etc.
