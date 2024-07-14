"""
This bot was created by Maurice, Alexa, Lilia and Sirja in the Seekers Chaos LSGM Summer Camp Tournament 2023. It received the 1st place.
"""

from seekers import *


def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

    for s in own_seekers:   
        if passed_time < 20:
            s.target = Vector(42, 42) 
        elif passed_time > 20:
            camp = own_camp
            camp_zone = [
                Vector(camp.position.x-camp.width/8, camp.position.y-camp.width/8),
                Vector(camp.position.x+camp.width/8, camp.position.y-camp.width/8),
                Vector(camp.position.x-camp.width/8, camp.position.y+camp.width/8),
                Vector(camp.position.x+camp.width/8, camp.position.y+camp.width/8)
            ]
            distance = world.torus_distance(s.position, world.nearest_goal(s.position, goals).position)
            if distance <= (s.radius + goals[0].radius) * 4:
                s.magnet.set_attractive()
                s.target = camp_zone[world.index_of_nearest(s.position, camp_zone)]
            else:
                s.magnet.disable()
                s.target = world.nearest_goal(s.position, goals).position

    return own_seekers
