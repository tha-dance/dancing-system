# Dancing System - Group 5

## This repository is used for implementing the system that we designed in the design report. 

## Arduino Perspective 
The code on Arduino collects data from 3 accelerometer sensors and sends the data to Raspberry Pi for further processing. 

## Raspberry Pi Perspective 
Pi receives data from Arduino and parses the data. Then it loads the ML models(We combined 2 models to predict the dance moves in order to make the predicted result more reliable) to predict dance moves from parsed move data. After that it will send the predicted move to server side through communciation protocol.

## ML model training Perspective
Initially, there were four algorithms that we trained during the journey of this project. We chose two different implementions of MLP from Dingfan and Archana to form our final Machine Learning subsystem. 

- Random Forest 
- MLP (scikit learn)
- MLP (Keras)
- CNN

## Server Perspective 
The server code is provided by Professor Peh and its basic function is to build the communication pipeline with Raspeberry Pi, receive predicted dance moves from Pi side and output the next move for dancers to dance accordingly. 

## Authors 
* Archana Pradeep 
* Jeremy Long Shi Wei
* Loh Denna
* Tee You Kuan 
* Yan Wei Cheng
* Zhao Dingfan
