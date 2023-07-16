"""
AI by Jonas in the Seekers FFA LSGM Tournament 2023; 2nd place
"""

from seekers import *
import math
import copy
import random

Vector.norm = Vector.length

# configs
config = {
    "gatherers": [0, 1, 2],
    "pushers": [],
    "collector": [],
    "attackram": [],
    "rams": [4],
    "defend": [3],
    "weight_magnet": 0,
    "weight_disabled": 0.25,
    "dist": 40,
    "pushing_tolerance": 5,
    "timefactor_allied": 0.2,
    "timefactor_enemy": -0.1,
    "decelerate_strength": -0.1,
    "decelerate_threshold": 20
}

def vectordiff(v1: Vector, v2: Vector) -> float:
    return abs(math.asin(v1.normalized().x)-math.asin(v2.normalized().x))


def hidden_target(s: Seeker, target: Vector, world: World) -> Vector:
    if world.torus_distance(s.position, target) < s.velocity.length():
        return target
    else:
        return s.position + world.torus_direction(s.position, target) * s.base_thrust / s.friction +\
            Vector((0.5 - random.random()) * 1, (0.5 - random.random()) * 1)


def goal_priority(s: Seeker, g: Goal, world: World, own_camp: Camp, timefactor_allied: float = config["timefactor_allied"], timefactor_enemy: float = config["timefactor_enemy"])  -> float:
    if g.owner is None:
        return world.torus_distance(s.position, g.position)
    else:
        return world.torus_distance(s.position, g.position) - \
            timefactor_allied * g.scoring_time * (g.owner.name == own_camp.owner.name) + \
            timefactor_enemy * g.scoring_time * (g.owner.name != own_camp.owner.name)


def decelerate(s: Seeker, target: Vector, world: World) -> Vector:
    if world.torus_distance(s.position + s.velocity, target) < config["decelerate_threshold"]:
        return world.torus_direction(target, s.position) * config["decelerate_strength"] + s.position
    else:
        return target


def decide(seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float) -> list[Seeker]:

    for s in seekers:
        s.max_speed = s.base_thrust / s.friction

    for goal in goals:
        goal.owned_for = goal.time_owned

    goals_copy = goals.copy()

    dist = config["dist"]

    for i, s in enumerate(seekers):
        if not s.disabled():
            goal = min(goals_copy, key=lambda g: goal_priority(s, g, world, own_camp))
            goals_copy.remove(goal)

            if world.torus_distance(s.position, goal.position) < dist:
                s.target = own_camp.position
                s.set_magnet_attractive()
            else:
                s.target = goal.position
                s.disable_magnet()
        s.target = decelerate(s, s.target, world)

    if own_camp.contains(world.nearest_seeker(own_camp.position, other_seekers).position):
        seekers[0].target = world.nearest_seeker(own_camp.position, other_seekers).position

        # collision avoidance
        other_seekers_copy = copy.deepcopy(other_seekers)
        own_seekers_copy = copy.deepcopy(seekers)
        all_seekers_copy = other_seekers_copy + own_seekers_copy
        for i in all_seekers_copy:
            i.move(world)

        for i, s in enumerate(own_seekers_copy):
            for j, t in enumerate(own_seekers_copy):
                if world.torus_distance(s.position, t.position) < s.radius + t.radius and \
                        not seekers[j].magnet.is_on() and \
                        not j == i:
                    seekers[i].set_magnet_attractive()

            nearest_enemy = world.index_of_nearest(s.position, list(x.position for x in other_seekers_copy))
            if world.torus_distance(s.position, other_seekers_copy[nearest_enemy].position) < \
                    s.radius + other_seekers_copy[nearest_enemy].radius:
                seekers[i].disable_magnet()


        # target hiding and pushing
        for i, s in enumerate(seekers):
            s.target = hidden_target(s, s.target, world)

    return seekers
