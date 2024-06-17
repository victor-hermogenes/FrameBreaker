from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import numpy as np


def start_video(video_file, player, speed, playing, label):
    player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
    playing[0] = True
    threading.Thread(target=play_video, args=(player, playing, label)).start()
    return player


def play_video(player, playing, label):
    while playing[0]:
        frame, val = player.get_frame()
        if val == 'eof':
            playing[0] = False
            break
        if frame is None:
            continue
        img, t = frame
        img_bytes = img.to_bytearray()[0]
        img = np.frombuffer(img_bytes, np.uint8).reshape(img.get_size()[1], img.get_size()[0], 3)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img
        if player.get_pause():
            while player.get_pause():
                if not playing[0]:
                    break
                continue


def pause_video(player, playing):
    if player:
        if player.get_pause():
            player.set_pause(False)
            playing[0] = True
        else:
            player.set_pause(True)
            playing[0] = False


def advance_video(player):
    if player:
        player.seek(10, relative=True)


def goback_video(player):
    if player:
        player.seek(-10, relative=True)