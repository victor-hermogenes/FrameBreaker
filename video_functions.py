from ffpyplayer.player import MediaPlayer
import threading
from PIL import Image, ImageTk
import numpy as np


def start_video(video_file, speed, playing, paused, label):
    try:
        print("Starting video...")
        player = MediaPlayer(video_file, ff_opts={'paused': False, 'af': f'atempo={speed}'})
        playing[0] = True
        paused[0] = False
        thread = threading.Thread(target=play_video, args=(player, playing, paused, label), daemon=True)
        thread.start()
        print("Video started successfully.")
        return player
    except Exception as e:
        print(f"Error in start_video (video_functions.py): {e}")


def play_video(player, playing, paused, label):
    try:
        print("Entered play_video function.")
        while True:
            if not playing[0]:
                print("Stopping video playback due to playing[0] being False.")
                break
            elif paused[0]:
                player.set_pause(True)
                print("Video playback paused.")
                continue
            else:
                player.set_pause(False)
                print("Video playback resumed.")

            frame, val = player.get_frame()
            if val == 'eof':
                print("End of video file reached.")
                playing[0] = False
                break
            elif frame is None:
                continue

            img, t = frame
            if img:
                try:
                    img_bytes = img.to_bytearray()[0]
                    img_np = np.frombuffer(img_bytes, np.uint8).reshape(img.get_size()[1], img.get_size()[0], 3)
                    img_pil = Image.fromarray(img_np)
                    img_tk = ImageTk.PhotoImage(img_pil)
                    label.config(image=img_tk)
                    label.image = img_tk
                    print("Frame updated on label.")
                except Exception as e:
                    print(f"Error processing frame: {e}")
    except Exception as e:
        print(f"Error in play_video (video_functions.py): {e}")


def pause_video(player, paused):
    try:
        print("Pausing video...")
        paused[0] = True
        player.set_pause(True)
        print("Video paused.")
    except Exception as e:
        print(f"Error in pause_video (video_functions.py): {e}")


def resume_video(player, paused):
    try:
        print("Resuming video...")
        paused[0] = False
        player.set_pause(False)
        print("Video resumed.")
    except Exception as e:
        print(f"Error in resume_video (video_function.py): {e}")