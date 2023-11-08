# Surveillance Project with AI Integration

This Python backend will run 24/7 on a server and request images from a ESP32-CAM module plugged into a wall or battery. 
The ESP32-CAM sends 320x240 resolution images back.

### TODO
YoloV7 is used to run the images and check for humans.
The images with humans are flagged and kept forever. The images without humans are deleted in 7 days.

These images are available to see on the web application powered by React. The link to that repo is here: TODO


# Note:
Create a copy of the `config_example.json` file and rename it to `config.json`. Change the passcode in the new config file to whatever you wish. The code from the ESP32-CAM's side should check that passcode as a basic precaution to make sure no one else on your network is seeing the images.

That being said, you must use the ESP32-CAM on a secured network as it is not hard to use a simple brute force attack to find the correct if one already has access to the same network the ESP32-CAM is running on.

The link to the code for the ESP32-CAM is here: TODO