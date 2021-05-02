import numpy as np
from PIL import Image
import imageio
import sys

class stereoMatching():
    def resizeTemplate(self, template, factor):
        temp = template.resize((int(template.width * factor), int(template.height * factor)))
        return np.asarray(temp)

    def SSD(self, left, right, row, col, windowSize, offset):
        ssd_total = 0
        for x in range(-(windowSize//2), (windowSize//2)):
            for y in range (-(windowSize//2), (windowSize//2)):
                ssd = int(left[row+x,col+y] - int(right[row+x, col+y-offset]))
                ssd_total += ssd * ssd
        return ssd_total

    def cor(self, left, right, row, col, windowSize, offset):
        cc_total = 0
        for x in range(-(windowSize // 2), (windowSize // 2)):
            for y in range(-(windowSize // 2), (windowSize // 2)):
                cc_total += int(left[row + x, col + y] * int(right[row + x, col + y - offset]))

        cc_mag = 0
        for x in range(-(windowSize // 2), (windowSize // 2)):
            for y in range(-(windowSize // 2), (windowSize // 2)):
                cc_mag += (int(int(left[row + x, col + y] **2))+(int(right[row + x, col + y - offset]))**2)
        cc_mag += 10 ** -8
        return np.round(cc_total / cc_mag, 2)

    def getDepthMap(self, left, right, windowSize, maxOffset, type):
        depthArray = np.zeros_like(right)
        rows, cols = depthArray.shape
        offsetFactor = 255 / maxOffset
        for row in range((windowSize//2), rows-(windowSize//2)):
            for col in range((windowSize//2), cols - (windowSize//2)):
                bestScore = 65536
                for offset in range(maxOffset):
                    if type == 'ssd':
                        bestScore_temp = self.SSD(left, right, row, col, windowSize, offset)
                    elif type == 'cc':
                        bestScore_temp = self.cor(left, right, row, col, windowSize, offset)

                    if bestScore_temp <= bestScore:
                        bestScore = bestScore_temp
                        bestOffset = offset
                depthArray[row, col] = bestOffset * offsetFactor
        return depthArray

    def endPointError(self, depthArray, gt):
        rows, cols = depthArray.shape
        error = np.sum(np.abs(depthArray - gt)) / (rows * cols)
        return error

    def errorRate(self, depthArray, gt):
        rows, cols = depthArray.shape
        temp = np.abs(depthArray - gt)
        temp = np.where(temp > 3, 1, 0)
        error = (np.sum(temp) / (rows * cols)) * 100
        return error

    def stereoMatch (self, left_filename, right_filename, gt_filename):
        left_img = Image.open(left_filename).convert('L')
        right_img = Image.open(right_filename).convert('L')
        left = np.asarray(left_img)
        right = np.asarray(right_img)

        # Ground truth disparity map for performance evaluation
        gt_img = Image.open(gt_filename).convert('L')
        gt = np.asarray(gt_img)

        # Resize the images if they are too large by a factor of 1/2
        n_rows, n_cols = left.shape
        if n_rows>500 or n_cols>1000:
            print ("Image size is: ", left.shape, ". Resizing the images to 0.5 times the original size.")
            left = self.resizeTemplate(left_img, 0.45)
            right = self.resizeTemplate(right_img, 0.45)
            gt = self.resizeTemplate(gt_img, 0.45)

        # Get depth map using SSD
        print ("SSD")
        depth_arr_ssd = self.getDepthMap(left, right, windowSize=3, maxOffset=30, type = "ssd")
        imageio.imwrite("output_ssd.png", depth_arr_ssd)


        epr = self.endPointError(depth_arr_ssd, gt)
        er = self.errorRate(depth_arr_ssd, gt)
        print("The End Point Error for the System is", epr)
        print("The Error Rate for the System is", er)

        print ("Cross-Correlation")
        depth_arr_cc = self.getDepthMap(left, right, windowSize=3, maxOffset=30, type="cc")
        imageio.imwrite("output_cc.png", depth_arr_cc)

        epr = self.endPointError(depth_arr_cc, gt)
        er = self.errorRate(depth_arr_cc, gt)
        print("The End Point Error for the System is", epr)
        print("The Error Rate for the System is", er)

if __name__ == "__main__":
    if len(sys.argv)==4:
        (left_filename, right_filename, gt_filename) = sys.argv[1:]
    else:
        raise Exception("Program requires 3 arguments: left image file, right image file, ground truth file.")
    stereoMatching().stereoMatch(left_filename, right_filename, gt_filename)