"""
This bot was created by Emilian, Moritz, Aaron and Anton in the Seekers Classic LSGM Summer Camp Tournament 2024. It received the 4th place.
"""

# .\run_seekers.exe .\ai-Python_User4397152068.py .\ai-Python_User4397152068.py
from seekers import *
import random
__color__ = (201, 223, 190)
def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    for Camp in camps:
        if Camp != own_camp:
            other_camp = Camp
            break
    
#    if not own_seekers[0].is_disabled:
    own_seekers[0].target = other_camp.position
#    else:
#        own_seekers[0].target = own_camp.position
    
    
    if world.torus_distance(own_seekers[0].position, other_camp.position) < 30:
        own_seekers[0].magnet.set_repulsive()
#        print(own_seekers[0].magnet.is_on(), random.randint(1,2000))
    else:
        own_seekers[0].magnet.disable()
    
#    all_seekers.remove(own_seekers[0])
#    if world.torus_distance(own_seekers[0].position, world.nearest_seeker(own_seekers[0].position, all_seekers).position) < 21:
#        own_seekers[0].magnet.disable()
#    all_seekers.append(own_seekers[0])

    seekers_used = 1
#    for g in goals:
#        if world.torus_distance(g.position, other_camp.position) < camps[0].height + 60:
#            own_seekers[0].target = world.nearest_goal(other_camp.position, goals).position
#    
    for o in other_seekers:
        if own_camp.contains(o.target):
            own_seekers[1].magnet.disable()
            if not o.is_disabled:
                own_seekers[1].target = o.position
            else:
                own_seekers[1].target = own_seekers[1].position
            seekers_used = 2
            break


    for i in range(seekers_used, len(own_seekers)):
        goal_index = i
        Abstand = world.torus_distance(own_seekers[i].position, goals[goal_index].position)
        if Abstand < 34:
            own_seekers[i].magnet.set_attractive()
            own_seekers[i].target = own_camp.position
        else:
            own_seekers[i].target = goals[goal_index].position
            if Abstand > 40:
                own_seekers[i].magnet.disable()
            else:
                own_seekers[i].magnet.set_attractive()
            
        if world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_seekers).position) < 30:
            own_seekers[i].magnet.disable()
        else:
            own_seekers[i].magnet.set_attractive()

    return own_seekers
 
