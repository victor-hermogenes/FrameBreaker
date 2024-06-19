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