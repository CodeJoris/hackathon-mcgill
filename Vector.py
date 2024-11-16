import numpy as np

class Vector:
  def __init__(self,x_coord,y_coord):
    self.vec = np.array([x_coord,y_coord])
    self.x_coord=x_coord
    self.y_coord=y_coord

  def norm(self):
     norm=(self.x_coord**2+self.y_coord**2)**0.5
     return norm
  
  def unit_vector(self):
    return self.vec / self.norm()