'''
Policies

This module implements the dispatching algorithms used by the event Process Calls 
'''

__version__ = "0.3"

import numpy as np
import pandas as pd
from classes import Scenario

#-------------------------------------------------------------------------#

M = 60
H = 3600
D = 86400

def create_scenario(kind):

    if kind == 'morning_rush':
    
        distribution_parameters = [(5, 1), (np.inf, np.inf), (np.inf, np.inf), (np.inf, np.inf), (np.inf, np.inf), (np.inf, np.inf)]
        duration = 30*M
        start_datetime = pd.to_datetime('2021-05-1 08:00:00').timestamp()
        waiting_tolerance = (np.inf, np.inf)
        floor_destination_probabilities = {'0': [0.00, 0.05, 0.2375, 0.2375, 0.2375, 0.2375],
                                           '1': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '2': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '3': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '4': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '5': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],}

    elif kind == 'residential_building':
    
        distribution_parameters = [(0.5*H, 1), (1*H, 1), (1*H, 1), (1*H, 1), (1*H, 1), (1*H, 1)]
        duration = 3*H
        start_datetime = pd.to_datetime('2021-05-1 08:00:00').timestamp()
        waiting_tolerance = (np.inf, np.inf)
        floor_destination_probabilities = {'0': [0.00, 0.05, 0.2375, 0.2375, 0.2375, 0.2375],
                                           '1': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '2': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '3': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '4': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '5': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],}

    elif kind == 'lunchtime':
        
        distribution_parameters = [(20, 1), (20, 1), (10, 1), (10, 1), (10, 1), (10, 1)]
        duration = 60*M 
        start_datetime = pd.to_datetime('2021-05-1 13:00:00').timestamp()
        waiting_tolerance = (np.inf, np.inf)
        floor_destination_probabilities = {'0': [0.00, 0.05, 0.2375, 0.2375, 0.2375, 0.2375],
                                           '1': [0.05, 0.00, 0.05, 0.30, 0.30, 0.30],
                                           '2': [0.7625, 0.2375, 0.00, 0.00, 0.00, 0.00],
                                           '3': [0.50, 0.50, 0.00, 0.00, 0.00, 0.00],
                                           '4': [0.50, 0.50, 0.00, 0.00, 0.00, 0.00],
                                           '5': [0.50, 0.50, 0.00, 0.00, 0.00, 0.00],}
        
        
    elif kind == 'evening_rush':
        
        distribution_parameters = [(np.inf, np.inf), (30, 1), (25, 1), (6, 1), (5, 1), (5, 1)]
        duration = 30*M 
        start_datetime = pd.to_datetime('2021-05-1 17:00:00').timestamp()
        waiting_tolerance = (np.inf, np.inf)
        floor_destination_probabilities = {'0': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '1': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '2': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '3': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '4': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                           '5': [1.00, 0.00, 0.00, 0.00, 0.00, 0.00],}
 
        
    return Scenario(distribution_parameters = distribution_parameters,
                    duration = duration,
                    floor_destination_probabilities = floor_destination_probabilities,
                    start_datetime = start_datetime,
                    waiting_tolerance = waiting_tolerance)