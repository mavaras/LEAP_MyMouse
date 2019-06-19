# PYTHON 2.7
import numpy as np
import cv2
from scipy.misc import imresize
from tkinter import *
from tkinter import ttk
from PIL import Image
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib
import sys

PATH = 'mlp_model.pkl'


def matrix_to_img(matrix):
    # matrix = cv2.dilate(matrix, np.ones((3, 3), np.uint8), iterations=4)

    img = Image.fromarray(matrix, "RGB")
    img.thumbnail((28, 28), Image.ANTIALIAS)  # resizing to 28x28
    img.save("image_28x28.png")
    # img.show()

    # dilate image
    img = cv2.dilate(cv2.imread("image_28x28.png", cv2.IMREAD_GRAYSCALE),
                     np.ones((3, 3), np.uint8), iterations=1)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("img", img)
    return img


def neural_network(img):
    # setting + normalizing image
    cv2.imshow("image", cv2.resize(img, (200, 200)))
    # img = cv2.resize(img, (8, 8))
    minValueInImage = np.min(img)
    maxValueInImage = np.max(img)
    img = np.floor(np.divide((img - minValueInImage).astype(np.float),
                             (maxValueInImage - minValueInImage).astype(np.float)) * 16)

    # loading digit database
    digits = datasets.load_digits()
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # setting classifier
    """clf = svm.SVC(gamma=0.0001, C=100)
    clf.fit(data[:n_samples], digits.target[:n_samples])"""

    # predict
    print('Loading model from file.')
    clf = joblib.load(PATH).best_estimator_
    predicted = clf.predict(img.reshape((1, img.shape[0] * img.shape[1])))

    # display results
    print("prediction: " + str(predicted))
    plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title("result: " + str(predicted))
    plt.show()


if __name__ == "__main__":
    canvas_width, canvas_height = 400, 400  # canvas size
    w, h = 400, 400  # res img size

    canvas_matrix = np.zeros((h, w, 3), dtype=np.uint8)
    white = [255, 255, 255]
    img = -1

    # matrix to img (test)
    """data = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(28):
        data[c, w/2] = white
        data[w/2, c] = white

    matrix_to_img(data)"""

    # Display code
    print("F to predict")


    def clear():
        canvas.delete("all")


    def click(e):
        if e.num == 1:
            x1, y1 = (e.x - 8), (e.y - 8)
            x2, y2 = (e.x + 8), (e.y + 8)

            clicked = True
            print(canvas)
            # canvas_matrix[e.y*h/canvas_height][e.x*w/canvas_width] = white
            canvas_matrix[e.y][e.x] = white
            canvas.create_oval(x1, y1, x2, y2, fill="#000000")


    def move(e):
        x1, y1 = (e.x - 8), (e.y - 8)
        x2, y2 = (e.x + 8), (e.y + 8)
        # canvas_matrix[e.y*28/canvas_height][e.x*28/canvas_width] = white
        canvas_matrix[e.y][e.x] = white
        canvas.create_oval(x1, y1, x2, y2, fill="#000000")


    def release(e):
        if e.num == 3:
            print("save")


    # matrix_to_img(canvas_matrix)

    def finish_stroke():
        # canvas stroke to img + through neural network
        neural_network(matrix_to_img(canvas_matrix))


    window = Tk()
    window.title("F to convert to image")
    window.bind("q", lambda e: window.destroy())
    window.bind("c", lambda e: clear())
    window.bind("f", lambda e: finish_stroke())

    canvas = Canvas(window, width=canvas_width, height=canvas_height)
    canvas.pack(expand=YES, fill=BOTH)
    canvas.bind("<Button>", click)
    canvas.bind("<B1-Motion>", move)
    canvas.bind("<ButtonRelease>", release)

    mainloop()
