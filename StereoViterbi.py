import numpy as np
import imageio
from PIL import Image
import sys

class stereoViterbi():
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

    def resizeTemplate(self, template, factor):
        temp = template.resize((int(template.width * factor), int(template.height * factor)))
        return np.asarray(temp)

    def viterbi(self, left_arr, right_arr, offset):
        n_rows, n_cols = left_arr.shape
        depth_arr = np.zeros((n_rows,n_cols), np.uint8)

        for row in range(0, n_rows):
            viterbi_vals = np.zeros((n_cols, n_cols))
            direction = np.zeros((n_cols, n_cols))

            # Update the first row and first col of viterbi table according to offset
            for i in range(0, n_cols):
                viterbi_vals[i, 0] = i * offset
                viterbi_vals[0, i] = i * offset

            # For rest of entries in the viterbi table, use the 3 neighboring values, also keep updating the direction from which minimum came
            for i in range(0, n_cols):
                for j in range(0, n_cols):
                    # We are doing a pixel to pixel difference, a 3x3 window can also be used.
                    min_diag = viterbi_vals[i - 1, j - 1] + np.abs((int(left_arr[row, i]) - int(right_arr[row, j])))
                    min_left = viterbi_vals[i - 1, j] + offset
                    min_up = viterbi_vals[i, j - 1] + offset
                    minimum = np.min((min_diag, min_left, min_up))

                    viterbi_vals[i, j] = minimum
                    if min_diag == minimum:
                        direction[i, j] = 1
                    if min_left == minimum:
                        direction[i, j] = 2
                    if min_up == minimum:
                        direction[i, j] = 3

            # Backtrack to fill depth value
            r = n_cols - 1
            c = n_cols - 1
            while ((r != 0) and (c != 0)):
                if direction[r, c] == 1:
                    depth_arr[row, r] = np.abs(r - c)*2
                    r = r - 1
                    c = c - 1
                elif direction[r, c] == 2:
                    r = r - 1
                elif direction[r, c] == 3:
                    c = c - 1
        return depth_arr

    def stereoMatching(self, left_filename, right_filename, gt_filename):
        left_image = Image.open(left_filename).convert('L')
        right_image = Image.open(right_filename).convert('L')
        gt_image = Image.open(gt_filename).convert('L')

        left_arr = np.asarray(left_image)
        right_arr = np.asarray(right_image)
        gt_arr = np.asarray(gt_image)

        # Resize the images if they are too large by a factor of 1/2
        n_rows, n_cols = left_arr.shape
        if n_rows>500 or n_cols>1000:
            resize_factor = 0.5
            print ("Image size is: ", left_arr.shape, ". Resizing the images to", resize_factor, " times the original size.")
            left_arr = self.resizeTemplate(left_image, resize_factor)
            right_arr = self.resizeTemplate(right_image, resize_factor)
            gt_arr = self.resizeTemplate(gt_image, resize_factor)


        depth_arr = self.viterbi(left_arr, right_arr, offset = 7)
        imageio.imwrite('output_viterbi.jpg', depth_arr)

        epr = self.endPointError(depth_arr, gt_arr)
        er = self.errorRate(depth_arr, gt_arr)
        print("The End Point Error using Viterbi is", epr)
        print("The Error Rate using Viterbi is", er)

if __name__ == "__main__":
    if len(sys.argv)==4:
        (left_filename, right_filename, gt_filename) = sys.argv[1:]
    else:
        raise Exception("Program requires 3 arguments: left image file, right image file, ground truth file.")
    stereoViterbi().stereoMatching(left_filename, right_filename, gt_filename)