"""
AI by Arthur, Sebastian and Jonathan in the Seekers 1vs1 LSGM Tournament 2023; 2nd place
"""

from seekers import *

__color__ = (255, 150, 12)

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    """This function gets called every tick the game processes.
    Only the target and the magnet state of the seekers you return affect the game."""

    for camp in camps:
        if camp != own_camp:
            other_camp = camp
            break

    own_seekers[0].target = other_camp.position
    
    for g in goals:
        if world.torus_distance(g.position, other_camp.position) < camps[0].height + 40:
            own_seekers[0].target = world.nearest_goal(other_camp.position, goals).position

    seekers_used = 1
    for o in other_seekers:
        if own_camp.contains(o.target):
            own_seekers[1].magnet.disable()
            own_seekers[1].target = o.position
            seekers_used = 2
            break

    tor = []
    tor_dist = 15
    tor.append(own_camp.position)
    tor.append(Vector(own_camp.position.x + tor_dist, own_camp.position.y))
    tor.append(Vector(own_camp.position.x - tor_dist, own_camp.position.y))
    tor.append(Vector(own_camp.position.x, own_camp.position.y + tor_dist))
    tor.append(Vector(own_camp.position.x, own_camp.position.y - tor_dist))

    for i in range(seekers_used, len(own_seekers)):
        goal_index = i
        dist = world.torus_distance(own_seekers[i].position, goals[goal_index].position)
        if dist < 38:
            own_seekers[i].magnet.set_attractive()
            #own_seekers[i].target = tor[world.index_of_nearest(own_seekers[goal_index].position, tor)]
            own_seekers[i].target = own_camp.position
        else:
            own_seekers[i].target = goals[goal_index].position
            if dist > 90:
                own_seekers[i].magnet.disable()
            else:
                own_seekers[i].magnet.set_attractive()
            
        if world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_seekers).position) < 10:
            own_seekers[i].magnet.disable()
        
    return own_seekers
