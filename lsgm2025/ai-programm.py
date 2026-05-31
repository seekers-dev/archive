
from seekers import *
from seekers.debug_drawing import *

color__ = (255, 255, 0)

# function definition
def foo(x):
    return foo(abs(x) - 1) if x != 0 else 0


def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    """This function gets called every tick the game processes.
    Only the target and the magnet state of the seekers you return affect the game."""
    # print(tick)
    # print(foo(tick))

    # draw_text(str(passed_time), world.middle())

    for i, s in enumerate(own_seekers):  # i is the index of the seeker and s is the seeker object
        gs=world.nearest_seeker(s.position, other_seekers)
        g = goals[i]  # selects the goal with the same index as the seeker
        dist = world.torus_distance(g.position,
                                    s.position)  # calculates the distance of the seeker to the selected goal
        # draws a line from the seekers position to the goal position
        # draw_line(s.position, g.position)
        gdist=world.torus_distance(gs.position,s.position)
        #if i==0:
        #  s.target=other_camp.position()
        if dist<40:  # decides if seeker is close enough to the g oal
            # if the seeker is close enough he enables his magnet and aims for the own camp
            # this is done by setting the magnet to the opposite polarity of the goal
            s.magnet = -g.polarity
            
    		
				
            # aim for own camp by setting the seeker target
            s.target = own_camp.position
        else:
            # otherwise it disables its magnet and aims for the goal
            s.set_magnet_disabled()
            s.target = g.position
    #s=own_seekers[1]
    #s.target=camps[0].position
    #world.nearest_goal(s.position, goals)
    #s.magnet = -g.polarity
		#gs=world.nearest_seeker(s.position, other_seekers)
        #if gdist <28:
         #    s.set_magnet_disabled()
    gdist=world.torus_distance(gs.position,s.position)
    own_seekers[0].target=world.nearest_seeker(s.position,other_seekers).position
    own_seekers[0].set_magnet_disabled()
    return own_seekers
