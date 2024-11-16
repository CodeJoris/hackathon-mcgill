import Vector as v

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
    return (self.vec[0],self.vec[1])