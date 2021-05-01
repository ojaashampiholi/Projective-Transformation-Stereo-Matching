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
