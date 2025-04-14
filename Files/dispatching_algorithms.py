'''
Policies

This module implements the dispatching algorithms used by the event Process Calls 
'''

__version__ = "0.3"

import numpy as np
from copy import copy

#-------------------------------------------------------------------------#

def apply_dispatching_algorithm(state, constants):
    
    kind = constants.dispatching_algorithm
        
    if kind == 'FIFO':
        return FIFO(state)
    
    if kind == 'IFOF':
        return IFOF(state)
    
    if kind == 'LOOK':
        return LOOK(state)
    
    if kind == 'LOOK_M':
        return LOOK_M(state)
    
    return None


### FIFO

def FIFO(state_):
    
    state = copy(state_)
    
    if not state.elevator.calls: 
        state.elevator.next_floor = None
        state.elevator.state = 'idle'
        return state.elevator
        
    state.elevator.state = 'busy'
    state.elevator.next_floor = int(state.elevator.calls[0].floor)
        
    return state.elevator

### IFOF

def IFOF(state_):
    
    state = copy(state_)
    
    if not state.elevator.calls:
        state.elevator.next_floor = None
        state.elevator.state = 'idle'
        return state.elevator
    
    outside_calls = [call for call in state.elevator.calls if call.type_ == 'outside']
    inside_calls = [call for call in state.elevator.calls if call.type_ == 'inside']
    
    state.elevator.state = 'busy'
    state.elevator.next_floor = int(inside_calls[0].floor if inside_calls else outside_calls[0].floor)
    
    return state.elevator

### LOOK

def LOOK(state_):
    
    state = copy(state_)
    
    # If there are no calls, become idle
    if not state.elevator.calls:
        state.elevator.state = 'idle'
        state.elevator.next_floor = None
        return state.elevator
        
    # If moving up, get upper calls, if any
    inside_calls = np.array([call.floor for call in state.elevator.calls if call.type_ == 'inside'])
    outside_calls = np.array([call.floor for call in state.elevator.calls if call.type_ == 'outside'])
    
    # Check outside calls in current floor. If enough space, stop in current floor
    if any(floor == state.elevator.current_floor for floor in outside_calls):
        if state.elevator.capacity - len(state.elevator.current_people):
            state.elevator.next_floor = int(state.elevator.current_floor)
            return state.elevator
    
    upper_inside_calls = inside_calls[inside_calls >= state.elevator.current_floor]
    upper_outside_calls = outside_calls[outside_calls > state.elevator.current_floor]
    upper_calls = np.append(upper_inside_calls, upper_outside_calls)
    
    # If moving up, get upper calls, if any 
    if len(upper_calls) and (state.elevator.state == 'up'):
        state.elevator.next_floor = int(np.min(upper_calls))
        return state.elevator
    
    # If no upper calls, go down and get lower calls
    state.elevator.state = 'down'
    lower_inside_calls = inside_calls[inside_calls <= state.elevator.current_floor]
    lower_outside_calls = outside_calls[outside_calls < state.elevator.current_floor]
    lower_calls = np.append(lower_inside_calls, lower_outside_calls)
    
    # If no lower calls, go up
    if not len(lower_calls):
        state.elevator.state = 'up'
        state.elevator.next_floor = np.inf
        return state.elevator
    
    # If lower calls, get the highest
    state.elevator.next_floor = int(np.max(lower_calls))
    
    return state.elevator

### LOOK-M

def LOOK_M(state_):
    
    state = copy(state_)
    
    # If there are no calls, become idle
    if not state.elevator.calls:
        state.elevator.state = 'idle'
        state.elevator.next_floor = None
        return state.elevator
        
    # If moving up, get upper inside calls, if any
    inside_calls = np.array([call.floor for call in state.elevator.calls if call.type_ == 'inside'])
    upper_inside_calls = inside_calls[inside_calls >= state.elevator.current_floor]
    if len(upper_inside_calls) and (state.elevator.state == 'up'):
        state.elevator.next_floor = int(np.min(upper_inside_calls))
        return state.elevator
    
    # Check outside calls in current floor. If enough space, stop in current floor
    outside_calls = np.array([call.floor for call in state.elevator.calls if call.type_ == 'outside'])
    if any(floor == state.elevator.current_floor for floor in outside_calls):
        if state.elevator.capacity - len(state.elevator.current_people):
            state.elevator.next_floor = int(state.elevator.current_floor)
            return state.elevator
    
    # If moving up, get upper outside calls, if any 
    upper_outside_calls = outside_calls[outside_calls > state.elevator.current_floor]
    if len(upper_outside_calls) and (state.elevator.state == 'up'):
        state.elevator.next_floor = int(np.min(upper_outside_calls))
        return state.elevator
    
    # If no upper calls, go down and get lower calls
    state.elevator.state = 'down'
    lower_inside_calls = inside_calls[inside_calls <= state.elevator.current_floor]
    lower_outside_calls = outside_calls[outside_calls < state.elevator.current_floor]
    lower_calls = np.append(lower_inside_calls, lower_outside_calls)
    
    # If no lower calls, go up
    if not len(lower_calls):
        state.elevator.state = 'up'
        state.elevator.next_floor = np.inf
        return state.elevator
    
    # If lower calls, get the highest
    state.elevator.next_floor = int(np.max(lower_calls))
    
    return state.elevator