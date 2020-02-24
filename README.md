<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/logo.PNG">
</p>

# LEAP MyMouse
<p align="justify">
The purpose of this proyect is mainly to explore the field of gesture recognition, specifically hand gestures, and apply that to control a computer and interact with it. It uses the Leap Motion device and includes simple and complex hand gesture recognition.
</p>

## Getting started
### You need to have
- Python **2.7**
- Leap Motion device

### Setting up
```
git clone <this_repo>
cd LEAP_MyMouse

pip install -r requirements.txt
python main.py
```

## Usage

<p align="center">
  <img width="607" height="350" title="asldfkj" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/gui.png">
</p>
<p align="justify">
We have two main sections, the left one is related to visualize data of our hands, in both planes, XY and XZ, and the right section is about configuration settings. There you can customize all the action-gesture assignments.

In the menubar, you can save and load customized configuration files, between other options.
</p>

******

### We have to different kinds of gestures: simple ones and complex ones.
- **Simple gestures**
<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/simple_gesture.gif">
</p>
<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/simple_gesture2.gif">
</p>

******

- **Complex gestures**
<p align="justify">
Here we have the $DollarRecognizer algorithm, working with some predefined letter templates, such as T, V, N, D, L, W or Z. The main future improvement is to include the implemented NN with the MNIST dataset into this control, so that the user can draw in the air the 1 to 9 numbers instead of this letters, offering this way the user two ways to perform complex gestures.<br><br>
This way, when you draw a letter in the air, the assigned action is performed, for example close or minimize a window, show the desktop etc.
</p>
<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/complex_gesture.gif">
</p>

</p>
<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/complex_gesture2.gif">
</p>

******

                               Extra: some PowerPoint interactions.
<p align="center">
  <img width="607" height="350" src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/powerpoint_interaction.gif">
</p>

## TODO
Some features to perform are:
- Multilayer Neural Network included into the interaction
- Add more templates
- Add gifs
- Pretty hand visualization :)
****
####  How the NN should be integrated into the interaction, spanish ;)
<p align="center">
  <img src="https://raw.githubusercontent.com/mavaras/LEAP_MyMouse/master/readme_files/NNdiagram.PNG">
</p>

- You can download the full PDF document of the project (spanish) here: https://mega.nz/#!P0QgQIqa!cOsuy9KXdbuxyVKCUtuxyoTVq2GHXsHhX0H1f_9Bp2o

## Contact
- Mario Varas: elasgard@hotmail.es
- [Linkedin](https://www.linkedin.com/in/mario-varas-gonz%C3%A1lez-270604174/)
