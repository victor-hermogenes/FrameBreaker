import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from ffpyplayer.player import MediaPlayer
import threading

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player")

        # Prompt to select video file
        self.video_file = filedialog.askopenfilename(title="Select a video file")
        if not self.video_file:
            messagebox.showerror("Error", "No video file selected. Exiting.")
            master.quit()
            return

        # Buttons for video control
        self.start_button = tk.Button(master, text="Start", command=self.start_video)
        self.start_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_video)
        self.pause_button.pack()

        self.advance_button = tk.Button(master, text="Advance", command=self.advance_video)
        self.advance_button.pack()

        self.goback_button = tk.Button(master, text="Go Back", command=self.goback_video)
        self.goback_button.pack()

        self.speed_button = tk.Button(master, text="Speed", command=self.set_speed)
        self.speed_button.pack()

        self.break_button = tk.Button(master, text="Break", command=self.break_video)
        self.break_button.pack()

        self.player = None
        self.playing = False
        self.speed = 1.0

    def start_video(self):
        self.playing = True
        self.player = MediaPlayer(self.video_file, ff_opts={'paused': False})
        threading.Thread(target=self.play_video).start()

    def play_video(self):
        while self.playing:
            frame, val = self.player.get_frame()
            if val == 'eof':
                break
            if frame is None:
                continue
            img, t = frame
            img = img.to_image()
            img.show()
    
    def pause_video(self):
        if self.player:
            self.playing = not self.playing
            self.player.set_pause(self.playing)

    def advance_video(self):
        if self.player:
            self.player.seek(10, relative=True)

    def goback_video(self):
        if self.player:
            self.player.seek(-10, relative=True)

    def set_speed(self):
        speed = simpledialog.askfloat("Input", "Enter speed rate (e.g., 0.5 for half speed, 2 for double speed):")
        if speed and speed > 0:
            self.speed = speed
            self.player.set_speed(self.speed)

    def break_video(self):
        # Placeholder for the break video functionality
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
