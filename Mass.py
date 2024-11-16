import Vector as v
from math import cos

class Mass:
  def __init__(self, name, radius, mass, x_pos, y_pos, velocity, color):
    self.name=name
    self.radius=radius
    self.mass=mass
    self.pos=v.Vector(x_pos,y_pos)
    self.velocity=velocity
    self.color=color

  def get_position(self):
    return self.pos
  
  def get_mass(self):
    return self.mass
  
  def pygame_position(self):
    return (self.pos.vec[0],self.pos.vec[1])
  
  def acceleration_due_to(self,other):
    
    G=6.67*10**-11
    relative_pos = v.Vector(self.get_position()-other.get_position()) #position vector between Sun and Earthin Pixels
    relative_pos_meters = relative_pos.pixels_to_meters()
    distance = relative_pos_meters.norm()#distance between Earth and Sun in pixels
    theta = relative_pos.polar_angle()
    norm_acceleration = -G*other.get_mass()/(distance**2)
    acceleration = v.Vector(norm_acceleration*cos(theta),norm_acceleration*sin(theta))
    return acceleration