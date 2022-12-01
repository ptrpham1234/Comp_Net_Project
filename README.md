# Comp_Net_Project

## Requirements:

- Design an application layer protocol for three network entities: controller (C), renderer (R) and server (S) to communicate with each other to provide a media consumption service to users. The protocol should be text-based and well documented. Teams should start designing and documenting the protocol before implementing a network application that uses this protocol. A protocol specification (refer to one of the RFCs on the IETF's web page for information on protocol documentation) must be submitted at the end of the project. The purpose of the protocol is to allow C to request a list of media files (for example a text or video file) from S, then  C can request R to render the chosen file. R, upon receiving a request from C, sends a request to S so that S can stream the chosen media file to R for rendering. R has a limitation, it does not have the capability to buffer so it just renders what it receives from S. During the streaming session, C can request R to pause/resume/start-from-the-beginning the streaming. 
- Use mininet to implement a network application that allows a user to use C to request a list of media files stored on S, and select one that the user is interested in. C then asks R to request a streaming session with S, and S starts streaming the selected file to R for rendering (note the limitation of R mentioned above). During a rendering session, the user can use C to control the rendering, e.g. pause/resume/start-from-the beginning. 
- C, R and S must run on different hosts simulated using mininet and use the protocol designed by the team for communications.
- For media file types, at the minimum text files must be supported but audio (e.g. MP3s) and video (e.g. MP4) files should be considered and if implemented will earn extra credits.

### General Flow
![IMG_0127](https://user-images.githubusercontent.com/58368335/204347787-938aa3c3-7051-48ed-a79e-2f3394376971.jpg)

1. Client sends a request for a list of files to the server
2. Server sends back a list of files to the client
3. Client sends a render request to the Render server
4. Render requests file from server
5. Server sends part of the file
    * repeat until all of files are sent
6. Sends rendered data to client.




![YQ5ES](https://user-images.githubusercontent.com/58368335/204420134-8ad152d3-fe19-4a62-9be5-48530b801de7.png)


## How to run:
Start an Ubuntu or Mininet instance. Make sure python 3.0 is install and run the command `sudo python start.py`. This should start Mininet and then inside of Mininet type in the following command `h3 python controller.py` and that should start the controller.
