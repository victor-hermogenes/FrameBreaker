from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QSizePolicy, QSlider, QSpacerItem, QMessageBox, QStyleOptionSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QLinearGradient, QBrush
from PyQt5.Qt import QStyle
import sys
import os
import video_functions as vf


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title and layout
        self.setWindowTitle("Video Frame Breaker")
        self.setGeometry(100, 100, 800, 600)

        # Center background
        self.videoWidget = QVideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoWidget.setStyleSheet("background-color: black;")

        # Slider Style:
        slider_style = """
            QSlider::groove:horizontal {
                background: gray;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: none;
                width: 15px;
                height: 15px;
                border-radius: 7.5px;
                margin: -5px 0;
            }
            QSlider::sub-page:horizontal {
                background: #5c5c5c;
            }
            QSlider::add-page:horizontal {
                background: lightgray;
            }
        """

        # Using ShinyButton instead of QPushButton
        self.openButton = ShinyButton("Open Video File", self)
        self.startPauseButton = ShinyButton("Play/Pause", self)
        self.fullscreenButton = ShinyButton("Toggle Fullscreen", self)
        self.advanceButton = ShinyButton("Skip Forward", self)
        self.rewindButton = ShinyButton("Skip Backward", self)
        self.extractFramesButton = ShinyButton("Extract Frames", self)

        # Set icons for buttons
        self.openButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.startPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.advanceButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.rewindButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.extractFramesButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))

        # Connect buttons to thei respective slots
        self.openButton.clicked.connect(self.open_file)
        self.startPauseButton.clicked.connect(self.start_pause_video)
        self.fullscreenButton.clicked.connect(self.toggle_fullscreen)
        self.advanceButton.clicked.connect(self.advance_video)
        self.rewindButton.clicked.connect(self.rewind_video)
        self.extractFramesButton.clicked.connect(self.extract_frames)
        
        # Volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.setFixedSize(100, 30)
        self.volumeSlider.valueChanged.connect(self.change_volume)
        self.volumeSlider.setStyleSheet(slider_style)

        # Video Position slider
        self.videoSlider = ClickableSlider(Qt.Horizontal)
        self.videoSlider.setRange(0, 100)
        self.videoSlider.setToolTip("Seek Video")
        self.videoSlider.sliderMoved.connect(self.seek_video)
        self.videoSlider.setStyleSheet(slider_style)

        # Layout for the function buttons
        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.addWidget(self.openButton)
        self.controlsLayout.addWidget(self.rewindButton)
        self.controlsLayout.addWidget(self.startPauseButton)
        self.controlsLayout.addWidget(self.advanceButton)
        self.controlsLayout.addWidget(self.fullscreenButton)
        self.controlsLayout.addWidget(self.volumeSlider)
        self.controlsLayout.addWidget(self.extractFramesButton)

        # Spacer to centralize the video slider
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.controlsLayout.insertItem(0, spacer)
        self.controlsLayout.insertItem(6, spacer)

        # Widget for the controls
        self.controls = QWidget(self)
        self.controls.setLayout(self.controlsLayout)
        self.controls.setFixedHeight(50)  # Adjust height as needed

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.videoWidget)
        mainLayout.addWidget(self.videoSlider)
        mainLayout.addWidget(self.controls)

        # Central widget
        centralWidget = QWidget(self)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Media player
        self.mediaPlayer = vf.create_media_player(self.videoWidget)
        self.is_paused = True
        self.is_fullscreen = False

        # Timer to make buttons layout vanish from fullscreen
        self.mouse_timer = QTimer(self)
        self.mouse_timer.setInterval(2000)  # Adjust this interval as needed
        self.mouse_timer.timeout.connect(self.hide_controls)

        # Timer to update the video slider position
        self.position_timer = QTimer(self)
        self.position_timer.setInterval(1000)  # Update every second
        self.position_timer.timeout.connect(lambda: self.update_slider(self.mediaPlayer.position()))
        self.position_timer.start()

        # Track mouse to show buttons layout again
        self.setMouseTracking(True)
        self.videoWidget.setMouseTracking(True)
        self.controls.setMouseTracking(True)
        centralWidget.setMouseTracking(True)

        self.video_path = ""


    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                                  "Video files (*.mp4 *.fkv *.ts *.mts *.avi)")
        
        if fileName:
            self.video_path = fileName
            vf.load_video(self.mediaPlayer, fileName)
            self.startPauseButton.setEnabled(True)
            self.mediaPlayer.durationChanged.connect(self.update_duration)
            self.mediaPlayer.positionChanged.connect(self.update_slider)


    def start_pause_video(self):
        self.is_paused = vf.toggle_play_pause(self.mediaPlayer, self.is_paused)
        self.startPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause if not self.is_paused else QStyle.SP_MediaPlay))


    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.setStyleSheet("")
            self.show()
            self.videoSlider.show()
            self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
            self.mouse_timer.stop()
            self.controls.show()
        else:
            self.showFullScreen()
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setStyleSheet("background-color: black;")
            self.show()
            self.videoSlider.hide()
            self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
            self.mouse_timer.start()

        self.is_fullscreen = not self.is_fullscreen


    def hide_controls(self):
        if self.is_fullscreen:
            self.controls.hide()
            self.videoSlider.hide()


    def mouseMoveEvent(self, event):
        if self.is_fullscreen:
            self.controls.show()
            self.videoSlider.show()
            self.mouse_timer.start()
        super().mouseMoveEvent(event)

    
    def change_volume(self, value):
        vf.set_volume(self.mediaPlayer, value)

    
    def advance_video(self):
        vf.advance(self.mediaPlayer, 10)

    
    def rewind_video(self):
        vf.rewind(self.mediaPlayer, 10)


    def seek_video(self, position):
        self.mediaPlayer.setPosition(position * 1000)


    def update_slider(self, position):
        if not self.videoSlider.isSliderDown():
            self.videoSlider.setValue(int(position / 1000))
    
    def update_duration(self, duration):
        self.videoSlider.setRange(0, int(duration / 1000))


    def extract_frames(self):
        if not self.video_path:
            QMessageBox.warning(self, "No Video Loaded", f"Please load a video file first.")
            return
        
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            frame_count, frame_rate = vf.extract_frames(self.video_path, output_folder)
            QMessageBox.information(self, "Extraction Complete", f"Extracted {frame_count} frames at {frame_rate} FPS to {output_folder}")


class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
            self.setValue(value)
            self.sliderMoved.emit(value)
        super().mousePressEvent(event)


class ShinyButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # create gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 209, 209))
        gradient.setColorAt(0.5, QColor(0, 180, 180))
        gradient.setColorAt(1, QColor(0, 150, 150))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        # Draw rounded rect with gradient
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 10, 10)

        # Draw the button text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

        # Draw the icon
        icon = self.icon()
        if not icon.isNull():
            icon_size = self.iconSize()
            pixmap = icon.pixmap(icon_size)
            icon_rect = QRect((self.width() - icon_size.width()) // 2, 10, icon_size.width(), icon_size.height())
            painter.drawPixmap(icon_rect, pixmap)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
