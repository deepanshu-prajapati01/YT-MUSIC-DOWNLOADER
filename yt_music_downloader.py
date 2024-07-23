# THIS CODE CAN RETRIEVE SONG URL FROM ITS NAME
import os, re
from youtubesearchpython import VideosSearch
from pytube import YouTube
from pytube.cli import on_progress

owner_folder = "Songs-Deepanshu-Prajapati01"
path_to_save_files = f"{os.path.expanduser('~')}\\Music\\{owner_folder}"


# code from github to fix error 400 bad request and get_throttling_function_name: could not find match for multiple"
from pytube.innertube import _default_clients
from pytube import cipher
import re

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]



def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name





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
    videosSearch = VideosSearch(song_name, limit = 5)
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
    if song == None:
      return f"Failed to download the song -> {song_name}"
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
