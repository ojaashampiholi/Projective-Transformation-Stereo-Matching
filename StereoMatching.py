import numpy as np
from PIL import Image
import imageio

class stereoMatching():
    def resizeTemplate(self, template, factor):
        # factor = space/template.height
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
        # cc_total = 1
        # for x in range(-(windowSize // 2), (windowSize // 2)):
        #     for y in range(-(windowSize // 2), (windowSize // 2)):
        #         cc_total *= int(left[row + x, col + y] * int(right[row + x, col + y - offset]))
        #
        # cc_mag = 0
        # for x in range(-(windowSize // 2), (windowSize // 2)):
        #     for y in range(-(windowSize // 2), (windowSize // 2)):
        #         cc_total *= int(left[row + x, col + y] * int(right[row + x, col + y - offset]))

        num = np.sum(left[row, col:col + windowSize] * right[row, col - offset:col + windowSize - offset])
        den = np.sum(np.sqrt(np.square(left[row, col:col + windowSize]) * np.square(right[row, col - offset:col + windowSize - offset]))) + 10 ** -8
        return np.round(num / den, 2)

    def getDepthMap(self, left, right, windowSize, maxOffset, type):
        depthArray = np.zeros_like(right)
        rows, cols = depthArray.shape
        offsetFactor = 255 / maxOffset
        for row in range((windowSize//2), rows-(windowSize//2)):
            if row == (windowSize//2):
                # Viterbi Values will
                for col in range((windowSize//2), cols - (windowSize//2)):
                    bestScore = 65536
                    for offset in range(maxOffset):
                        if type == 'ssd':
                            bestScore_temp = self.SSD(left, right, row, col, windowSize, offset)
                        # elif type == 'cc':
                        #     bestScore_temp = self.cor(left, right, row, col, windowSize, offset)

                        if bestScore_temp < bestScore:
                            bestScore = bestScore_temp
                            bestOffset = offset
                    depthArray[row, col] = bestOffset * offsetFactor
            else:

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

    def stereoMatch (self):
        basepath =  "C://Users//navek\Documents//CV//a2//input_images-2//input_images//part2//"

        # Read the images
        left_filename = "1//0015_rgb_left"
        right_filename = "1//0015_rgb_right"
        left_img = Image.open(basepath+left_filename+'.png').convert('L')
        right_img = Image.open(basepath+right_filename+'.png').convert('L')
        left = np.asarray(left_img)
        right = np.asarray(right_img)

        # Also read the ground truth disparity map for performance evaluation
        gt_filename = "1//0015_gt"
        gt_img = Image.open(basepath+gt_filename+'.png').convert('L')
        gt = np.asarray(gt_img)

        # Resize the images if they are too large by a factor of 1/2
        n_rows, n_cols = left.shape
        if n_rows>500  or n_cols>1000:
            print ("Image size is: ", left.shape, ". Resizing the images to 0.5 times the original size.")
            left = self.resizeTemplate(left_img, 0.5)
            right = self.resizeTemplate(right_img, 0.5)
            gt = self.resizeTemplate(gt_img, 0.5)

        # Get depth map using SSD
        print ("SSD")
        depth_arr_ssd = self.getDepthMap(left, right, windowSize = 15, maxOffset = 7, type = "ssd")
        imageio.imwrite("output_ssd.png", depth_arr_ssd)


        epr = self.endPointError(depth_arr_ssd, gt)
        er = self.errorRate(depth_arr_ssd, gt)
        print("The End Point Error for the System is", epr)
        print("The Error Rate for the System is", er)

        print ("Cross-Correlation")
        depth_arr_cc = self.getDepthMap(left, right, windowSize=15, maxOffset=7, type="cc")
        imageio.imwrite("output_cc.png", depth_arr_cc)

        epr = self.endPointError(depth_arr_cc, gt)
        er = self.errorRate(depth_arr_cc, gt)
        print("The End Point Error for the System is", epr)
        print("The Error Rate for the System is", er)


stereoMatching().stereoMatch()