# Circle Recognition
Class to do red circle detection in sample images.
### Dependencies
python-opencv
matplotlib (might not actually be needed)
numpy
```
pip install python-opencv matplotlib numpy
```
### How to use
1. Create a test directory, enter it.
2. Create a python script, and a list of all image paths seperated by a newline names image_paths.txt in the form: images/example.png\n.
3. Create an image directory with all images within it.
4. Create an empty directory named results.

Import the class, initialize it, call the "analyze" method, the resulting list of images with a circle will be located at results/detected.txt
```
  from circle_detection.CIRCLEREC_SABER import CIRCLEREC_SABER

  test_object = CIRCLEREC_SABER()

  test_object.analyze()
```

<img width="266" height="154" alt="screenshot_22112025_192126" src="https://github.com/user-attachments/assets/cf1636db-649b-4a09-b69b-0fbcf291621c" />

You can also call the private method "_db_full_analysis" to plot all images with circles included, and to print detection information to the terminal.
This is to be used as a debug feature and is not intended to be used with everything working together.

```
  from circle_detection.CIRCLEREC_SABER import CIRCLEREC_SABER

  test_object = CIRCLEREC_SABER()

  test_object._db_full_analysis()
```
Terminal Output:

<img width="457" height="369" alt="screenshot_22112025_192335" src="https://github.com/user-attachments/assets/0b4a9879-ec29-40fc-ba7a-83399031717e" />




Image output:

<img width="300" height="500" alt="wsu" src="https://github.com/user-attachments/assets/654451e7-f43d-49c6-a6b3-9ec085f733b2" />
<img width="266" height="154" alt="screenshot_22112025_192126" src="https://github.com/user-attachments/assets/a160747b-f2fb-41dd-8612-158e80a08c3c" />

<img width="300" height="500" alt="twentyonepilots" src="https://github.com/user-attachments/assets/08b137b5-3f63-4c6c-9114-60b31c1c00e7" />

<img width="300" height="300" alt="image35" src="https://github.com/user-attachments/assets/2d19fdd0-4338-4de3-ac5f-896a8781cd82" />
<img width="300" height="300" alt="image13" src="https://github.com/user-attachments/assets/121316d6-3be9-4d70-aa03-73b2732f8fa3" />
<img width="300" height="300" alt="image9" src="https://github.com/user-attachments/assets/7d9e81ee-333e-4357-849f-e812867f2bfe" />

Any attempt to create a seperate analysis function should call all private methods in the following order:
```
  def my_custom_analysis(self):
        self.load_images()
        self.hsv_conversion()
        self.mask_red()
        self.bgr_conversion()
        self._find_circles()
        ...
```
### To-Do

- Need to feed in paths with a config file instead of having them be hardcoded.
- Need to test extensively with a large amount of images to ensure confidence
- Unit tests
- Add detected images to readme - add a save method for the opencv modified images

