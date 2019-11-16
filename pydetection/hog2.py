import numpy as np
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils
import cv2

if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture(0)
    while True:
	    _,image=cap.read()
	    '''
	    found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
	    print(len(found),"\n##############################")
	    draw_detections(frame,found)
	    cv2.imshow('feed',frame)
	    cv2.waitKey(10000)
	    '''
	    #image = imutils.resize(image, width=min(400, image.shape[1]))
	    orig = image.copy()
	 
	    # detect people in the image
	    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
	        padding=(8, 8), scale=1.05)
	 
	    # draw the original bounding boxes
	    for (x, y, w, h) in rects:
	        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
	 
	    # apply non-maxima suppression to the bounding boxes using a
	    # fairly large overlap threshold to try to maintain overlapping
	    # boxes that are still people
	    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	 
	    # draw the final bounding boxes
	    for (xA, yA, xB, yB) in pick:
	        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
	 
	    # show some information on the number of bounding boxes
	    #filename = imagePath[imagePath.rfind("/") + 1:]
	    #print("[INFO] {}: {} original boxes, {} after suppression".format(
	    #    filename, len(rects), len(pick)))
	 
	    # show the output images
	    #cv2.imshow("Before NMS", orig)
	    #cv2.waitKey(10000)
	    cv2.imshow("After NMS", image)
	    key = cv2.waitKey(10)
	    if key == 27:
	    	break
	#cv2.destroyAllWindows()
