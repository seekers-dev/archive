from seekers import *
# python ./examples/ai-demo.py
# python -m examples.ai-demo
# examples/ai-decide.py examples/ai-decide.py
# python run_seekers.py examples/ai-x=x+1_1vs1.py examples/Tests/ai2.py --nogrpc --debug --nokill

__color__ = (12, 242, 231)

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):

    # Gegner Camp falls gleicher Bot gegeneinander
    other_camp=other_players[0].camp

    # Blocker
    blocker = own_seekers[0]
    blocker.target = other_camp.position
    blocker.magnet.disable()
    for os in other_seekers:
        if os.target == blocker.position and not os.magnet.is_on(): blocker.magnet.disable()
        elif world.torus_distance(blocker.position, other_camp.position) < own_camp.height: blocker.magnet.set_repulsive()
        else: blocker.magnet.disable()

    # Defense
    defense = own_seekers[1]
    defense.magnet.disable()
    for os in other_seekers:
        if (os.target.x >= own_camp.top_left.x) and (os.target.x <= own_camp.bottom_right.x) and (os.target.y >= own_camp.top_left.y) and (os.target.y <= own_camp.bottom_right.y):
            defense.target = os.position    
    
    # Rammbock
    rammbock = own_seekers[2]
    rammbock.magnet.disable()
    os_distance_list = []
    for os_n in range(len(other_seekers)):
        os_distance_list.append((world.torus_distance(rammbock.position, other_seekers[os_n].position), os_n))
    os_distance_list.sort()
    for i in range(len(other_seekers)):
        if other_seekers[os_distance_list[i][1]].magnet.is_on() == True:
            rammbock.target = other_seekers[os_distance_list[i][1]].position
            break

    # Goaler
    n = 4 # Range ab welcher Magnet bei Goaler eingeschalten wird
    camp_zone = [
        Vector(own_camp.position.x-own_camp.width/4, own_camp.position.y-own_camp.width/4),
        Vector(own_camp.position.x+own_camp.width/4, own_camp.position.y-own_camp.width/4),
        Vector(own_camp.position.x-own_camp.width/4, own_camp.position.y+own_camp.width/4),
        Vector(own_camp.position.x+own_camp.width/4, own_camp.position.y+own_camp.width/4)
    ]
    camp_zone_target = [
        Vector(own_camp.position.x-own_camp.width/8, own_camp.position.y-own_camp.width/8),
        Vector(own_camp.position.x+own_camp.width/8, own_camp.position.y-own_camp.width/8),
        Vector(own_camp.position.x-own_camp.width/8, own_camp.position.y+own_camp.width/8),
        Vector(own_camp.position.x+own_camp.width/8, own_camp.position.y+own_camp.width/8)
    ]
    for i in [3, 4]:
        goaler = own_seekers[i]
        distance = world.torus_distance(goaler.position, world.nearest_goal(goaler.position, goals).position)
        if world.torus_distance(goaler.position, camp_zone[world.index_of_nearest(goaler.position, camp_zone)]) <= own_camp.width and goaler.magnet.is_on == True and distance >= own_camp.width*2:
            goaler.magnet.disable()
        elif distance <= (goaler.radius + goals[0].radius) * n:
            goaler.magnet.set_attractive()
            goaler.target = camp_zone_target[world.index_of_nearest(goaler.position, camp_zone_target)] # own_camp.position, camp_zone[world.index_of_nearest(goaler.position, camp_zone)]
        else:
            goaler.magnet.disable()
            goaler.target = world.nearest_goal(goaler.position, goals).position

    # All (quasi)
    for s in own_seekers:
        if world.torus_distance(s.position, world.nearest_seeker(s.position, other_seekers).position) <= own_seekers[0].radius + 20:
            s.magnet.disable()

    return own_seekers

#TODO
'''
1v1:
-# 1 Blocker im gegnerischen Tor (maybe mit repulsivem Magnetem an, kurz bevor Gegner aus)
-# 1 Defense (Abwehr des Tores)
-# 1 Rammbock für Gegner mit aktiven Magneten, solange Bug nicht gefixt
-# 2 Goaler (# nächster Goal, # besserer Stoppbereich) (eher unnötig: Abstimmen aufeinander)
- Abstand zu anderen Teambots (gilt nicht im Bereich des Tores)
- # Abstand von Gegnern

Multiplayer:
- Teaming von Bots mithilfe von Mustern zur Erkennung
- Ersatzprogramm
- 3 Goaler
- 1 Defense
- 1 Rammbock
- sonst alles wie gehabt
'''