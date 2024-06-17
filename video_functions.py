from ffpyplayer.player import MediaPlayer
import threading


def start_video(video_file, player, speed, playing):
    player= MediaPlayer(video_file, ff_opts={'paused': False})
    playing[0]
    threading.Thread(target=play_video, args=(player, speed, playing)).start()
    return player


def play_video(player, speed, playing):
    while playing[0]:
        frame, val = player.get_frame()
        if val == 'eof':
            break
        if frame is None:
            continue
        img, t = frame
        img = img.to_image()
        img.show()


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

    
def set_speed(player, speed):
    if player:
        player.set_speed(speed)