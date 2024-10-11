import asyncio
import socketio
import numpy as np
import cv2
import base64

sio = socketio.Client()


def handler_frame(data):
    print(len(data))


@sio.event
def frame(data):
    print(len(data))
    # base64_data = data.split(",")[0]  # Get the base64 part
    nparr = np.frombuffer(data, np.uint8)
    # nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # cv2.imwrite("./jo2.jpg", Image)
    cv2.imshow("frame", frame)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()  # Close the window after the key press


def main():
    sio.connect("http://127.0.0.1:5000/")
    # data = input()
    sio.emit("process", "./test.mp4")
    sio.wait()
    sio.shutdown()


if __name__ == "__main__":
    main()
