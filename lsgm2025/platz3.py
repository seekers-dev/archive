import seekers
from seekers import *


def collision_avoidance(all_seekers: list[Seeker], own_seekers: list[Seeker], world: World):
    for seeker in own_seekers:
        for seeker2 in all_seekers:
            if seeker.position == seeker2.position:
                continue
            elif world.torus_distance(seeker2.position, seeker2.position) < 20:
                seeker.magnet = 0
                break



def goalkeeper(gk: Seeker, goals: list[Goal], world: World, enemy_camp: Camp):
    if gk.is_disabled:
        return
    index_dist_gk = 0
    dist_gk = 1000
    gk.target = enemy_camp.position
    for i, g in enumerate(goals):
        if world.torus_distance(gk.position, g.position) < dist_gk:
            dist_gk = world.torus_distance(gk.position, g.position)
            index_dist_gk = i
    if dist_gk < 100:
        gk.magnet = goals[index_dist_gk].polarity
    else:
        gk.magnet = 0


def attacker(own_seekers: list[Seeker], goals: list[Goal], world: World, other_seekers: list[Seeker], own_camp: Camp):
    my_goals = goals
    for seeker in own_seekers:
        goal = my_goals[0]
        num = 0
        for i, g in enumerate(my_goals):
            if world.torus_distance(seeker.position, g.position) < world.torus_distance(seeker.position, goal.position):
                goal = g
                num = i
        seeker.target = goal.position
        my_goals.remove(my_goals[num])
        if world.torus_distance(seeker.position, goal.position) < 40:
            seeker.magnet = -goal.polarity
            seeker.target = own_camp.position
        # elif world.torus_distance(seeker.position, goal.position) < 80:
        #    seeker.target =
        else:
            seeker.magnet = 0


def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    # define seekers to jobs
    gk = own_seekers[0]
    attack = [own_seekers[1], own_seekers[2], own_seekers[3], own_seekers[4], own_seekers[5]]

    # get enemy_camp
    for camp in camps:
        if camp != own_camp:
            enemy_camp = camp
            break

    # start functions for seekers
    goalkeeper(gk, goals, world, enemy_camp)
    # defender(defense, other_seekers, world, goals)
    attacker(attack, goals, world, other_seekers, own_camp)
    #helper(help, goals, world, own_camp)
    #collision_avoidance(all_seekers, own_seekers, world)
    return own_seekers


'''
def helper(gk: Seeker, goals: list[Goal], world: World, own_camp: Camp):
    if gk.is_disabled:
        return
    index_dist_gk = 0
    dist_gk = 1000
    gk.target = own_camp.position
    for i, g in enumerate(goals):
        if world.torus_distance(gk.position, g.position) < dist_gk:
            dist_gk = world.torus_distance(gk.position, g.position)
            index_dist_gk = i
    if dist_gk < 100:
        gk.magnet = -goals[index_dist_gk].polarity
    else:
        gk.magnet = 0


def defender(own_seekers: list[Seeker], other_seekers: list[Seeker], world: World, goals: list[Goal]):
    # define
    pos_seekers = [s.position for s in other_seekers]
    targets = []
    for p_s in pos_seekers:
        for g in goals:
            if world.torus_distance(p_s, g.position) < 10:
                targets.append(p_s)
    velocity = [target.velocity for target in targets]
    accel = [target.acceleration for target in targets]
    not_paired = [s for s in pos_seekers if s not in targets]

    # get pos for seeker
    for i in range(len(targets)):
        if i == len(own_seekers):
            break
        own_seekers[i].target = targets[i]
    for i in range(len(not_paired)):
        if i == len(own_seekers):
            break
        own_seekers[i + len(targets)].target = not_paired[i]





'''
