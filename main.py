from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
import sys


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("PyQt5 Video Player")
        self.setGeometry(100, 100, 800, 600)


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        videoWidget = QVideoWidget()


        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.open_file)


        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play_video)
        self.playButton.setEnabled(False)


        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.playButton)


        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.mediaPlayer.setVideoOutput(videoWidget)


    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                                  "Video files (*.mp4 *.fkv *.ts *.mts *.avi)")
        
        if fileName:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)


    def play_video(self):
        self.mediaPlayer.play()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())