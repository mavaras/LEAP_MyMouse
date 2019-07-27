

# LEAP MyMouse
The purpose of this proyect is mainly to explore the field of gesture recognition, specifically hand gestures, and apply that to control a computer and interact with it. It uses the Leap Motion device and includes simple and complex hand gesture recognition.

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

![LEAP MyMouse](https://raw.githubusercontent.com/mavaras/LEAP_proyect/origin/readme_files/gui.png)

******
### We have to different kinds of gestures: simple ones and complex ones.
- **Simple gestures**
![simple gesture example (grabbing action)](https://raw.githubusercontent.com/mavaras/LEAP_proyect/origin/readme_files/simple_gesture.gif)
******
- **Complex gestures**
Here we have the $DollarRecognizer algorithm, working with some predefined letter templates, such as T, V, N, D, L, W or Z. The main future improvement is to include the implemented NN with the MNIST dataset into this control, so that the user can draw in the air the 1 to 9 numbers instead of this letters, offering this way the user two ways to perform complex gestures.

![complex gesture example (T gesture)](https://raw.githubusercontent.com/mavaras/LEAP_proyect/origin/readme_files/simple_gesture.gif)

## TODO
Some features to perform are:
- Multilayer Neural Network included into the interaction
- Add more templates
- Add gifs
- Pretty hand visualization :)

###  How the NN should be integrated into the interaction
![NN into Leap Motion control (spanish :3)](https://raw.githubusercontent.com/mavaras/LEAP_proyect/origin/readme_files/NNdiagram.png)


## Contact
- Mario Varas: elasgard@hotmail.es
- [Linkedin](https://www.linkedin.com/in/mario-varas-gonz%C3%A1lez-270604174/)
