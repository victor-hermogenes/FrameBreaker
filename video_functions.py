from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import numpy as np


def start_video(video_file, speed, playing, paused, label):
    try:
        player = MediaPlayer(video_file, ff_otps={'paused': False, 'af': f'atempo={speed}'})
        playing[0] = True
        paused[0] = False
        threading.Thread(target=play_video, args=(player, playing, paused, label)).start()
        return player
    except Exception as e:
        print(f"Error in start_video (video_functions.py): {e}")


def play_video(player, playing, paused, label):
    try:
        while True:
            if not playing[0]:
                break
            elif paused[0]:
                continue

            frame, val = player.get_frame()
            if val == 'eof':
                playing[0] = False
                break
            elif frame is None:
                continue
            img, t = frame
            img_bytes = img.to_bytearray()[0]
            img = np.frombuffer(img_bytes, np.uint8).reshape(img.get_size()[1], img.get_size()[0], 3)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            label.img = img
    except Exception as e:
        print(f"Error in play_video (video_functions.py): {e}")