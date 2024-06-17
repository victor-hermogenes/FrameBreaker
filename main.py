import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from video_functions import start_video, pause_video, advance_video, goback_video


class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player")


        # Prompt to select video file
        self.video_file = filedialog.askopenfilename(title="Select a video file")
        if not self.video_file:
            messagebox.showerror("Error", "No video file select. Exiting.")
            master.quit()
            return
        
        # Label to display video frames
        self.video_label = tk.Label(master)
        self.video_label.pack()


        # Buttons for video control
        self.start_button = tk.Button(master, text="Start", command=self.start_video)
        self.start_button.pack()


        self.pause_button = tk.Button(master, text="Pause", command=self.pause_video)
        self.pause_button.pack()


        self.advance_button = tk.Button(master , text="Advance", command=self.advance_video)
        self.advance_button.pack()


        self.goback_button = tk.Button(master, text="Go Back", command=self.goback_video)
        self.goback_button.pack()


        self.speed_button = tk.Button(master, text="Speed", command=self.set_speed)
        self.speed_button.pack()


        self.break_button = tk.Button(master, text="Break", command=self.break_video)
        self.break_button.pack()


        self.player = None
        self.playing = [False]
        self.speed = 1.0


    def start_video(self):
        try:
            if self.player:
                self.player.close_player()
            self.player = start_video(self.video_file, self.player, self.speed, self.playing, self.video_label)
        except Exception as e:
            print(f"Error: {e}")


    def pause_video(self):
        try:
            pause_video(self.player, self.playing)
            if self.playing[0]:
                self.pause_button.config(text="Pause")
            else:
                self.pause_button.config(text="Return")
        except Exception as e:
            print(f"Error: {e}")

    def advance_video(self):
        try:
            advance_video(self.player)
        except Exception as e:
            print(f"Error: {e}")

        
    def goback_video(self):
        try:
            goback_video(self.player)
        except Exception as e:
            print(f"Error: {e}")

    
    def set_speed(self):
        speed = simpledialog.askfloat("Input", "Entre speed rate (e.g., 0.5 for half speed, 2 for double speed):")
        if speed and speed > 0:
            self.speed = speed
            self.start_video()


    def break_video(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()

