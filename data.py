def create_band_data_structure(file_path):
    """
    Reads a file containing data about the band Pink Floyd and creates a nested dictionary data structure.

    The outer dictionary has album names as keys, and the corresponding values are inner dictionaries.
    The inner dictionaries have song names as keys, and the corresponding values are lists containing the song's length and lyrics.

    :param file_path: Path to the file.
    :type file_path: str
    :return: list inside a Nested dictionary data structure.
    :rtype: dict
    """
    file = open(file_path, "r")
    file_content = file.read()
    file.close()

    data_dict = {}
    file_content = file_content[1:]  # erase the '#' at the beginning
    splitted_albums = file_content.split('#')
    splitted_album_data = []

    for album in splitted_albums:
        data_dict[album.split("::")[0]] = {}  # Key of the outer dict is the album name
        splitted_album_data.append(album.split("*"))

    for album in splitted_album_data:
        for song in album:
            splitted_song_data = song.split("::")
            if len(splitted_song_data) == 2:  # this is the album name and release date
                album_name = splitted_song_data[0]
                continue

            data_dict[album_name][splitted_song_data[0]] = [splitted_song_data[2], splitted_song_data[3]]
            # Key in inner dict is the name of the song
            # Value is a list [length of the song, lyrics]

    return data_dict


def get_all_albums(data_dict):
    """
    function gets the data structure of the band Pink Floyd , the function will return all the albums names
    :param data_dict: Pink Floyd's data
    :type data_dict: dict
    :return: all albums
    :rtype str
    """
    try:
        return ', '.join(data_dict.keys())
    except KeyError as e:
        return "Key error: %s" % e


def get_all_songs_in_album(data_dict, album_name):
    """
     function gets the data structure of the band Pink Floyd and a name of an album
     the function will return all the songs names on the album
    :param data_dict: Pink Floyd's data
    :type data_dict: dict
    :param album_name: name of album of the band
    :type album_name: str
    :return: all songs on the album
    :rtype str
    """
    try:
        return ', '.join(data_dict[album_name].keys())
    except KeyError as e:
        return "Key error: %s" % e


def get_song_length(data_dict, song):
    """
    function gets the data structure of the band Pink Floyd and a name of a song
    the function will return all the length of that song
    :param data_dict: Pink Floyd's data
    :type data_dict: dict
    :param song: song's name
    :type song: str
    :return: length of the song
    :rtype: str
    """
    for album in data_dict.keys():
        if song in data_dict[album].keys():
            return data_dict[album][song][0]
    return "Song Wasn't Found"


def get_song_lyrics(data_dict, song):
    """
    function gets the data structure of the band Pink Floyd and a name of a song
    the function will return all the lyrics of that song
    :param data_dict: Pink Floyd's data
    :type data_dict: dict
    :param song: song's name
    :type song: str
    :return: lyrics of the song
    :rtype: str
    """

    for album in data_dict.keys():
        if song in data_dict[album].keys():
            return data_dict[album][song][1]
    return "Song Wasn't Found"


def get_song_album(data_dict, song):
    """
    function gets the data structure of the band Pink Floyd and a name of a song
    the function will return the name of the album of that song
    :param data_dict: Pink Floyd's data
    :type data_dict: dict
    :param song: song's name
    :type song: str
    :return: song's album name
    :rtype: str
    """
    for album in data_dict.keys():
        if song in data_dict[album].keys():
            return album
    return "Album doesn't exist"


def search_song_by_name(data_dict, data):
    """
    function will search in data dict a song by a part of the name
    :param data_dict: data dict of the band Pink Floyd
    :type data_dict: dict
    :param data: a part of the song's name
    :type data: str
    :return: all matching songs' names
    :rtype: str
    """
    all_songs = []
    for album in data_dict.keys():
        for song in data_dict[album].keys():
            if data.lower() in song.lower():
                all_songs.append(song)
    if len(all_songs) == 0:
        return "Nothing was found"
    return ', '.join(all_songs)


def search_song_by_lyrics(data_dict, lyrics):
    """
    function will search in data dict a song by a part of its lyrics
    :param data_dict: data dict of the band Pink Floyd
    :type data_dict: dict
    :param lyrics: a part of the song's lyrics
    :type lyrics: str
    :return: all matching songs' names
    :rtype: str
    """
    all_songs = []
    for album in data_dict.keys():
        for song in data_dict[album].keys():
            if lyrics.lower() in data_dict[album][song][1].lower():
                all_songs.append(song)
    if len(all_songs) == 0:
        return "Nothing was found"
    return ', '.join(all_songs)


def fifty_most_common(data_dict):
    """
    function will return the fifty most common words in all song of the band
    :param data_dict: data dict of the band Pink Floyd
    :type data_dict: dict
    :return: fifty most common words in a string
    :rtype str
    """
    words = []
    for album in data_dict.keys():
        for song in data_dict[album].keys():
            lyrics_words = data_dict[album][song][1].lower()

            # all these define a begging of a new word
            lyrics_words = lyrics_words.replace(',', '')
            lyrics_words = lyrics_words.replace('.', '')
            lyrics_words = lyrics_words.replace('\n', ' ')
            lyrics_words = lyrics_words.replace("!", '')

            for word in lyrics_words.split():
                words.append(word)

    words_set = set(words)
    most_common = []
    for i in range(50):
        common = max(words_set, key=words.count)  # find the most common word
        most_common.append("%s appears : %d" % (common, words.count(common)))
        words_set.remove(common)  # remove it in order to find the next most common
    return ', '.join(most_common)



