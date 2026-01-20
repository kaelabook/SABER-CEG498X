# CircleRecognition
## Descriptuon
This class is responsible for being the entrypoint to the origin side programs. This takes in   images, loads metadata about them into the database, processes them to the point where red circles are detected, and returns true or false regarding the presence of red circles.
## External Dependencies
- OpenCV
- numpy (packaged with OpenCV)
```
pip install python-opencv numpy
```
imported with:
```
import cv2
import numpy as np
```
## Internal Dependencies
- Database_SABER
- validationUtility_SABER
```
from Database.Database_SABER import Database_SABER
from Utilities.validationUtility_SABER import validationUtility_SABER, handleExceptions, retryOn
``` 
## Parameters
Hough Circle transform modifiable parameters.
| name            | dataType | Description                                                               | defaultValue | 
|---|---|---|---|
| self.dp         | double   | Ratio of image resolution seen by CV2 and the original image resolution   |  1         |
| self.minDist    | double   | Minimum Distance between centers of multiple circles  (pixels)            |  100          |
| self.param1     | double   | Value modifiying the HoughCircle method HOUGH_GRADIENT modifies the Canny Edge detector |      175        |
| self.param2     | double   | Value modifying the HoughCircle method HOUGH_GRADIENT, a larger number can create more false detections, too small can cause misses           |   32           |
| self.minRadius  | int      | Minimum radius for a detected circle (pixels) |   0           |
| self.maxRadius  | int      | Maximum radius for a detected circle (pixels) (if set to 0 it can detect a circle as big as the image)         |  0            |
## Methods
Publicly callable methods:
``` self.main ``` entrypoint function for the class, calls all internal methods in the correct order and cleans up.
## Database interactions
This class is designed to initialize the origin side database, it is the first instanciation of a Database object referencing the origin database.

Internal methods that perform database interactions:
```self.loadImages``` calls DB.bulkRetrieval searching for the 'path' column in the 'origin' database, querying all rows.
```self.maskRed``` calls DB.setValue and modifies the 'hasRed' column and conditionally the 'hasCircle' column in the 'origin' table. The call for setValue references the 'id' value associated with each image.

FINISH THIS
