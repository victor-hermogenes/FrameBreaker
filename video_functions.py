from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import numpy as np

def start_video(video_file, speed, playing, label):
    try:
        player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
        playing[0] = True
        threading.Thread(target=play_video, args=(player, playing, label)).start()
        return player
    except Exception as e:
        print(f"Error in start_video: {e}")

def play_video(player, playing, label):
    try:
        while True:
            if not playing[0]:
                break
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
    except Exception as e:
        print(f"Error in play_video: {e}")

def pause_video(player, playing):
    try:
        if player:
            playing[0] = not playing[0]
            player.set_pause(not playing[0])
    except Exception as e:
        print(f"Error in pause_video: {e}")

def advance_video(player):
    try:
        if player:
            player.seek(10, relative=True)
    except Exception as e:
        print(f"Error in advance_video: {e}")

def goback_video(player):
    try:
        if player:
            player.seek(-10, relative=True)
    except Exception as e:
        print(f"Error in goback_video: {e}")

def change_speed(video_file, player, speed, playing, label):
    try:
        current_pos = player.get_pts()
        player.set_pause(True)
        playing[0] = False
        player.close_player()
        import time
        time.sleep(1)
        new_player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
        new_player.seek(current_pos, relative=False)
        playing[0] = True
        threading.Thread(target=play_video, args=(new_player, playing, label)).start()
        return new_player
    except Exception as e:
        print(f"Error in change_speed: {e}")

