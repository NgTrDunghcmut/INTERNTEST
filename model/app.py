import socketio
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QFileDialog,
    QMessageBox,
    QDialog,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QLineEdit,
    QDockWidget,
    QSizePolicy,
    # QListview,
)
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class Communicator(QObject):
    update_text_signal = pyqtSignal(str)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle("TEST")
        self.resize(1600, 900)
        self.appsignal = True
        # central_widget = QWidget(self)
        # self.setCentralWidget(central_widget)
        # define the layouts
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        top_layout = QWidget()
        direction = QHBoxLayout()

        bot_layout = QWidget()
        control = QHBoxLayout()

        # TOP LAYOUT:
        # FIRST COMPONENT:
        self.label2 = QLabel("ADVICE")
        self.label2.setStyleSheet(
            " color: black; border:1px solid black;  font: 'Time News Roman';font-size:18px"
        )
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFixedSize(200, 50)
        # SECOND COMPONENT
        self.showadvice = QVBoxLayout()
        self.showadvice.setSpacing(0)
        # FIRST LAYOUT IN SIDE SECOND COMPONENT
        self.layout2 = QHBoxLayout()
        # SUB-COMPONENT
        self.sign = QGraphicsView()
        self.sign.setFixedSize(200, 50)
        self.textsign = QLabel("Not now")
        self.textsign.setStyleSheet(" border: 1px solid black")
        self.textsign.setFixedSize(200, 50)
        self.sign.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.textsign.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # ADD TO LAYOUT IN SIDE SECOND COMPONENT
        self.layout2.addWidget(self.sign)
        self.layout2.addWidget(self.textsign)
        # SECOND LAYOUT IN SIDE SECOND COMPONENT
        self.history = QLabel("none")
        self.history.setFixedSize(
            self.sign.size().width() + self.textsign.size().width(),
            self.sign.size().height(),
        )
        self.history.setStyleSheet("border:2px solid red")

        self.showadvice.addLayout(self.layout2)
        # Adjust spacing between widgets in layout2
        self.showadvice.addWidget(self.history)

        # ADJUST DIRECTION
        direction.addWidget(self.label2)
        direction.addLayout(self.showadvice)

        top_layout.setLayout(direction)
        main_layout.addWidget(top_layout)

        self.graphic = QVideoWidget()
        self.media = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media.setVideoOutput(self.graphic)
        self.label = QLabel("THIS IS A DEMO")
        self.button = QPushButton("Start")
        self.button.setStyleSheet(
            "QPushButton:hover { background-color: #4CAF50; color: white; border: none; padding: 15px 32px; text-align: center; text-decoration: none; font-size: 16px; }"
        )
        # self.button.resize(100, 50)
        self.button.clicked.connect(self.whne_click)
        self.button.setFixedSize(200, 50)
        # main_layout.addWidget(self.label)

        control.addWidget(self.label)
        control.addWidget(self.button)

        bot_layout.setLayout(control)
        main_layout.addWidget(self.graphic)
        main_layout.addWidget(bot_layout)
        # main_layout.addWidget(self.button)

    def whne_click(self):
        self.appsignal = not self.appsignal
        self.button.setText("Start" if self.appsignal else "Stop")
        self.path = "./output_video.mp4"
        self.media.setMedia(QMediaContent(QUrl.fromLocalFile(self.path)))
        # size = self.media.metaData(QMediaPlayer.)
        # print(size)
        # self.graphic.resize(size.width(), size.height())
        if self.appsignal:
            self.media.play()
        else:
            self.media.stop()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    Root = App()
    Root.show()

    sys.exit(application.exec())
