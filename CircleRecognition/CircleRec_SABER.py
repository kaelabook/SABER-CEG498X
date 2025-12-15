"""
Class: CirlceRec_SABER
Author: Spencer Mullins
Version: 0.0.2
Last Change: 11/28/25
Description:
Loads in images from a database, determines if any red hue exists in every image,
performs a Hough transform on each image containing red hue,
determines from the Hough transform if the red in an image is a circle,
updates the database to indicate a true or a false based on the detection results.
"""
import cv2
import numpy as np
from Database.Database_SABER import Database_SABER
import time
from Utilities.validationUtility_SABER import validationUtility_SABER, handleExceptions, retryOn
import logging
logger = logging.getLogger("CircleRec_SABER")
#Constants
#HSV Red Spectrum Upper and lower values

LRED1 = np.array([0,100,100])
URED1 = np.array([10,255,255])
LRED2 = np.array([160,100,100])
URED2 = np.array([180,255,255])

Val = validationUtility_SABER



class CircleRec_SABER:
    def __init__(self):
        self.imageArray = []
        self.imageArrayHSV = []
        self.imageArrayBGR = []
        self.imageArrayRedMasked = []
        self.redIDs = []
        self.circleIDs = []
        self.imageIDs = []
        #Hough params
        self.dp = 1
        self.minDist = 100
        self.param1 = 175
        self.param2 = 32
        self.minRadius = 0
        self.maxRadius = 0
        #config values
        self.imagePaths = None
        self.DB = Database_SABER()

    
    @handleExceptions(reRaise=False)
    def warmupHough(self):
        # warm up common sizes (add any others you use)
        sizes = [(1024, 1024), (768, 1349), (720, 1280)]

        for w, h in sizes:
            dummy = np.zeros((w, h), dtype=np.uint8)
            # run median blur and Hough once
            dummy_blur = cv2.medianBlur(dummy, 5)

            cv2.HoughCircles(
                dummy_blur,
                cv2.HOUGH_GRADIENT,
                dp=self.dp,
                minDist=self.minDist,
                param1=self.param1,
                param2=self.param2,
                minRadius=self.minRadius,
                maxRadius=self.maxRadius
            )


    def __del__(self):
        self.DB.cleanup()

    @handleExceptions(reRaise=True)
    def  loadImages(self):
        
        """Loads images for analysis from DB by retrieving paths, using opencv's imread, and appending them to an object -SAM"""
        self.imagePaths, self.imageIDs = self.DB.bulkRetrieval('origin','path')
        Val.emptyCheck(self.imagePaths, "Image path array")
        for path in self.imagePaths:
            Val.emptyCheck(str(path),"Path from imagePaths")
            Val.pathExists(str(path))
            

            logger.info(f" Function {self.loadImages.__name__}: Image loaded from {str(path)}")

            loaded = cv2.imread(str(path))
            Val.emptyCheck(loaded)
            self.imageArray.append(loaded)



    @handleExceptions(reRaise=True)
    def convertHSV(self):
        """Converts images to HSV values using cvtColor, HSV is used for hue analysis -SAM"""
        Val.emptyCheck(self.imageArray)
        for i,image in enumerate(self.imageArray):
            Val.emptyCheck(image, "Image from imageArray")
            logger.info(f" Function {self.convertHSV.__name__}: Image converted to HSV on iteration {i}.")

            self.imageArrayHSV.append(cv2.cvtColor(image,cv2.COLOR_BGR2HSV))
    @handleExceptions(reRaise=True)
    def maskRed(self):
        """Masks for all red hues, if none exist, both red and circle are updated in the DB to be false,
         if red exists in an image, just red is updated to be true for that image. -SAM"""
        Val.emptyCheck(self.imageArrayHSV, "HSV image array")
        Val.emptyCheck(self.imageIDs, "")
        for i,image in enumerate(self.imageArrayHSV):
            #create redmask on image list
            mask1 = cv2.inRange(image, LRED1,URED1)
            mask2 = cv2.inRange(image, LRED2, URED2)

            red_mask = mask1 + mask2

            #if the current redmask is >0 add the images index in the previous array to filter to images with only red
            if cv2.countNonZero(red_mask) > 0:
                self.imageArrayRedMasked.append(image)
                self.redIDs.append(self.imageIDs[i])
                self.DB.setValue('origin','hasRed',1,'id',self.imageIDs[i])
                logger.info(f" Function {self.maskRed.__name__}: Image contained red on iteration {i}.")
            else:
                self.DB.setValue('origin','hasRed',0,'id',self.imageIDs[i])
                self.DB.setValue('origin','hasCircle',0,'id',self.imageIDs[i])
                logger.info(f" Function {self.maskRed.__name__}: Image on iteration {i} did not contain red.")
    
    @handleExceptions(reRaise=True)
    def convertBGR(self):
        """converts images containing red to BGR format, this is going to be used for circle detection -SAM"""
        Val.emptyCheck(self.imageArrayRedMasked, "Red masked array")
        for i,image in enumerate(self.imageArrayRedMasked):
             self.imageArrayBGR.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
             logger.info(f" Function {self.convertBGR.__name__}: Image converted to BGR on iteration {i}")



    @handleExceptions(reRaise=True)
    def findCircles(self):
        """uses a Hough Transform to detect for circles in the images converted to bgr,
        also creates circles to place on the image for visual debugging
        and updates the database to indicate if circles were found or not in the images that had red -SAM"""
        cv2.setUseOptimized(True)
        t0 = time.time()
        Val.emptyCheck(self.imageArrayBGR, "BGR Image Array is empty")
        for i, image in enumerate(self.imageArrayBGR):
            t2 = time.time()

            #convert to grayscale, needed for circle detection
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


            grayImage = cv2.medianBlur(grayImage, 5)
            resized = cv2.resize(grayImage, (360, 360), interpolation=cv2.INTER_AREA)

            #these values were mostly found through guess and check,
            #the variable that seems to have the most effect on false alarm is param2,
            #too high it won't detect anything, too low it detects too much, 32 is the sweet spot for at least the test images that have been used

            t = time.time()
            circles = cv2.HoughCircles(
                resized,
                cv2.HOUGH_GRADIENT,
                dp=self.dp,
                minDist=self.minDist,
                param1=self.param1,
                param2=self.param2,
                minRadius=self.minRadius,
                maxRadius=self.maxRadius
            )


            if circles is not None:

                self.DB.setValue('origin','hasCircle',1,'id',self.redIDs[i])

                self.circleIDs.append(self.redIDs[i])
                logger.info(f" Function {self.findCircles.__name__}: Circle detected in image on iteration {i}.")
                #circles = np.uint16(np.around(circles))

                # for j in circles[0,:]:
                #     currentOrig = self.imageArray[self.redIDs[i]]
                #     #draw the outer circle
                #     cv2.circle(currentOrig,(j[0],j[1]),j[2],(0,255,0),2)
                #         # draw the center of the circle
                #     cv2.circle(currentOrig,(j[0],j[1]),2,(0,0,255),3)

            else:
                self.DB.setValue('origin','hasCircle', 0, 'id', self.redIDs[i])
                logger.info(f" Function {self.findCircles.__name__}: Circle not detected in image on iteration {i}.")
            t3 = time.time()
            logger.info(f" Function {self.findCircles.__name__}: Single loop execution took {t3-t2} seconds for index {i}.")
        t1 = time.time()
        logger.info(f" Function {self.findCircles.__name__}: Full execution took {t1-t0} seconds.")

    #DEBGUG METHODS
    def plotCircles(self):
        """plots the circles on the bgr images, here for visual debugging -SAM"""
        for image in self.imageArrayRedMasked:
            cv2.imshow('image', image)
            cv2.waitKey(0)
            # Destroy all created windows
            cv2.destroyAllWindows()



    #ENTRYPOINT
    def main(self):
        """just performs the circle detection and updates the database, doesn't print or plot -SAM"""
        self.loadImages()
        self.convertHSV()
        self.maskRed()
        self.convertBGR()

        self.findCircles()
        self.__del__()
