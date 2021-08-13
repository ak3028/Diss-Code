from PIL import Image
# import matplotlib as m
# from matplotlib.pyplot import tricontour
import pytesseract
import cv2
import numpy as np
import math


 
def getImageFromURL(imageURL):
    return cv2.imread(imageURL)

def processImageForOcr(image):

    originalImage = image.copy()
   
    resizedImage, ratio = resizeImage(image)

    imageGrayScale = imageToGrayScale(resizedImage)

    # grayImageForOcr = originalImage # get a copy of image to be passed directly for ocr in case the boundary of the card is not detected

    grayImageForOcr = imageGrayScale

    showImage('GrayScale', imageGrayScale)

    imageGaussianBlur = applyGaussianBlur(imageGrayScale)

    showImage('Blurred', imageGaussianBlur)

    imageCanny = cannyEdgeDetection(imageGaussianBlur)
  
    showImage('CannnyImage', imageCanny)

    # imageDilate = dilateImage(imageCanny)
    # showImage('Dilated Image', imageCanny)

    contours = cv2.findContours(imageCanny,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = getContours_BasedOn_CV2_Version(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True) [:5]
    # c = max(contours, key = cv2.contourArea)
    cardContour = ''
    for contour in contours:
        peri = cv2.arcLength(contour,False) # true ensures that the contour is closed 
        approx = cv2.approxPolyDP(contour, 0.02*peri, True)
        if len(approx) == 4 and cv2.contourArea(contour) > 50000: #sometimes an image contains a closed figure which should not be considered as the biggest contour while deciding the card boundary, so we discard such figures.
            cardContour = approx
            break
    
    if cardContour == '':
        isCardBoundaryDetected = False
        return grayImageForOcr, isCardBoundaryDetected

    cv2.drawContours(resizedImage, [cardContour], -1, (0, 255, 0), 2)
    showImage('ImageContours', resizedImage)
    
    warpedImage = applyPerspectiveTransformAndThreshold(originalImage, cardContour, ratio)
    
    showImage('ImageWarped', warpedImage)

    imageForOcr = imageToGrayScale(warpedImage)
    showImage('Image for OCR', imageForOcr)
    isCardBoundaryDetected =True
    print(isCardBoundaryDetected)
    return imageForOcr, isCardBoundaryDetected

def getContours_BasedOn_CV2_Version(cntrs):
    if len(cntrs) == 2:
        contours = cntrs[0]
    
    elif len(cntrs) == 3:
        contours = cntrs[1]

    else:
        raise Exception("Contour tuples should either have a length of 2 or 3")

    return contours
        
def resizeImage(image):
    ratio = image.shape[0] / 500.0
    image = resize(image, height = 500) # alok can make his function here
    return image, ratio

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

def applyPerspectiveTransformAndThreshold(orig, screenCnt, ratio):

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    return warped

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

def dilateImage(imageCanny):
    kernel = np.ones((5,5))
    return cv2.dilate(imageCanny, kernel, iterations = 2)

def applyErosion(imageDilated):
    kernel = np.ones((5,5), np.uint8)
    return cv2.erode(imageDilated, kernel, iterations = 1)

def cannyEdgeDetection(image):
    # return cv2.Canny(image, 80, 80, apertureSize=3)    
    # return cv2.Canny(image, 75, 200, apertureSize=3) # doesnt give good results   
    # return cv2.Canny(image, 50, 200, apertureSize=5) # gives better result for tilted cards with apperturesize = 5
    return cv2.Canny(image, 50, 200, apertureSize=5) # aperture size is reduced to avoid small contorus that is formed by noise
    # apperture size of 5 is better in reading characters in some card like carol soh card

def imageToGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
def applyGaussianBlur(image):
    return cv2.GaussianBlur(image, (5,5), 0)  # 5,5 can be used | higher the kernel value more the blur

def preprocessUsingNLTK(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def showImage(imageType, image):
    pass
    # cv2.imshow(imageType, image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 







