from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


def create_media_player(videoWidget):

    mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    mediaPlayer.setVideoOutput(videoWidget)
    return mediaPlayer


def load_video(mediaPlayer, fileName):
    mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))


def toggle_play_pause(mediaPlayer, is_paused):
    if is_paused:
        mediaPlayer.play()
        return False
    else:
        mediaPlayer.pause()
        return True


def set_volume(mediaPlayer, volume):
    """
    Sets the volume of the media player.
    :param mediaPlayer: The QMediaPlayer instance.
    :param volume: Volume level (0 to 100).
    """
    mediaPlayer.setVolume(volume)


def get_volume(mediaPlayer):
    """
    Gets the current volume of the media player.
    :param mediaPlayer: the QMediaPlayer instance.
    :return: Current volume level (0 to 100)
    """
    return mediaPlayer.volume()