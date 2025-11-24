"""
Class: CirlceRec_SABER
Author: Spencer Mullins
Version: 1.0.0
Last Change: 11/23/25
Description:
Loads in images from a database, determines if any red hue exists in every image,
performs a Hough transform on each image containing red hue,
determines from the Hough transform if the red in an image is a circle,
updates the database to indicate a true or a false based on the detection results.
"""
import cv2
import numpy as np
from database.Database_SABER import Database_SABER

#Constants
#HSV Red Spectrum Upper and lower values
LRED1 = np.array([0,100,100])
URED1 = np.array([10,255,255])
LRED2 = np.array([160,100,100])
URED2 = np.array([180,255,255])

class CircleRec_SABER:
    def __init__(self):
        self.image_array = []
        self.hsv_image_array = []
        self.bgr_image_array = []
        self.red_index_array = []
        self.masked_image_array = []
        self.circle_index_array = []
        self.circle_array = []
        self.image_paths = None
        self.DB = Database_SABER()


    def  _load_images(self):
        """Loads images for analysis from DB by retrieving paths, using opencv's imread, and appending them to an object -SAM"""
        self.image_paths=self.DB.retrieve_image_paths()
        for path in self.image_paths:
            self.image_array.append(cv2.imread(path))



    def _hsv_conversion(self):
        """Converts images to HSV values using cvtColor, HSV is used for hue analysis -SAM"""
        for image in self.image_array:
            self.hsv_image_array.append(cv2.cvtColor(image,cv2.COLOR_BGR2HSV))

    def _mask_red(self):
        """Masks for all red hues, if none exist, both red and circle are updated in the DB to be false,
         if red exists in an image, just red is updated to be true for that image. -SAM"""
        for i,image in enumerate(self.hsv_image_array):
            #create redmask on image list
            mask1 = cv2.inRange(image, LRED1,URED1)
            mask2 = cv2.inRange(image, LRED2, URED2)

            red_mask = mask1 + mask2
            #if the current redmask is >0 add the images index in the previous array to filter to images with only red
            if cv2.countNonZero(red_mask) > 0:
                self.masked_image_array.append(red_mask)
                self.red_index_array.append(i)
                self.DB.update_red(self.image_paths[i],1)
            else:
                self.DB.update_red(self.image_paths[i],0)
                self.DB.update_circle(self.image_paths[i], 0)

    def _bgr_conversion(self):
        """converts images containing red to BGR format, this is going to be used for circle detection -SAM"""
        for image in self.masked_image_array:
             self.bgr_image_array.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


    def _find_circles(self):
        """uses a Hough Transform to detect for circles in the images converted to bgr,
        also creates circles to place on the image for visual debugging
        and updates the database to indicate if circles were found or not in the images that had red -SAM"""
        for i, image in enumerate(self.bgr_image_array):
            #convert to grayscale, needed for circle detection
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            gray_image = cv2.medianBlur(gray_image, 5)

            #these values were mostly found through guess and check, 
            #the variable that seems to have the most effect on false alarm is param2,
            #too high it won't detect anything, too low it detects too much, 32 is the sweet spot for at least the test images that have been used
            circles = cv2.HoughCircles(
                gray_image,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=100,      
                param1=175,         
                param2=32,       
                minRadius=10,        
                maxRadius=300
            )
            if circles is not None:
                circles = np.uint16(np.around(circles))
                self.circle_index_array.append(i)
                self.DB.update_circle(self.image_paths[self.red_index_array[i]],hascircle=1)
                for j in circles[0,:]:
                    #draw the outer circle
                    cv2.circle(image,(j[0],j[1]),j[2],(0,255,0),2)
                        # draw the center of the circle
                    cv2.circle(image,(j[0],j[1]),2,(0,0,255),3)
            else:
                self.DB.update_circle(self.image_paths[self.red_index_array[i]], hascircle=0)
    #DEBGUG METHODS
    def plot_circles(self):
        """plots the circles on the bgr images, here for visual debugging -SAM"""
        for image in self.bgr_image_array:
            cv2.imshow('image', image)
            cv2.waitKey(0)
            # Destroy all created windows
            cv2.destroyAllWindows()

    def print_results(self):
        """original validation function for initial development,
        prints results to the console -SAM"""
        for index in self.red_index_array:
            print('Red detected in ' + self.image_paths[index])

        #the indexes stored for images that contain circles are relative to the indexes of images that contain red, 
        # to recover the original file names we have to index the red_index_array from the circle_index_array
        for index in self.circle_index_array:
            print('Circle detected in ' + self.image_paths[self.red_index_array[index]])

    def _debug_full_analysis(self):
        """prints everything, plots everything, here to debug"""
        self._load_images()
        self._hsv_conversion()
        self._mask_red()
        self._bgr_conversion()
        self._find_circles()
        self.print_results()
        self.plot_circles()
    #ENTRYPOINT METHOD
    def analyze(self):
        """just performs the circle detection and updates the database, doesn't pring or plot -SAM"""
        self._load_images()
        self._hsv_conversion()
        self._mask_red()
        self._bgr_conversion()
        self._find_circles()

