# import socketio
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl, QThread
import asyncio
import socketio
import cv2
import base64
import cv2

# from modelfile.detect import run
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
from modelfile.utils import visualize
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# uri = "http://127.0.0.1:5000/"

# sio = socketio.Client()


# @sio.event
# def connect():
#     print("Đã kết nối với server")


# Xử lý sự kiện khi ngắt kết nối
# @sio.event
# def disconnect():
#     print("Đã ngắt kết nối với server")


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    ButtonUpdate = pyqtSignal()

    def __init__(self, path="./jo.jpg", id=0, parent=None):
        super().__init__(parent)
        self.path = path  # Store the path as an instance variable
        self.ThreadActive = False
        self.camera_id = id

    def run(self):
        self.ThreadActive = True
        # sio.on(
        #     "frame_transmit", self.handle_frame
        # )  # Listen to the 'frame' event from the server
        # print("start listening")  # Keep listening for incoming frames
        # sio.wait()

        # Variables to calculate FPS
        counter, fps = 0, 0
        start_time = time.time()

        # Start capturing video input from the camera
        cap = cv2.VideoCapture(self.camera_id if self.camera_id != "0" else 0)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10

        detection_result_list = []

        def visualize_callback(
            result: vision.ObjectDetectorResult,
            output_image: mp.Image,
            timestamp_ms: int,
        ):
            result.timestamp_ms = timestamp_ms
            detection_result_list.append(result)

        # Initialize the object detection model
        base_options = python.BaseOptions(
            model_asset_path="./efficientdet_lite0.tflite"
        )
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            score_threshold=0.5,
            result_callback=visualize_callback,
        )
        detector = vision.ObjectDetector.create_from_options(options)

        # Continuously capture images from the camera and run inference
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                sys.exit(
                    "ERROR: Unable to read from webcam. Please verify your webcam settings."
                )

            counter += 1
            image = cv2.flip(image, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

            # # Run object detection using the model.
            # detector.detect_async(mp_image, counter)
            # current_frame = mp_image.numpy_view()
            # current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)

            # # Calculate the FPS
            # if counter % fps_avg_frame_count == 0:
            #     end_time = time.time()
            #     fps = fps_avg_frame_count / (end_time - start_time)
            #     start_time = time.time()

            # # Show the FPS
            # fps_text = "FPS = {:.1f}".format(fps)
            # text_location = (left_margin, row_size)
            # cv2.putText(
            #     current_frame,
            #     fps_text,
            #     text_location,
            #     cv2.FONT_HERSHEY_PLAIN,
            #     font_size,
            #     text_color,
            #     font_thickness,
            # )

            # if detection_result_list:
            #     # print(detection_result_list)
            #     vis_image = visualize(current_frame, detection_result_list[0])
            #     # print((vis_image))
            #     # print(vis_image.shape())

            #     # Convert the image to QImage format

            # else:
            #     vis_image = current_frame
            # # newimg = cv2.imread(vis_image)
            # # print()
            # # newimg = cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)
            # # newimg = cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR)
            cv2.imshow("test", rgb_image)
            converted_img = QImage(
                rgb_image.data,
                rgb_image.shape[1],
                rgb_image.shape[0],
                rgb_image.strides[0],
                QImage.Format_RGBA8888,
            )
            # Resize the image to fit the UI
            Pic = converted_img.scaled(640, 480, Qt.KeepAspectRatio)
            # Emit the image to update the GUI
            self.ImageUpdate.emit(Pic)
            detection_result_list.clear()
            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break

        detector.close()
        cap.release()
        self.ButtonUpdate.emit()
        cv2.destroyAllWindows()

    def stop(self):
        self.ThreadActive = False
        # sio.off("frame_transmit")
        # sio.shutdown()
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

        self.graphic = QLabel()
        # self.scene = QGraphicsScene()
        # self.graphic.setScene(self.scene)
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

        path = self.showpopup()
        print("path", path)
        self.worker.run()
        self.button.setEnabled(False)

    def enable_button(self):
        self.button.setEnabled(True)

    def update_image(self, image_data):
        # print("img", image_data)
        # self.scene.clear()
        self.graphic.setPixmap(QPixmap.fromImage(image_data))


application = QApplication(sys.argv)
Root = App()


# @sio.event
# def frame_transmit(data):
#     Root.updateImage(data)


if __name__ == "__main__":

    Root.show()

    sys.exit(application.exec())
