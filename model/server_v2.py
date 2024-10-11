import os
import numpy as np
import torch
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import websockets
import logging
import socketio
import asyncio
import cv2
import base64

# import I
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server SocketIO
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    logger.info(f"Client {sid} connected")


@sio.event
def disconnect(sid):
    logger.info(f"Client {sid} disconnected")


@sio.event
def process(sid, data):
    asyncio.run(process_video2(sid, data))
    # logger.info("received")


global stop_processing
stop_processing = False


@sio.event
def letstop(sid):
    global stop_processing
    stop_processing = True
    print("Stoping")


async def process_video2(sid, path):
    global stop_processing
    try:
        print("RECEIVED.")

        # Receive the video file link from the client
        video_link = path
        if not video_link:
            raise ValueError("Empty video link received")
        print("Received video link:", video_link)

        # Attempt to open the video file for processing
        cap = cv2.VideoCapture(0 if video_link == "0" else video_link)
        if not cap.isOpened():
            sio.disconnect(sid)
            raise IOError("Failed to open video file: " + video_link)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        isProcessing = False
        processing_delay = (
            5  # Simulated delay between sending responses (adjust as needed)
        )

        while True:
            # Check if the server is still processing the previous frame

            if isProcessing:
                await asyncio.sleep(processing_delay)
                continue

            if stop_processing:
                print("Stop signal received. Terminating process.")
                stop_processing = False
                break
            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break

            # Set the processing flag to indicate that the server is busy
            isProcessing = True

            frame_count += 1
            print(f"Processing frame {frame_count}...")

            # Convert the frame to grayscale
            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Encode the frame as base64
            frame_data = cv2.imencode(".jpg", frame)[1].tobytes()
            # base64_frame = base64.b64encode(frame_data)

            print(f"Emitting frame data of length: {len(frame_data)}")
            # Send the base64-encoded frame to the client
            sio.emit("frame", (frame_data))
            print("TYPE:", type(frame_data))
            # Simulate processing delay
            await asyncio.sleep(processing_delay)

            # Reset the processing flag once frame processing is complete
            isProcessing = False

        # Close the video file and connection when finished
        cap.release()
        print("Video processing complete. Closing connection.")
        sio.disconnect(sid)

    except Exception as e:
        print(f"Error on the server: {str(e)}")


@sio.event
def testing(sid, data):
    print(f"Received testing data from {sid}: {data}")
    sio.emit("frame", data)
    sio.disconnect(sid)


async def process_video3(sid, path):
    global stop_processing
    try:
        print("RECEIVED.")

        # Receive the video file link from the client
        video_link = path
        if not video_link:
            raise ValueError("Empty video link received")
        print("Received video link:", video_link)

        # Attempt to open the video file for processing
        cap = cv2.imread(0 if video_link == "0" else video_link)
        # if not cap.isOpened():
        #     raise IOError("Failed to open video file: " + video_link)
        # fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        isProcessing = False
        processing_delay = (
            2  # Simulated delay between sending responses (adjust as needed)
        )

        while True:
            # Check if the server is still processing the previous frame

            if isProcessing:
                await asyncio.sleep(processing_delay)
                continue

            if stop_processing:
                print("Stop signal received. Terminating process.")
                stop_processing = False
                break
            # Read a frame from the video
            # ret, frame = cap.read()
            # if not ret:
            #     break

            # Set the processing flag to indicate that the server is busy
            isProcessing = True

            frame_count += 1
            print(f"Processing frame {frame_count}...")

            # Convert the frame to grayscale
            # gray_frame = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

            # Encode the frame as base64
            frame_data = cv2.imencode(".jpg", cap)[1].tostring()
            # base64_frame = base64.b64encode(frame_data).decode("utf-8")

            print(f"Emitting frame data of length: {len(frame_data)}")
            # Send the base64-encoded frame to the client
            sio.emit("frame", frame_data)
            print("TYPE:", type(frame_data))
            # Simulate processing delay
            await asyncio.sleep(processing_delay)

            # Reset the processing flag once frame processing is complete
            isProcessing = False
            break

        # Close the video file and connection when finished
        # cap.release()
        print("Video processing complete. Closing connection.")
        sio.disconnect(sid)

    except Exception as e:
        print(f"Error on the server: {str(e)}")
        sio.disconnect(sid)


if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(("localhost", 5000)), app)
