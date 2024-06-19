import cv2
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


def advance(mediaPlayer, seconds):
    """Advance the video by a specified number of seconds."""
    if mediaPlayer.state() == QMediaPlayer.PlayingState or mediaPlayer.state() == QMediaPlayer.PausedState:
        new_position = mediaPlayer.position() + (seconds * 1000)
        mediaPlayer.setPosition(new_position)

    
def rewind(mediaPlayer, seconds):
    """Rewind the video by a specified number of seconds."""
    if mediaPlayer.state() == QMediaPlayer.PlayingState or mediaPlayer.state() == QMediaPlayer.PausedState:
        new_position = mediaPlayer.position() - (seconds * 1000)
        mediaPlayer.setPosition(new_position)


def extract_frames(video_path, output_folder):
    """Extract frames from a video and save them as images in the output folder"""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = f"{output_folder}/frame_{count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    return frame_count, frame_rate