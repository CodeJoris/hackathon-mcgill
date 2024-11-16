
from math import *
import pygame
import numpy as np

def norm(array):
    norm=(array[0]**2+array[1]**2)**0.5
    return norm

def unit_vector(array):
  return array / norm(array)

def polar_angle(array):
  return atan((array[1])/array[0]) 
  
def pixels_to_meters(array):
  return array*(1.5*10**11/300)

class Mass:
  def __init__(self, name, radius, mass, x_pos, y_pos, velocity, color):
    self.name=name
    self.radius=radius
    self.mass=mass
    self.pos=np.array([x_pos,y_pos])
    self.velocity=np.array([velocity[0],velocity[1]],dtype=np.float64)
    self.color=color

  def get_position(self):
    '''return np.array'''
    return self.pos
  
  def get_mass(self):
    return self.mass
  
  def pygame_position(self):
    return (self.pos[0],self.pos[1])
  
  def acceleration_due_to(self,other):
    G=6.67*10**-11
    relative_pos = self.get_position() - other.get_position() #position vector between Sun and Earthin Pixels
    direction = unit_vector(relative_pos)

    relative_pos_meters = pixels_to_meters(relative_pos)
    distance = norm(relative_pos_meters)#distance between Earth and Sun in pixels
    theta = polar_angle(relative_pos)
    
    norm_acceleration = -G*other.get_mass()/(distance**2)
    acceleration = norm_acceleration * direction
    return acceleration

  def update_position(self):
      self.pos += self.velocity

  def apply_acceleration_due_to(self,other):

      self.velocity += self.acceleration_due_to(other)

  def draw(self, screen):
      center = (int(self.pos[0]), int(self.pos[1]))
      center = (int(center[0]),int(center[1]))
      pygame.draw.circle(screen, self.color, center, self.radius)
  
