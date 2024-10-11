# import socketio
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl, QThread
import asyncio
import socketio
import cv2
import base64
import cv2
from modelfile.detect import run
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGraphicsView,
    QSizePolicy,
    QMessageBox,
    QFileDialog,
    QGraphicsScene,
)
from PyQt5.QtGui import QPixmap, QImageReader, QImage
from PyQt5.QtMultimediaWidgets import QVideoWidget
import numpy as np

uri = "http://127.0.0.1:5000/"

sio = socketio.Client()


@sio.event
def connect():
    print("Đã kết nối với server")


# Xử lý sự kiện khi ngắt kết nối
@sio.event
def disconnect():
    print("Đã ngắt kết nối với server")


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    ButtonUpdate = pyqtSignal()

    def handle_frame(self, data):
        # Convert the received byte data to an image
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is not None:
            # Convert the frame to RGB
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the image to QImage format
            converted_img = QImage(
                Image.data,
                Image.shape[1],
                Image.shape[0],
                Image.strides[0],
                QImage.Format_RGB888,
            )
            # Resize the image to fit the UI
            Pic = converted_img.scaled(640, 480, Qt.KeepAspectRatio)
            # Emit the image to update the GUI
            self.ImageUpdate.emit(Pic)

        self.stop()

    def run(self):
        try:
            self.ThreadActive = True
            sio.on(
                "frame_transmit", self.handle_frame
            )  # Listen to the 'frame' event from the server
            print("start listening")  # Keep listening for incoming frames
            sio.wait()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def stop(self):
        self.ThreadActive = False
        # sio.off("frame_transmit")
        sio.shutdown()
        self.quit()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.worker = Worker1()
        self.setWindowTitle("TEST")
        self.resize(1600, 900)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF")
        # self.appsignal = True
        # central_widget = QWidget(self)
        # self.setCentralWidget(central_widget)
        # define the layouts
        main = QWidget()
        main_layout = QVBoxLayout()
        main.setLayout(main_layout)
        # top_layout = QWidget()
        direction = QHBoxLayout()
        direction.setSpacing(0)

        # bot_layout = QWidget()
        control = QHBoxLayout()

        # TOP LAYOUT:
        # FIRST COMPONENT:
        self.label2 = QLabel("ADVICE")
        self.label2.setStyleSheet(
            " color: red; border:1px solid white;  font: 'Time News Roman';font-size:18px"
        )
        self.label2.setAlignment(Qt.AlignCenter)
        # self.label2.setFixedSize(200, 50)
        # SECOND COMPONENT
        self.showadvice = QVBoxLayout()
        self.showadvice.setSpacing(5)
        # FIRST LAYOUT IN SIDE SECOND COMPONENT
        self.layout2 = QHBoxLayout()
        self.layout2.setSpacing(2)
        # self.layout2.SetFixedSize(QSize(400, 50))
        # SUB-COMPONENT
        self.sign = QGraphicsView()
        self.sign.setFixedHeight(100)
        self.textsign = QLabel("Not now")
        self.textsign.setStyleSheet(" border: 1px solid yellow")
        self.sign.setStyleSheet(" border: 1px solid yellow")
        self.textsign.setFixedHeight(100)
        self.textsign.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sign.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # ADD TO LAYOUT IN SIDE SECOND COMPONENT
        self.layout2.addWidget(self.sign)
        self.layout2.addWidget(self.textsign)
        self.layout2.setStretch(0, 1)
        self.layout2.setStretch(1, 3)
        # SECOND LAYOUT IN SIDE SECOND COMPONENT
        self.history_direction = []
        self.history = QLabel("none")
        self.history.setFixedHeight(self.sign.size().height())
        self.history.setStyleSheet("border:2px solid red")
        # self.showpopup()
        self.showadvice.addLayout(self.layout2)
        # Adjust spacing between widgets in layout2
        self.showadvice.addWidget(self.history)

        # ADJUST DIRECTION
        direction.addWidget(self.label2)
        direction.addLayout(self.showadvice)
        direction.setStretch(0, 1)
        direction.setStretch(1, 3)

        self.graphic = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphic.setScene(self.scene)
        self.graphic.setStyleSheet("border: 2px solid green; background-color: gray")
        self.label = QLabel("THIS IS A DEMO")
        self.button = QPushButton("Connect")
        self.button.setStyleSheet(
            "QPushButton:hover { background-color: #4CAF50; color: white; border: none; padding: 15px 32px; text-align: center; text-decoration: none; font-size: 16px; }"
        )
        # self.button.resize(100, 50)
        self.button.clicked.connect(self.when_click)
        # self.button.setFixedSize(200, 50)

        control.addWidget(self.label)
        control.addWidget(self.button)

        main_layout.addLayout(direction)
        main_layout.addWidget(self.graphic)
        main_layout.addLayout(control)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 3)
        main_layout.setStretch(2, 1)
        self.setCentralWidget(main)
        # main_layout.addWidget(self.button)
        self.worker.ImageUpdate.connect(self.update_image)
        self.worker.ButtonUpdate.connect(self.enable_button)

    def get_local_file_path(self):
        # Create a QWidget instance (necessary for QFileDialog)
        widget = QWidget()
        widget.setWindowTitle("Select File")

        # Open a file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(
            widget, "Open File", "", "All Files (*)"
        )

        # Check if a file path was selected
        if file_path:
            print(f"Selected file path: {file_path}")
            return str(file_path)
        else:
            print("No file selected")
            return None

    def showpopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("OPTION")
        msg.setText("DO YOU WANT TO OPEN WEBCAM?")
        msg.setStyleSheet("font: 'Time News Roman';font-size:18px")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        response = msg.exec_()
        if response == QMessageBox.No:
            path = self.get_local_file_path()
            return path
        # You can perform any action if "No" is clicked
        elif response == QMessageBox.Yes:
            return "0"

    def when_click(self):
        sio.connect(uri)

        path = self.showpopup()
        print("path", path)
        sio.emit("process", path)
        self.worker.run()
        self.button.setEnabled(False)

    def enable_button(self):
        self.button.setEnabled(True)

    def update_image(self, image_data):

        self.scene.clear()
        self.scene.addPixmap(image_data)


application = QApplication(sys.argv)
Root = App()


@sio.event
def frame_transmit(data):
    Root.updateImage(data)


if __name__ == "__main__":

    Root.show()

    sys.exit(application.exec())
