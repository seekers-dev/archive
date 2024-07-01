from seekers import *

__color__ = (94, 74, 22)

search = True

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: int):
   
	global search

	for c in camps:
		if c != own_camp:
			other_camp = c
	
	
	radius = 25
	current_goal = world.nearest_goal(own_seekers[0].position, goals)
	
	if world.torus_distance(own_seekers[0].position, current_goal.position) < radius:
		own_seekers[0].magnet.set_attractive()
		target = own_camp.position

	else:
		own_seekers[0].magnet.disable()
		target = current_goal.position
		

	mr = 100
	td = 30
	
	own_seekers[1].target = other_camp.position + Vector(td, td)
	if world.torus_distance(world.nearest_goal(own_seekers[1].position, goals).position, own_seekers[1].position) < mr:
		own_seekers[1].magnet.set_repulsive()
	else:
		own_seekers[1].magnet.disable()

	
	own_seekers[2].magnet.disable()
	own_seekers[2].target = other_camp.position + Vector(-td, td)
	if world.torus_distance(world.nearest_goal(own_seekers[2].position, goals).position, own_seekers[2].position) < mr:
		own_seekers[2].magnet.set_repulsive()
	else:
		own_seekers[2].magnet.disable()

	
	own_seekers[3].magnet.disable()
	own_seekers[3].target = other_camp.position + Vector(-td, -td)
	if world.torus_distance(world.nearest_goal(own_seekers[3].position, goals).position, own_seekers[3].position) < mr:
		own_seekers[3].magnet.set_repulsive()
	else:
		own_seekers[3].magnet.disable() 

	own_seekers[4].magnet.disable()
	own_seekers[4].target = other_camp.position + Vector(td, -td)
	if world.torus_distance(world.nearest_goal(own_seekers[4].position, goals).position, own_seekers[4].position) < mr:
		own_seekers[4].magnet.set_repulsive()
	else:
		own_seekers[4].magnet.disable()


	return own_seekers