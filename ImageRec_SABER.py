import matplotlib.pyplot as plt
import cv2
import numpy as np
from pathlib import Path
import os

#Constants

#HSV Red Spectrum Upper and lower values
LRED1 = np.array([0,100,100])
URED1 = np.array([10,255,255])
LRED2 = np.array([160,100,100])
URED2 = np.array([180,255,255])

class ImageRec_SABER:
    def __init__(self):
        self.list_file = 'image_paths.txt'
        self.image_array = []
        self.hsv_image_array = []
        self.bgr_image_array = []
        self.red_index_array = []
        self.masked_image_array = []
        self.circle_index_array = []
        self.circle_array = []
        self.image_files = []
        self.image_files_names = []


    """
    name: load_images
    last edit: 10/5/2025 SAM
    description: 
    loads the test images in, appends them to the image_array class parameter for self use later
    needed future capability:
    eventually will need to load in image file names either from an entire directory (mounted flash drive), or a file
    Update 10/6/2025 - files able to be loaded in from text file
    """
    def load_images(self):
        try:
            with open(self.list_file) as f:
                for line in f:
                    path = line.strip()
                    if path and os.path.exists(path):
                        self.image_files.append(path)
                    elif path:
                        print(f"Warning: Image path not found or invalid: {path} ")
        except FileNotFoundError:
            print(f"Error: Text file not found at {self.list_file}")       
            

        for file in self.image_files:
            self.image_array.append(cv2.imread(file))

    """
    name: plot_images
    last edit: 10/5/2025 SAM
    description: 
    shows the images loaded in, kind of bad and just used for debugging
    """
    """
    def plot_images(self):
        for image in self.image_array:
            
            cv2.imshow('image', image)
            cv2.waitKey(0)
            # Destroy all created windows
            cv2.destroyAllWindows() """
    """

    name: hsv_conversion
    last edit: 10/5/2025 SAM
    description: 
    converts the original image files to hsv which represents the image as a hue spectrum instead of its standard RGB value

    """
    def hsv_conversion(self):
        #takes the original images and converts them all to hsv format to determine the hue value makeup of the images
        for image in self.image_array:
            self.hsv_image_array.append(cv2.cvtColor(image,cv2.COLOR_BGR2HSV))
    """
    name: mask_red
    last edit: 10/5/2025 SAM
    description: 
    masks all images to only red hues, this will be used to determine if an image should be thrown out or kept for circle detection
    
    """
    def mask_red(self):
        #
        for i,image in enumerate(self.hsv_image_array):
            #create redmask on image list
            mask1 = cv2.inRange(image, LRED1,URED1)
            mask2 = cv2.inRange(image, LRED2, URED2)

            red_mask = mask1 + mask2
            #if the current redmask is >0 add the images index in the previous array to filter to images with only red
            if cv2.countNonZero(red_mask) > 0:
                self.masked_image_array.append(red_mask)
                self.red_index_array.append(i)
                #print('red found in image')
            #else:
                #print('red not found in image')
    """
    name: mask_red
    last edit: 10/5/2025 SAM
    description: 
    converts masked images to bgr for further circle detection
    
    """
    def bgr_conversion(self):
        for image in self.masked_image_array:
             self.bgr_image_array.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    """
    name: show_red_images
    last edit: 10/5/2025 SAM
    description: 
    shows the red masked images used for debugging
    """
    """  def show_red_images(self):
        for image in self.masked_image_array:
            cv2.imshow('image', image)
            cv2.waitKey(0)
            # Destroy all created windows
            cv2.destroyAllWindows() """
    """
    name: find_circles
    last edit: 10/5/2025 SAM
    description: 
    finds circles in the images, detects using cv2s Hough transform, some magic number parameters
    """
    
    def find_circles(self):

        for i,image in enumerate(self.bgr_image_array): 
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
                #for i in circles[0,:]:
                        # draw the outer circle
                        #cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
                        # draw the center of the circle
                        #cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)

    #here for debugging don't use unless you uncomment the 'for i in circles[0,:]:' loop in find_circles(), 
    # also should not be used at all for production because it edits the original images, might fix this later
    """def plot_circles(self):
     
        for image in self.bgr_image_array:
            cv2.imshow('image', image)
            cv2.waitKey(0)
            # Destroy all created windows
            cv2.destroyAllWindows()    """
    
    """
    name: print_results
    last edit: 10/5/2025 SAM
    description: 
    prints resulting red detection and circle detection, mostly used for debug but will eventually be utilized
    to send to code used for encryption/compression/encoding for transmission
    """
   
    def print_results(self):
        for index in self.red_index_array:
            print('Red detected in ' + self.image_files[index])

        #the indexes stored for images that contain circles are relative to the indexes of images that contain red, 
        # to recover the original file names we have to index the red_index_array from the circle_index_array
        for index in self.circle_index_array:
            print('Circle detected in ' + self.image_files[self.red_index_array[index]])
    
    def full_analysis(self):
        self.load_images()
        self.hsv_conversion()
        self.mask_red()
        self.bgr_conversion()
        self.find_circles()
        self.print_results()






testObject = ImageRec_SABER()
testObject.full_analysis()