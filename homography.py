import sys
import cv2
import numpy as np
from itertools import product

class homography:
    
  def __init__(self,source_path,target_path):
      self.source_path = source_path
      self.target_path = target_path
      self.corner_index = 0     
      self.target_coords = np.array([[0, 0],[0, 0],[0, 0],[0, 0]]) #initializing the four annotated corners
            
  def read_image(self):
      self.source_image = cv2.imread(self.source_path,1)
      self.target_image = cv2.imread(self.target_path,1)
      
      self.display_image()
      
  def display_image(self):
      cv2.namedWindow('Source Image')
      cv2.imshow("Source Image",self.source_image)
      cv2.waitKey(0) & 0xFF   
      cv2.destroyAllWindows()  
      
      self.call_mouse_event()
     
  def call_mouse_event(self):
      cv2.namedWindow('Target Image')
      cv2.setMouseCallback('Target Image', self.annotate_image)    
      cv2.imshow('Target Image', self.target_image)
      k = cv2.waitKey(0) & 0xFF
      if k == 27:     
          return
      cv2.imwrite('annotated_target_image.jpg', self.annotated_image)
      cv2.destroyAllWindows() 
      
      self.form_Amatrix()
        
  def annotate_image(self, event, x, y, flags, param):
      if event == 1:
          self.target_coords[self.corner_index] = np.array([x, y])
          self.display_annotated_image()
          self.corner_index += 1
          if self.corner_index == 4:
              self.corner_index = 0           
              
  def display_annotated_image(self):
      self.annotated_image = self.target_image.copy()
      for (x, y) in self.target_coords:
          cv2.circle(self.annotated_image, (x, y), 5 , (255,0,0), -1)
      cv2.imshow('Target Image', self.annotated_image)   
        
  def form_Amatrix(self):
      height,width = self.source_image.shape[:2]
      self.source_coords = [[0,0],[width,0],[width,height],[0,height]]
            
      self.A = np.empty((0,9))
      
      for i in range(len(self.source_coords)): # here, there are 4 pairs of points
         x = self.source_coords[i][0] # x
         y = self.source_coords[i][1] # y
         
         u = self.target_coords[i][0] # x'
         v = self.target_coords[i][1] # y'
         
         Ai = np.array([[-x, -y, -1, 0, 0, 0, x*u, y*u, u],
                         [0, 0, 0, -x, -y, -1, x*v, y*v, v]])

         self.A = np.append(self.A, Ai, axis=0)
         
      self.A = np.append(self.A, np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1]]))
      self.A = np.reshape(self.A, (9, 9)) 
      
      self.estimate_homography_matrix()      
      
  def estimate_homography_matrix(self):
     u,s,vT = np.linalg.svd(self.A)
     v = np.transpose(vT)
     L = v[:,-1]
     self.homography_matrix = L.reshape(3,3)
     print(f'Homography Matrix:\n{self.homography_matrix}')
     
     self.apply_homography()
     
  def apply_homography(self):         
     # For every pixel in the source image
     for (y, x) in product(range(self.source_image.shape[0]), range(self.source_image.shape[1])):
             p = np.array([x, y, 1])
             p_cap_homogenous = np.dot(self.homography_matrix, p)
             
             new_x = p_cap_homogenous[0]/p_cap_homogenous[2]
             new_y = p_cap_homogenous[1]/p_cap_homogenous[2]
        
             self.target_image[int(new_y)][int(new_x)] = self.source_image[y][x]
             
     cv2.namedWindow('Warped Image') 
     cv2.imshow('Warped Image', self.target_image)   
     cv2.waitKey(0) & 0xFF   
     cv2.destroyAllWindows()
      
if __name__ == "__main__":
    path = 'images/'
    source_path = path + 'source/' + sys.argv[1]
    target_path = path + 'target/' + sys.argv[2]     
    obj = homography(source_path,target_path)
    obj.read_image()       