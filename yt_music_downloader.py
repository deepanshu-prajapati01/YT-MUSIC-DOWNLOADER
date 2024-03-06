# THIS CODE CAN RETRIEVE SONG URL FROM ITS NAME
import os, re
from youtubesearchpython import VideosSearch
from pytube import YouTube
from pytube.cli import on_progress

owner_folder = "Songs-Deepanshu-Prajapati01"
path_to_save_files = f"{os.path.expanduser('~')}\\Music\\{owner_folder}"

# TO CATCH UP THE ERROR - INCASE IT OCCURS CONFIRMING THE PATH TO SAVE FILES.
try:
  os.chdir(path_to_save_files)
except:
  os.chdir(f"{os.path.expanduser('~')}\\Music")
  if not os.path.exists(owner_folder):
    os.mkdir(owner_folder)
    os.chdir(path_to_save_files)


def download_song(song_name):
  # TAKING SONG NAME ALSO REMOVING ANY CHARACTER THAT MAY CAUSE ANY ERROR.
  song_name = f"{song_name} song"
  song_name = re.sub(r'[^\x00-\x7f]', '', song_name)

  # RETREIVING THE URL OF THE VIDEO SONG.
  try:
    videosSearch = VideosSearch(song_name, limit = 1)
    result = videosSearch.result()
    url = result['result'][0]['link']
  except Exception as error:
    if error == "[Errno 11001] getaddrinfo failed":
      return "No internet connection"

    elif error == "list index out of range":
      return f"Song Name invalid!\nNo search results for the song {song_name}"

    else:
      return f"An unknown error occured during searching for the song.\nPlease report the error to the owner.\nError occured: {error}"




  # DOWNLOADING THE SONG.
  try:
    yt = YouTube(url, on_progress_callback=on_progress)
    song = yt.streams.filter(only_audio=True).desc().first()
    song.download()

    try:
      song_name_return = song.default_filename.title()
    except:
      song_name_return = song_name

    return f"{song_name_return} has been successfully downloaded."

  except Exception as error:
    return f"An unknown error occured during downloading the file.\nPlease report about this bug to the owner\nError: {error}"

if __name__ == "__main__":
    pass