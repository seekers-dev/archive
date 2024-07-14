"""
This bot was created by Johannes and Emil in the Seekers Classic LSGM Summer Camp Tournament 2024. It received the 6th place.
"""

from seekers import *

__color__ = (0, 255, 0)

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

	camps.remove(own_camp)
	camps[0].position - Vector(20, 20)
	other_camp = camps[0]
	
	if passed_time < 4000:
		own_seekers[0].target = other_camp.position
		own_seekers[0].magnet.set_repulsive()

		for i, seeker in enumerate(own_seekers[1:]):
			if world.torus_distance(seeker.position, goals[i].position) > 30:
				seeker.target = goals[i].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()	
	
	else:
		destinations = [
			Vector(other_camp.top_left.x, other_camp.bottom_right.y),
			Vector(other_camp.bottom_right.x, other_camp.top_left.y),
			other_camp.bottom_right,
			other_camp.top_left,
			other_camp.position
		]

		for i, seeker in enumerate(own_seekers):
			seeker.magnet.set_repulsive()
			seeker.target = destinations[0]

	for seeker in own_seekers:
		for other in all_seekers:
			if seeker != other:
				if world.torus_distance(seeker.position, other.position) < 30:
					if other in own_seekers:
						if other.magnet.is_on():
							seeker.magnet.disable()
						else:
							seeker.magnet.set_attractive()
					else: seeker.magnet.disable()


	return own_seekers
 