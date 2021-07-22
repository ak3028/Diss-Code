from PIL import Image
import matplotlib as m
from matplotlib.pyplot import tricontour
import pytesseract
import cv2
import numpy as np

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag


def getAllTextFromCard(imageURL):
    image = cv2.imread(imageURL)
    # imageGrayScale = imageToGrayScale(image)
    return pytesseract.image_to_string(image)



def imageToGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  










