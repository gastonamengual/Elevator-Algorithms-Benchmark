'''
Parameters

This module provides the parameters for the Elevator Simulation 
'''

__version__ = "0.3"

#-------------------------------------------------------------------------#

def get_parameters():
  
  parameters = {
    'elevator_capacity' : 6,
    'elevator_doors_time' : 3,
    'elevator_floor_time' : 5,
    'elevator_person_time' : 1,
    'num_floors' : 6,
  }

  return parameters