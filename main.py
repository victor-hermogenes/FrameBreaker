import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player")


        self.video_file = filedialog.askopenfilename(title="Select a video file")
        if not self.video_file:
            messagebox.showerror("Error", "No video file selected. Exiting.")
            master.quit()
            return
        
        
        self.frame = tk.Frame(master)
        self.frame.pack()


        self.video_label = tk.Label(master)
        self.video_label.pack()


        self.control_frame = tk.Frame(master)
        self.control_frame.pack()


        self.icon_size = (30, 30)
        self.start_icon = ImageTk.PhotoImage(Image.open("icons/play_replay.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.pause_icon = ImageTk.PhotoImage(Image.open("icons/pause.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.resume_icon = ImageTk.PhotoImage(Image.open("icons/start.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.advance_icon = ImageTk.PhotoImage(Image.open("icons/Forward.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.goback_icon = ImageTk.PhotoImage(Image.open("icons/Back.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.speed_icon = ImageTk.PhotoImage(Image.open("icons/speed_rate.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.break_icon = ImageTk.PhotoImage(Image.open("icons/corte.ico").resize(self.icon_size, Image.Resampling.LANCZOS))
        self.close_icon = ImageTk.PhotoImage(Image.open("icons/sair.ico").resize(self.icon_size, Image.Resampling.LANCZOS))


        self.start_button = tk.Button(self.control_frame, image=self.start_icon, command=self.start_video)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.control_frame, image=self.pause_icon, command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT)


        self.advance_button = tk.Button(self.control_frame, image=self.advance_icon, command=self.advance_video)
        self.advance_button.pack(side=tk.LEFT)


        self.goback_button = tk.Button(self.control_frame, image=self.goback_icon, command=self.goback_video)
        self.goback_button.pack(side=tk.LEFT)

        self.speed_button = tk.Button(self.control_frame, image=self.speed_icon, command=self.set_speed)
        self.speed_button.pack(side=tk.LEFT)


        self.break_button = tk.Button(self.control_frame, image=self.break_icon, command=self.break_frame)
        self.break_button.pack(side=tk.LEFT)


        self.close_button = tk.Button(self.control_frame, image=self.break_icon, command=self.on_closing)
        self.close_button.pack(side=tk.LEFT)


        self.player = None
        self.playing = [False]
        self.speed = 1.0


    def start_video(self):
        print("Start Video")


    def toggle_pause(self):
        if self.playing[0]:
            self.pause_video()
        else:
            self.resume_video()


    def pause_video(self):
        self.playing[0] = False
        self.pause_button.config(image=self.pause_icon)
        print("Pause video")


    def resume_video(self):
        self.playing[0] = True
        self.pause_button.config(image=self.resume_icon)
        print("Resume video")


    def advance_video(self):
        print("Advance 10 sec")


    def goback_video(self):
        print("Go back 10 sec")


    def set_speed(self):
        print("Set speed")


    def break_frame(self):
        print("Break frame")

    
    def on_closing(self):
        print("Close player")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
