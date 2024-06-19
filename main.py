from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
import video_functions as vf


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("PyQt5 Video Player")
        self.setGeometry(100, 100, 800, 600)


        videoWidget = QVideoWidget()

        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.open_file)

        self.startPauseButton = QPushButton("Start")
        self.startPauseButton.clicked.connect(self.start_pause_video)
        self.startpauseButton.setEnabled(False)


        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.startPauseButton)


        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.mediaPlayer = vf.create_media_player(videoWidget)
        self.is_paused = True


    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                                  "Video files (*.mp4 *.fkv *.ts *.mts *.avi)")
        
        if fileName:
            vf.load_video(self.mediaPlayer, fileName)
            self.startPauseButton.setEnabled(True)


    def start_pause_video(self):
        self.is_paused = vf.toggle_play_pause(self.mediaPlayer, self.is_paused)
        self.startPauseButton.setText("Pause" if not self.is_paused else "Start")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())