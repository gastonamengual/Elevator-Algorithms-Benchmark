'''
Events

This module provides the events for the elevator simulation module 
'''

__version__ = "0.3"

import numpy as np
from copy import copy
from collections import namedtuple
from typing import Optional
from utilities import get_next_arrival
from dispatching_algorithms import apply_dispatching_algorithm

from classes import User, ElevatorCall

#-------------------------------------------------------------------------#

def user_arrival(state_, constants):
    
    state = copy(state_)
    
    arrival_floor = state.next_arrival_floor
    
    # Get user destination
    destination_floor = get_user_destination(state, constants, arrival_floor)
    
    # Create user
    user = User(arrive_time=state.current_event_time,
                origin=arrival_floor,
                destination=destination_floor,
                waiting_tolerance=get_user_waiting_tolerance(state),
               )
    
    # Add user to queue
    state.floors_queues[user.origin] = tuple(state.floors_queues[user.origin]) + (user,)
    
    # Set next arrival time for current floor
    next_arrival_time = np.abs(state.PRNGs_floors_arrival[arrival_floor]())
    state.events.user_arrival[arrival_floor] = state.current_event_time + next_arrival_time

    # Get floor of next arrival
    state.next_arrival_floor = get_next_arrival(state.events.user_arrival)
    
    # If user can enter, go to load and unload if not called, and disable move elevator
    if user_can_enter(state, user.origin) and state.events.load_and_unload == np.inf and state.events.enter_elevator == np.inf:
        state.events.load_and_unload = state.current_event_time
        state.events.move_elevator_one_floor = np.inf
        return state
    
    # If user cannot enter and button is not pressed, press button
    if not button_pressed(state.elevator.calls, user.origin, 'outside'):
        elevator_call = ElevatorCall(state.current_event_time, 'outside', user.origin) 
        state.elevator.calls.append(elevator_call)
    
    # If no other elevator event is programmed
    if list(vars(state.events).values())[1:] == [np.inf, np.inf, np.inf, np.inf]:
        state.events.process_calls = state.current_event_time
        
    return state

####################

def get_user_destination(state, constants, origin_floor):
    
    probabilities = constants.floor_destination_probabilities[str(origin_floor)]
    destination_floor = state.PRNG_choice(constants.floors_ids, p=probabilities)
     
    return destination_floor

####################

def get_user_waiting_tolerance(state):
    return state.PRNG_waiting_tolerance()

####################

def get_next_arrival(next_arrivals):
    
    next_arrival =  min(next_arrivals.items(), key=lambda x: x[1])

    return next_arrival[0]

####################

def user_can_enter(state, origin_floor):
    
    correct_position = state.elevator.current_floor == origin_floor
    enough_space = state.elevator.capacity - len(state.elevator.current_people)
    people_in_queue = len(state.floors_queues[state.elevator.current_floor])
    doors_open = state.elevator.doors == 'open'
    
    return correct_position and enough_space > 0 and people_in_queue > 0 and doors_open

####################

def button_pressed(calls, current_floor, kind):
    return any(call.floor == current_floor and call.type_ == kind for call in calls)


#-------------------------------------------------------------------------#


def process_calls(state_, constants):

    state = copy(state_)
    state.events.process_calls = np.inf

    state.elevator = apply_dispatching_algorithm(state, constants)
    
    if state.elevator.next_floor is None:
        return state
    
    if state.elevator.next_floor == np.inf:
        state.events.process_calls = state.current_event_time
        return state

    # If elevator on destination floor
    if state.elevator.next_floor == state.elevator.current_floor:
        state.events.load_and_unload = state.current_event_time + state.elevator.doors_time
        return state
    
    # Do not consider doors time if they are closed
    doors_time = state.elevator.doors_time * (state.elevator.doors == 'open')
    state.events.move_elevator_one_floor = state.current_event_time + doors_time

    return state


#-------------------------------------------------------------------------#


def move_elevator_one_floor(state_, constants):
    
    state = copy(state_)
    
    state.events.move_elevator_one_floor = np.inf
    
    state.elevator.doors = 'close'
    
    delta = 1 if state.elevator.next_floor > state.elevator.current_floor else -1
    
    state.elevator.current_floor = state.elevator.current_floor + delta
    
    state.events.process_calls = state.current_event_time + state.elevator.floor_time
    
    return state


#-------------------------------------------------------------------------#


def load_and_unload(state_, constants):
    
    state = copy(state_)
    
    state.events.load_and_unload = np.inf
    
    # Open Doors
    state.elevator.doors = 'open'
    
    elevator_previous_people = len(state.elevator.current_people)
    
    # Delete calls of current floor
    state.elevator.calls = [call for call in state.elevator.calls if call.floor != state.elevator.current_floor]
    
    # Users get off the elevator in destination
    people_in_elevator = []
    for person in state.elevator.current_people:
        if person.destination != state.elevator.current_floor:
            people_in_elevator.append(person)
        else:
            person.arrive_destination_time = state.current_event_time
            state.users_served.append(person)
            
    state.elevator.current_people = people_in_elevator
    
    people_unload_time = (elevator_previous_people - len(state.elevator.current_people)) * state.elevator.person_time
    
    # Delete people that have left queue
    def wait_time_excedeed(person):
        return state.current_event_time <= person.arrive_time + person.waiting_tolerance
    
    users_in_queue = state.floors_queues[state.elevator.current_floor]
    
    state.floors_queues[state.elevator.current_floor] = list(filter(wait_time_excedeed, users_in_queue))
    
    # If users can enter, go to enter elevator
    if user_can_enter(state, state.elevator.current_floor):
        state.events.enter_elevator = state.current_event_time + state.elevator.person_time
        return state
    
    # If users left in floor, add call for current floor
    if state.floors_queues[state.elevator.current_floor]:
        elevator_call = ElevatorCall(state.current_event_time, 'outside', state.elevator.current_floor) 
        state.elevator.calls.append(elevator_call)
    
    # Otherwise, process calls
    state.events.process_calls = state.current_event_time + people_unload_time
    
    return state


#-------------------------------------------------------------------------#


def enter_elevator(state_, constants):
    
    state = copy(state_)
    
    state.events.enter_elevator = np.inf
          
    # Get first user of queue and delete it from queue
    user, *rest = state.floors_queues[state.elevator.current_floor]
    state.floors_queues[state.elevator.current_floor] = rest
    user.enter_elevator_time = state.current_event_time
    
    # Add user to elevator
    state.elevator.current_people.append(user)
    
    # If not already pressed, user presses a button. Create an elevator inside call
    if not button_pressed(state.elevator.calls, user.destination, 'inside'):
        elevator_call = ElevatorCall(state.current_event_time, 'inside', user.destination)
        state.elevator.calls.append(elevator_call)
    
    # If more users can enter, repeat the event
    if user_can_enter(state, user.origin):
        state.events.enter_elevator = state.current_event_time + state.elevator.person_time
        return state
    
    # If no more users can enter and there are users left in queue, press button again
    if state.floors_queues[state.elevator.current_floor]:
        elevator_call = ElevatorCall(state.current_event_time, 'outside', state.elevator.current_floor) 
        state.elevator.calls.append(elevator_call)
    
    state.events.process_calls = state.current_event_time
    
    return state