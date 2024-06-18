from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import numpy as np
import time

def start_video(video_file, player, speed, playing, label, speed_control):
    try:
        player = MediaPlayer(video_file, ff_opts={'paused': False})
        playing[0] = True
        threading.Thread(target=play_video, args=(player, playing, label, speed_control)).start()
        return player
    except Exception as e:
        print(f"Error in start_video: {e}")

def play_video(player, playing, label, speed_control):
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

            # Control playback speed
            time.sleep(speed_control[0])
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
        # Save the current position
        current_pos = player.get_pts()
        
        # Pause the current player
        player.set_pause(True)
        
        # Close the current player after ensuring the playing flag is set to False
        playing[0] = False
        player.close_player()
        
        # Wait for a moment to ensure the old player and thread are properly closed
        time.sleep(1)
        
        # Create a new player with the updated speed
        new_player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
        
        # Seek to the saved position in the new player
        new_player.seek(current_pos, relative=False)
        
        # Update the player reference and set playing to True
        player = new_player
        playing[0] = True
        
        # Start a new thread to play the video
        threading.Thread(target=play_video, args=(new_player, playing, label)).start()
        
    except Exception as e:
        print(f"Error in change_speed: {e}")
