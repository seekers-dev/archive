from seekers import *
from seekers.debug_drawing import *
import math

__color__ = (255, 0, 0)

#def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
 #              other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

         #own_seekers[0].target = goals[0].position #

         #entfernung = world.torus_distance(own_seekers[0].position, goals[0].position)

         #schranke = 30

         #print("Entfernung", entfernung)

         #own_seekers[1].target = world.middle()

        #if entfernung < schranke:

    #return own_seekers

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

    other_camp = other_players[0].camp

    cx ,cy = other_camp.position

    if not hasattr(own_seekers[0],'orbit_angle'):
        own_seekers[0].orbit_angle = 0

    own_seekers[0].orbit_angle += 0.05

    radius = 80

    tx = cx + radius * math.cos(own_seekers[0].orbit_angle)
    ty = cy + radius * math.sin(own_seekers[0].orbit_angle)

    goals[0].position = Vector(tx, ty)
    #own_seekers[0].target = goals[0]

    #    for i in range(1, len(own_seekers)):
    #    goals[i] = own_camp
    #    own_seekers[i].target = goals[i].position
    #    print(goals[i].position)
    #    print(type(goals[i].position))

    for i, s in enumerate(own_seekers):  # i is the index of the seeker and s is the seeker object
        g = goals[i]  # selects the goal with the same index as the seeker
        dist = world.torus_distance(g.position,
                                    s.position)  # calculates the distance of the seeker to the selected goal
        # draws a line from the seekers position to the goal position
        draw_line(s.position, g.position)

        if dist < 40:  # decides if seeker is close enough to the goal
            # if the seeker is close enough he enables his magnet and aims for the own camp
            # this is done by setting the magnet to the opposite polarity of the goal
            s.magnet = -g.polarity

            # aim for own camp by setting the seeker target
            s.target = own_camp.position
        else:
            # otherwise it disables its magnet and aims for the goal
            s.set_magnet_disabled()
            s.target = g.position
    return own_seekers
#nicht main