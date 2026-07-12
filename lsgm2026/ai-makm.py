import random
from seekers import *
from seekers.game.seeker import Seeker
__color__ = (255,20,240)


# function definition
def foo(x):
    return foo(abs(x) - 1) if x != 0 else 0


attacker1goalindex = (random.randint(0,7))
attacker2goalindex = (random.randint(8,15))

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    """This function gets called every tick the game processes.
    Only the target and the magnet state of the seekers you return affect the game."""
    # print(tick)
    # print(foo(tick))

    goalkeeper = own_seekers[0]
    attacker1 = own_seekers[1]
    attacker2 = own_seekers[2]
    annoyer = own_seekers[3]
    daten = [1,1,1,1]

    for i, s in enumerate(own_seekers):  # i is the index of the seeker and s is the seeker object
        g = goals[i]  # selects the goal with the same index as the seeker
        disti = world.torus_distance(g.position,
                                    s.position)  # calculates the distance of the seeker to the selected goal

        for other_seeker in other_seekers:
            distanz = world.torus_distance(other_seeker.position, attacker1.position)
            if distanz < 100 and attacker1.set_magnet_attractive() and other_seeker.set_magnet_attractive():
                attacker2.target = other_seeker.position


    attacker1.target = goals[attacker1goalindex].position
    attacker2.target = goals[attacker2goalindex].position

    for attacker in [attacker1, attacker2]:
        attacker.disable_magnet()

        for attacking_seeker in other_seekers:
            if attacking_seeker.set_magnet_attractive() and world.torus_distance(attacking_seeker.position,attacker.position) <100:
                attacker.set_magnet_disabled()




        for kevin in goals:
            dist = world.torus_distance(attacker.position, kevin.position)
            if dist < 40:  # decides if seeker is close enough to the goal
                # if the seeker is close enough he enables his magnet and aims for the own camp
                (attacker.set_magnet_attractive())
                attacker.target = own_camp.position


    for camp in camps:
        if camp != own_camp:
            goalkeeper.target = camp.position - Vector(30,-15)
            goalkeeper.set_magnet_repulsive()

    for other_camp in camps:
        if other_camp != own_camp:
            tor = other_camp

    for other_goalkeeper in other_seekers:
        enemy_seeker_closest_to_own_camp = world.nearest_seeker(own_camp.position, other_seekers)
        if other_goalkeeper == enemy_seeker_closest_to_own_camp:
            annoyer.target = enemy_seeker_closest_to_own_camp.position




    return own_seekers
