# Projective-Transformation-Stereo-Matching

## Stereo Matching

### Problem Statement
Use two rectified images as the inputs, estimate depth map and compare the results quantitatively and qualitatively with ground truth image provided for pair of input images.

### Algorithm
•	Input Images from both left and right camera are taken as the input by this program along with the ground truth depth map. 

•	All the images are converted to grayscale, this step is done to increase the computational speed.

•	If input image size is found larger than certain threshold level, image resizing is done, which helps to boost computational speed.

•	Two types of scoring schemes have been used here to compute depth map (Sum of Squared Differences(SSD) and Cross Correlation(cor) ).

•	The sharpness and smoothness of depth map depends on Window Size and Maximum Offset Levels that can be tuned as per use case.

•	The computed depth map is saved as output image.

•	The ground truth and computed Depth Maps are used to compute the end point error and error rate. These measures show how well application performs on input image pairs for depth estimation.

### Class Methods and Design Choices

#### resizeTemplate()
This method takes input image and resizing factor as input. The resizing factor must be a number between (0.25 - 1) where 0.25 implies that image is reduced to 1/4th of its original size and 1 implies no change in the image size. Resized image is given as output.

#### SSD()
This method takes left and right input images along with row, column, window size and offset information as input and computes the sum of squared differences between left and right input images which is returned as output. The formula for the same has been shown below:

![plot](./Formulae/ssd.JPG)

#### cor()
This method takes left and right input images along with row, column, window size and offset information as input and computes the cross correlation between left and right input images which is returned as output. The formula for the same has been shown below:

![plot](./Formulae/cor.JPG)

#### getDepthMap()
This method takes left and right images as input along with window size, maximum offset, and type of scoring method to be used. If the scoring type is ‘ssd’, then sum of squared difference scoring is used. If the scoring type is ‘cc’, then cross correlation scoring is used. Offset factor is calculated as 255 / maxOffset. This is done to ensure that pixel values in depth map always lie between 0 and 255. 

For each pixel in the left image, all the pixels in the corresponding window along with offset are compared from the right image. The offset of pixel with the least score is chosen as the output offset level. This offset is multiplied by the offset factor to get the corresponding pixel value for the depth map from the calculated disparity. The depth map is returned as output by this method.

#### endPointError()
This function takes depth map and ground truth images as input and calculates the end point error between images which is returned as output. The implementation uses following formula:

![plot](./Formulae/epe.JPG)

#### errorRate()
This function takes depth map and ground truth images as input and calculates the error rate between images which is returned as output. The implementation uses following formula:

![plot](./Formulae/er.JPG)

#### stereoMatch()
This method is the main method which implements all the steps mentioned in Algorithm using the above support functions.

### Results
