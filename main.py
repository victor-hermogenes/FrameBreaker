from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QSizePolicy, QSlider, QSpacerItem, QMessageBox, QShortcut, QLabel
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QTimer, Qt, QRect, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QLinearGradient, QBrush, QKeySequence, QMouseEvent
from PyQt5.Qt import QStyle
import sys
import os
from ctypes import windll
import video_functions as vf


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setFixedHeight(30)
        self.parent = parent  # Keep a reference to the parent

        # Create layout and buttons in headers
        self.layout = QHBoxLayout()
        self.title = QLabel("Video Frame Breaker")
        self.title.setStyleSheet("background-color: transparent; color: white; margin-left: 10px;")
        self.layout.addWidget(self.title)

        # Add stretch to push buttons to the right
        self.layout.addStretch()

        # Standard window buttons using QStyle
        self.minimizeButton = QPushButton()
        self.minimizeButton.setFixedSize(20, 20)
        self.minimizeButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton))
        self.minimizeButton.setStyleSheet(self.get_button_style("inactive"))
        self.minimizeButton.clicked.connect(parent.showMinimized)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(20, 20)
        self.maximizeButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.maximizeButton.setStyleSheet(self.get_button_style("inactive"))
        self.maximizeButton.clicked.connect(parent.toggle_maximize)

        self.closeButton = QPushButton()
        self.closeButton.setFixedSize(20, 20)
        self.closeButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.closeButton.setStyleSheet(self.get_button_style("close"))
        self.closeButton.clicked.connect(parent.close)

        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.maximizeButton)
        self.layout.addWidget(self.closeButton)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def get_button_style(self, button_type):
        if button_type == "inactive":
            return """
                QPushButton {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 black, stop:0.7 gray);
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 gray, stop:0.3 white);
                }
                """
        elif button_type == "close":
            return """
                QPushButton {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 red, stop:0.7 darkred);
                    color:white;
                    border: none
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 darkred, stop:0.3 red);
                }
            """

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.start_moving(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move_window(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.stop_moving(event)


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove native title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Title and layout
        self.setWindowTitle("Video Frame Breaker")
        self.setGeometry(100, 100, 800, 600)

        # Custom title bar
        self.titleBar = CustomTitleBar(self)
        self.titleBar.setStyleSheet("background-color: black;")

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
        self.openButton = ShinyButton("", self)
        self.startPauseButton = ShinyButton("", self)
        self.fullscreenButton = ShinyButton("", self)
        self.advanceButton = ShinyButton("", self)
        self.rewindButton = ShinyButton("", self)
        self.extractFramesButton = ShinyButton("", self)

        # Set icons for buttons
        self.openButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.startPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.advanceButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.rewindButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.extractFramesButton.setIcon(self.style().standardIcon(QStyle.SP_DriveCDIcon))

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
        mainLayout.addWidget(self.titleBar)
        mainLayout.addWidget(self.videoWidget)
        mainLayout.addWidget(self.videoSlider)
        mainLayout.addWidget(self.controls)

        # Central widget
        centralWidget = GradientWidget(self)
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

        # Set keyboard shortcuts
        self.set_shortcuts()

        # For dragging
        self.moving = self
        self.offset = QPoint()


    def start_moving(self, event):
        self.moving = True
        self.offset = event.pos()
    

    def move_window(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)


    def stop_moving(self, event):
        self.moving = False


    # Implement toggle_maximize
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


    # Set keyboard shortcuts
    def set_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.exit_fullscreen)
        QShortcut(QKeySequence(Qt.Key_F11), self, self.toggle_fullscreen)
        QShortcut(QKeySequence(Qt.Key_Space), self, self.start_pause_video)
        QShortcut(QKeySequence(Qt.Key_M), self, self.toggle_mute)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.advance_video)
        QShortcut(QKeySequence(Qt.Key_Left), self, self.rewind_video)

    
    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    
    def toggle_mute(self):
        current_volume = self.mediaPlayer.volume()
        if current_volume > 0:
            self.previous_volume = current_volume
            self.mediaPlayer.setVolume(0)
        else:
            self.mediaPlayer.setVolume(self.previous_volume)


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
            self.titleBar.hide()


    def mouseMoveEvent(self, event):
        if self.is_fullscreen:
            self.controls.show()
            self.videoSlider.show()
            self.titleBar.show()
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


class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

    
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(64, 64, 64))
        gradient.setColorAt(1, QColor(0, 0, 0))
        painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)

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

            # Apply gradient black to the pixmap
            gradient = QLinearGradient(0, 0, 0, pixmap.height())
            gradient.setColorAt(0, QColor(0, 0, 0))
            gradient.setColorAt(1, QColor(64, 64, 64))
            brush = QBrush(gradient)

            icon_pixmap = QPixmap(pixmap.size())
            icon_pixmap.fill(Qt.transparent)
            icon_painter = QPainter(icon_pixmap)
            icon_painter.setCompositionMode(QPainter.CompositionMode_Source)
            icon_painter.drawPixmap(0, 0, pixmap)
            icon_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon_painter.fillRect(icon_pixmap.rect(), brush)
            icon_painter.end()

            icon_rect = QRect((self.width() - icon_size.width()) // 2, 10, icon_size.width(), icon_size.height())
            painter.drawPixmap(icon_rect, icon_pixmap)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
