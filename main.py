from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QSizePolicy
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QTimer, Qt
import sys
import video_functions as vf


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Frame Breaker")
        self.setGeometry(100, 100, 800, 600)

        self.videoWidget = QVideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoWidget.setStyleSheet("background-color: black;")  # Ensure background is black

        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.open_file)
        self.openButton.setStyleSheet("background-color: white")

        self.startPauseButton = QPushButton("Start")
        self.startPauseButton.clicked.connect(self.start_pause_video)
        self.startPauseButton.setEnabled(False)
        self.startPauseButton.setStyleSheet("background-color: white")

        self.fullscreenButton = QPushButton("Full Screen")
        self.fullscreenButton.clicked.connect(self.toggle_fullscreen)
        self.fullscreenButton.setStyleSheet("background-color: white")

        # Layout for the buttons
        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.addWidget(self.openButton)
        self.controlsLayout.addWidget(self.startPauseButton)
        self.controlsLayout.addWidget(self.fullscreenButton)

        # Widget for the controls
        self.controls = QWidget(self)
        self.controls.setLayout(self.controlsLayout)
        self.controls.setFixedHeight(50)  # Adjust height as needed

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.videoWidget)
        mainLayout.addWidget(self.controls)

        # Central widget
        centralWidget = QWidget(self)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.mediaPlayer = vf.create_media_player(self.videoWidget)
        self.is_paused = True
        self.is_fullscreen = False

        self.mouse_timer = QTimer(self)
        self.mouse_timer.setInterval(2000)  # Adjust this interval as needed
        self.mouse_timer.timeout.connect(self.hide_controls)

        self.setMouseTracking(True)
        self.videoWidget.setMouseTracking(True)
        self.controls.setMouseTracking(True)
        centralWidget.setMouseTracking(True)


    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                                  "Video files (*.mp4 *.fkv *.ts *.mts *.avi)")
        
        if fileName:
            vf.load_video(self.mediaPlayer, fileName)
            self.startPauseButton.setEnabled(True)


    def start_pause_video(self):
        self.is_paused = vf.toggle_play_pause(self.mediaPlayer, self.is_paused)
        self.startPauseButton.setText("Pause" if not self.is_paused else "Start")


    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.setStyleSheet("")
            self.show()
            self.fullscreenButton.setText("Full Screen")
            self.mouse_timer.stop()
            self.controls.show()
        else:
            self.showFullScreen()
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setStyleSheet("background-color: black;")
            self.show()
            self.fullscreenButton.setText("Exit Full Screen")
            self.mouse_timer.start()

        self.is_fullscreen = not self.is_fullscreen


    def hide_controls(self):
        if self.is_fullscreen:
            self.controls.hide()


    def mouseMoveEvent(self, event):
        if self.is_fullscreen:
            self.controls.show()
            self.mouse_timer.start()
        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())