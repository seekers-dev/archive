"""
This bot was created by Jan and Karl in the Seekers Chaos LSGM Summer Camp Tournament 2023. It received the 3rd place.
"""

from seekers import *

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

    gegner_camp = None
    for camp in camps:
        if not own_camp == camp:
            gegner_camp = camp
    if gegner_camp == None:
        gegner_camp = other_players[0].camp

    seeker0 = own_seekers[0]
    seeker0.target = gegner_camp.position
    if world.torus_distance(seeker0.position, world.nearest_seeker(seeker0.position, other_seekers).position) < 25:
        seeker0.set_magnet_disabled()
    else:
        if world.torus_distance(seeker0.position, gegner_camp.position) < 16:
            seeker0.set_magnet_repulsive()
    
    seeker1 = own_seekers[1]
    seeker1.target = own_camp.position
    if world.torus_distance(seeker1.position, world.nearest_seeker(seeker1.position, other_seekers).position) < 25:
        seeker1.set_magnet_disabled()
    else:
        seeker1.set_magnet_attractive()

    for index, seeker in enumerate(own_seekers[2:]):
        goal = goals[index]
        distance = world.torus_distance(seeker.position, goal.position)
        if distance > 20:
            seeker.target = goal.position
            seeker.set_magnet_disabled()
        else:
            seeker.target = own_camp.position
            seeker.set_magnet_attractive()
    
    return own_seekers



