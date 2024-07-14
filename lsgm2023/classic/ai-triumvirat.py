"""
This bot was created by Jonas, Bela and Karl in the Seekers Classic LSGM Summer Camp Tournament 2023. It received the 1st place.
"""

from seekers import *
import time
import math
import copy
import time
global timee
timee = 0

Vector.norm = Vector.length

__color__ = (200, 140, 60)

def vectordiff(v1: Vector, v2: Vector) -> float:
    return abs(math.asin(v1.x)-math.asin(v2.x))


def hidden_target(s: Seeker, target: Vector, world: World) -> Vector:
    if world.torus_distance(s.position, target) < s.velocity.length():
        return target
    else:
        return s.position + world.torus_direction(s.position, target) * s.base_thrust / s.friction


def goal_priority(s: Seeker, g: Goal, world: World, own_camp: Camp, timefactor: float = 0.2) -> float:
    if g.owner is None:
        return world.torus_distance(s.position, g.position)
    else:
        return world.torus_distance(s.position, g.position) - \
            timefactor * g.scoring_time * (g.owner.name == own_camp.owner.name)


def decelerate(s: Seeker, target: Vector, world: World) -> Vector:
    if world.torus_distance(s.position, target) < 42 * s.velocity.length() - 27.3:
        return world.torus_direction(target, s.position) * 0.1 + s.position
    else:
        return target


def collision_avoidance(s: Seeker, target: Vector, world: World, collidables: list[Physical]) -> Vector:
    hidden = hidden_target(s, target, world)
    collidable_positions = list(collidable.position for collidable in collidables)
    closest = world.index_of_nearest(hidden, collidable_positions)
    if world.torus_distance(hidden, collidable_positions[closest]) < s.radius + collidables[closest].radius:
        direction = rotate(world.torus_direction(s.position, target), 3)
        return Vector(s.position.x + s.max_speed * direction.x, s.position.y + s.max_speed * direction.y)
    else:
        return hidden


def rotate(vector: Vector, angle: float) -> Vector:
    return Vector(vector.x * math.cos(angle) - vector.y * math.sin(angle),
                  vector.x * math.sin(angle) + vector.y * math.cos(angle))


def decide(seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float) -> list[Seeker]:

    t0 = time.time()
    for camp in camps:
        if not camp.id == own_camp.id:
            enemy_camp = camp

    tick = int(passed_time)

    for s in seekers:
        s.max_speed = s.base_thrust / s.friction

    seeker_radius = seekers[0].radius
    goal_radius = goals[0].radius

    targets = list(s.position for s in seekers)

    gatherers = [0, 1, 2]
    pushers = []
    collector = []
    attackram = []
    rams = [4]
    defend = [3]

    aggressive = attackram + rams + defend

    weight_magnet = 0
    weight_disabled = 0.1

    dist = 40
    goals_copy = goals.copy()
    if len(collector) > 0:
        goals_copy = []
        for i in goals:
            if not (own_camp.contains(i.position) and Vector(i.velocity.x, i.velocity.y).length() < 3) and \
                    not world.torus_distance(i.position, world.nearest_seeker(i.position, seekers).position) < dist:
                goals_copy.append(i)

    for i in gatherers:
        s = seekers[i]
        if not s.disabled():
            minimum_priority = 1e10
            minimum_index = 0
            for j, goal in enumerate(goals_copy):
                if goal_priority(s, goal, world, own_camp) < minimum_priority:
                    minimum_priority = goal_priority(s, goal, world, own_camp)
                    minimum_index = j

            goal = goals_copy[minimum_index]
            del goals_copy[minimum_index]

            collidables = all_seekers.copy()
            collidables.remove(s)

            if world.torus_distance(s.position, goal.position) < dist:
                targets[i] = own_camp.position
                s.set_magnet_attractive()
            else:
                targets[i] = goal.position
                s.disable_magnet()
        targets[i] = decelerate(s, targets[i], world)

    for i in pushers:
        s = seekers[i]
        if s.disabled():
            pass
        else:
            minimum_index = world.index_of_nearest(s.position, [g.position for g in goals_copy])
            goal = goals_copy[minimum_index]
            del goals_copy[minimum_index]
            if world.torus_distance(s.position, goal.position) < 42:
                targets[i] = rotate(world.torus_direction(s.position, goal.position),
                                    math.pi / 16 * 3) * s.max_speed + s.position
                if vectordiff(world.torus_direction(s.position, goal.position) , world.torus_direction(s.position,
                                                                                              own_camp.position)) \
                        < 0.5:
                    s.set_magnet_repulsive()
                    print("push")

            else:
                targets[i] = goal.position
                s.disable_magnet()

    for i in collector:
        s = seekers[i]
        if s.disabled():
            pass
        else:
            collidables = all_seekers.copy()
            collidables.remove(s)
            targets[i] = own_camp.position
            if own_camp.contains(s.position) and \
                    world.torus_distance(world.nearest_seeker(s.position, other_seekers).position, s.position) > 17:
                s.set_magnet_attractive()
            else:
                s.disable_magnet()

    enemy_pos = []
    prio = []
    prio2 = []
    for i in other_seekers:
        prio.append(world.torus_distance(i.position, own_camp.position) + weight_magnet * i.magnet.is_on()
                    + weight_disabled * i.disabled_counter)
        prio2.append(world.torus_distance(i.position, enemy_camp.position))
        enemy_pos.append(i.position)

    for i in rams:
        for j, enemy_seeker in enumerate(other_seekers):
            if prio[j] == min(prio):
                targets[i] = enemy_pos[j]

    for i in attackram:
        s = seekers[i]
        for j in range(len(other_seekers)):
            if prio2[j] == min(prio2):
                targets[i] = enemy_pos[j]

    for i in defend:
        s = seekers[i]
        targets[i] = enemy_camp.position
        if enemy_camp.contains(s.position):
            s.set_magnet_repulsive()
        else:
            s.disable_magnet()

    for i, s in enumerate(seekers):
        s.target = targets[i]
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

    for i, s in enumerate(seekers):
        s.target = hidden_target(s, targets[i], world)

    global timee
    timee += time.time() - t0
    return seekers
