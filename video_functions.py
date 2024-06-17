from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import tkinter as tk


def start_video(video_file, player, speed, playing, label):
    player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
    playing[0] = True
    threading.Thread(target=play_video, args=(player, playing, label)).start()
    return player


def play_video(player, playing, label):
    while playing[0]:
        frame, val = player.get_frame()
        if val == 'eof':
            break
        if frame is None:
            continue
        img, t = frame
        img = img.to_image()
        img = Image.frombytes('RGB', img.get_size(), img.to_bytearray()[0])
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img


def pause_video(player, playing):
    if player:
        playing[0] = not playing[0]
        player.set_pause(playing[0])


def advance_video(player):
    if player:
        player.seek(10, relative=True)


def goback_video(player):
    if player:
        player.seek(-10, relative=True)