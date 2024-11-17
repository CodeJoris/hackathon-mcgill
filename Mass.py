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

class Mass(pygame.sprite.Sprite):
  def __init__(self, name, radius, mass, x_pos, y_pos, velocity, color):
    super().__init__()  # Call the Sprite initializer

    self.name = name
    self.radius = radius
    self.mass = mass
    self.pos = np.array([x_pos, y_pos])
    self.velocity = np.array([velocity[0], velocity[1]], dtype=np.float64)
    self.color = color
    self.originalData = (radius, mass, self.pos.copy(), self.velocity.copy())
    self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

    # Set the rect attribute of the sprite
    self.rect = self.image.get_rect(center=self.pygame_position())

  def restart(self):

    self.pos = self.originalData[2].copy()
    self.velocity = self.originalData[3].copy()
    # Recreate the image surface with the new color (if necessary)
    self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
    # Update the rect to reflect the new image size and position
    self.rect = self.image.get_rect(center=self.pygame_position())

  def get_position(self):
    '''return np.array'''
    return self.pos

  def get_mass(self):
    return self.mass

  def set_mass(self, newMass):
    self.mass = newMass
    return

  def get_velocity(self):
     return self.velocity

  def norm_velocity(self):
     return norm(self.velocity)

  def pygame_position(self):
    return (self.pos[0],self.pos[1])
  
  def apply_custom_acceleration(self,a):
    self.velocity += a

  def update(self):
    '''Update the position of the object based on velocity'''
    self.pos += self.velocity
    self.rect.center = self.pygame_position()

  def acceleration_due_to(self,other):
    ''' (Mass, Mass) -> np.array

    all the physics of the project is here tbh'''
    G=6.67*10**-11
    relative_pos = self.get_position() - other.get_position() #position vector between Sun and Earthin Pixels
    direction = unit_vector(relative_pos)

    relative_pos_meters = pixels_to_meters(relative_pos)
    distance = norm(relative_pos_meters)#distance between Earth and Sun in pixels
    theta = polar_angle(relative_pos)

    norm_acceleration = -G*other.get_mass()/(distance**2)
    acceleration = norm_acceleration * direction
    return acceleration


  def apply_acceleration_due_to(self,other):
      '''name says it all'''
      self.velocity += self.acceleration_due_to(other)

  def draw(self, screen):
    '''Draw the circle to the screen (handled by sprite's image and rect)'''
    screen.blit(self.image, self.rect)
