print ("wir  sind seeger")

a = 2
b = 5
print (a+b, a-b, a*b, a/b)


zahlen = [1, 2, 3]
erste = zahlen [0]
zweite = zahlen [1]
dritte = zahlen [2] 

print (erste, zweite, dritte)

for zahl in zahlen:
  if zahl == 2:
    print ("Zahl ist größer")
  else:
    print ("zahl kleiner")
    


for seeker in own_seekers:
		if world.torus_distance(seeker.position, goals[0].position) > 40:
			seeker.target = goals[0].position
			seeker.magnet.disable()
		else:
			seeker.target = own_camp.position
			seeker.magnet.set_attractive()

















from seekers import *

__color__ = (200, 140, 60)

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

	




	camps.remove(own_camp)
	camps[0].position - Vector(20, 20)
	
	if passed_time > 4000:
	
		for own_seekers[0] in own_seekers:
			if world.torus_distance(seeker.position, goals[0].position) > 40:
				seeker.target = goals[0].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()

		for own_seekers[1] in own_seekers:
			if world.torus_distance(seeker.position, goals[1].position) > 40:
				seeker.target = goals[1].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()
	
		for own_seekers[2] in own_seekers:
			if world.torus_distance(seeker.position, goals[2].position) > 40:
				seeker.target = goals[2].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()
		
		for own_seekers[3] in own_seekers:
			if world.torus_distance(seeker.position, goals[3].position) > 40:
				seeker.target = goals[3].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()
	
		for own_seekers[4] in own_seekers:
			if world.torus_distance(seeker.position, goals[4].position) > 40:
				seeker.target = goals[4].position
				seeker.magnet.disable()
			else:
				seeker.target = own_camp.position
				seeker.magnet.set_attractive()
		
	


	else:
		for own_seekers[0] in own_seekers:
			magnet.set_repulsive 
			own_seeker[0].target = property bottom_left: other_camp.position

		for own_seekers[1] in own_seekers:
			magnet.set_repulsive 
			own_seeker[1].target = property top_right: other_camp.position
	
		for own_seekers[2] in own_seekers:
			magnet.set_repulsive 
			own_seeker[2].target = property bottom_right: other_camp.position

		for own_seekers[3] in own_seekers:
			magnet.set_repulsive 
			own_seeker[3].target = property top_left: other_camp.position

		for own_seekers[4] in own_seekers:
			magnet.set_repulsive
        		own_seeker[4].target = other_camp.position



	for seeker in own_seekers:
		for other in all_seekers:
			if seeker != other:
				if world.torus_distance(seeker.position, goals[0].position) > 40:
					if other in own_seekers:
						if other.magnet.is_on():
							seeker.magnet.disable()

						else:
							seeker.magnet.set_attractive()


		return own_seekers
 
