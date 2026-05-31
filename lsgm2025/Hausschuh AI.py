from seekers import *
import math

__color__ = (0, 200, 255)  # Cyan

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker],
           goals: list[Goal], other_players: list[Player], own_camp: Camp,
           camps: list[Camp], world: World, passed_time: float):

    if not own_seekers:
        return []

    camp_center = (own_camp.top_left + own_camp.bottom_right) * 0.5
    used_goals = []

    # === Rammbock (Seeker 0) ===
    rammbock = own_seekers[0]
    target_enemy = None
    # Suche Gegner mit aktivem Magnet (vermutlich Goalträger)
    for enemy in other_seekers:
        if enemy.magnet != 0 and enemy.disabled_counter == 0:
            target_enemy = enemy
            break

    if target_enemy:
        dir_to_enemy = world.torus_direction(rammbock.position, target_enemy.position)
        rammbock.target = rammbock.position + dir_to_enemy
    else:
        # Patrouilliere gegnerisches Camp
        if other_players and other_players[0].camp:
            enemy_camp_center = (other_players[0].camp.top_left + other_players[0].camp.bottom_right) * 0.5
            dir_to_camp = world.torus_direction(rammbock.position, enemy_camp_center)
            rammbock.target = rammbock.position + dir_to_camp
        else:
            rammbock.target = world.middle()
    rammbock.magnet = 0  # kein Magnet – nur rammen

    # === Punktesammler (Seeker 1-4) ===
    for seeker in own_seekers[1:]:
        # Finde nächstes unbenutztes Goal
        best_goal = None
        best_dist = float("inf")
        for g in goals:
            if g in used_goals:
                continue
            dist = world.torus_distance(seeker.position, g.position)
            if dist < best_dist:
                best_dist = dist
                best_goal = g

        if not best_goal:
            seeker.target = world.middle()
            seeker.set_magnet_disabled()
            continue

        used_goals.append(best_goal)

        # Richtungsvektoren
        to_goal = world.torus_direction(seeker.position, best_goal.position)
        to_camp = world.torus_direction(seeker.position, camp_center)
        goal_to_camp = world.torus_direction(best_goal.position, camp_center)

        # Kollisionsvermeidung: Abstand zu anderen Seekern halten
        for teammate in own_seekers:
            if teammate != seeker and world.torus_distance(seeker.position, teammate.position) < 40:
                to_goal = to_goal.rotated(math.pi / 4)  # ausweichen

        # Magnetlogik
        aligned = to_goal.normalized().dot(goal_to_camp.normalized()) > 0.6
        close_enough = world.torus_distance(seeker.position, best_goal.position) < 60

        if aligned and close_enough and seeker.disabled_counter == 0:
            seeker.magnet = -best_goal.polarity
            seeker.target = seeker.position + to_camp  # Ziel = Camp
        else:
            seeker.set_magnet_disabled()
            seeker.target = seeker.position + to_goal  # Ziel = Goal

    return own_seekers