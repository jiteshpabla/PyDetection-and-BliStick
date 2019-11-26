# PyDetection-and-BliStick

#### Introduction

This repository contains a basic fuctionality implemplementation of the OpenDetection library in Python named - PyDetection.
It also contains an app called "BliStick" which uses the PyDetection library (served via a server) to aid visually challenged people to identify familiar/friendly faces and humanoid figures.

#### Problem Statement
##### Part 1:
Current “Opendetection” implementation is done on C++, however lots of people use python, specially when it comes to rapid prototyping. Having an implementation of this library in any other popular language will help spread the use of the library and expand the options it offers to the users. 

Therefore, the implementation of “Opendetection” in another popular language (python3) while eliminating the issues present in the current C++ implementation is the problem.

Github link: https://github.com/krips89/opendetection

##### Part 2:
To combat the problems that visually impaired people face everyday, we came up with the idea to develop an app that helps visually impaired people to quickly identify the people around them. It will accept input from the user's surroundings, decipher it to extract information about entities (faces AND figures of people) in the user's environment, and then transmit that information to the subject via auditory means.
All its user need to do is point their phones towards the unidentified person, click a picture, and the app will tell them which person it sees using text that will be spoken out by using text to speech; or the user will has to long press on the screen and the app will tell them how many human figures are present in front of them.
 The app will actually send the clicked image via the available network to a flask server where the actual face recognition will happen and a response of the identified people will be sent back.

The user will also be able to record videos of known people and send them to a server for adding them to the list of known people by training the face recogniser present on the server.
