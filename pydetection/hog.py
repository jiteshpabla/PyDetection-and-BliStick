import numpy as np
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils
import cv2


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    for i in range(5,10):
        image=cv2.imread('pic'+str(i)+'.jpg')
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
        #(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        #    padding=(8, 8), scale=1.05)

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
        cv2.waitKey(10000)
#cv2.destroyAllWindows()
