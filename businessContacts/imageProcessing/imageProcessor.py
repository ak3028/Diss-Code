from PIL import Image
# import matplotlib as m
# from matplotlib.pyplot import tricontour
import pytesseract
import cv2
import numpy as np
import math


# This method is called from the UI 
# to get the Image from the Input URL 
def getImageFromURL(imageURL):
    return cv2.imread(imageURL)

# This method is the main method that performs all the image processing
# and return the final image to be passed to the OCR engine
def processImageForOcr(image):

    # This image is passed directly for ocr in case the boundary of the card is not detected
    imageGrayScaleOriginal = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    resizedImage, ratio = resizeImage(imageGrayScaleOriginal)

    imageGaussianBlur = cv2.GaussianBlur(resizedImage, (5,5), 0)  # 5,5 can be used | higher the kernel value more the blur
    
    imageCanny = cv2.Canny(imageGaussianBlur, 50, 200, apertureSize=5)


  
    contours = cv2.findContours(imageCanny,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True) [:5]
    cardContour = ''
    for contour in contours:
        peri = cv2.arcLength(contour,True) # true ensures that the contour is closed 
        approx = cv2.approxPolyDP(contour, 0.02*peri, True)
        if len(approx) == 4 and cv2.contourArea(contour) > 50000: #sometimes an image contains a closed figure which should not be considered as the biggest contour while deciding the card boundary, so we discard such figures.
            cardContour = approx
            break
    
    if cardContour == '':
        isCardBoundaryDetected = False
        return imageGrayScaleOriginal, isCardBoundaryDetected

    
    warpedImage = applyPerspectiveTransform(imageGrayScaleOriginal, cardContour, ratio)
    

    isCardBoundaryDetected = True

    return warpedImage, isCardBoundaryDetected


# This method just returns a resized image 
# The image is resized while preserving the aspect ratio    
def resizeImage(image):
    ratio = image.shape[0] / 500.0
    image = resize(image, height = 500)
    return image, ratio

# This is the generic method that we use for resizing the image.
# Source - 
def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

# This method applied perspective correction on the input image
# and returns the warped image that can be passed to the OCR engine.
# source - 
def applyPerspectiveTransform(orig, cardContour, ratio):

    warped = four_point_transform(orig, cardContour.reshape(4, 2) * ratio)

    return warped

# source - 
def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

# source - 
def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect









