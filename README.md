# This is a brief sum of the test for the Delta Cognition company for the machine learning intern test.


## Idea forming:
My initial thoughts on the problem were using a pre-trained model for the object detection and fine tuning with datasets such as ApolloSpace. <br><br>
For novel object detection, my idea was trying to label uncertain object (objects that has a low accuracy score under a certain threshold) as novel object. <br><br>
For collision avoidance, I planed to find simple algorithm or method that can calculate the distance between the obstacles boundary boxes and the simulated boundary box of the vehicle. But because of the time limit and limit experience, I rushed into the making of the app, intended to leave the rest of the research later.
<br><br>
I did come across the use of optical flow for colision avoidance but decided to skip in order to try to but some build the back bone for the project.

## Researches done:
This topic is relative new for me. In the process of researching, I came across multiple powerfull pre-trained models that fit the mission of the test. I decided to test with YOLOv8n and YOLO11n due to their fast response with aaccuracy tradeoff. <br><br>
I also saw MMDetection from OpenMMLab and Object Detection from Mediapipe, but I decided to try out YOLO and Mediapipe.
<br><br>
The result of the atempts of testing those pre-trained models can be found in ***test.ipynb***.<br><br>
Both model can be used to detect objects in separate frame from a video format file, hence the same method can be applied for webcam, dashcam in cars, all I need now is an app to display both the decision to avoid colision and result of object detection.
<br><br>

## App building:
I choose PyQt5 just for the sake of not changing coding language, I intended to build a webapp, host a server that can streaming individual images after the model has already processed them. Therefore, a ***server_v2.py*** was build base on my recent project but it didn't work. <br><br>
I built 3 different version of the app just to test things out. I test the media on the first version, tried connecting and processing asynchronously with server on the second version and try but everthing on a single file with the third.<br><br>
The app files respectively are ***app.py***, ***app_v2.py*** and ***app.v3**

## Result:
Unfortunately, with given time, the project can not be finished on  time. I planed to clean up the codes, the files when I finish but my lack of experience and knowledge lead to this result, I hope I will receive a feedback from the company for my improvement in the future. <br><br>
Thank you for considering me.