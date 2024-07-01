from seekers import * # :3
from math import *
import copy
# python run_seekers.py examples/ai-x=x+1_1vs1.py .\examples\ai-versklavung.py --nogrpc --debug --nokill
__color__ = (20,240,230)

# 1 block, 2 goaler, 1 defend, 1 attack X

def angle_from_vector(v: Vector) -> float:
    if v.x > 0: return (2*pi+atan(v.y/v.x))%(2*pi)
    elif v.x < 0: return pi+atan(v.y/v.x)
    elif v.x == 0:
        if v.y > 0: return 1/2*pi
        elif v.y < 0: return 3/2*pi
        elif v.y == 0: return 0

def quadratic_point_from_angle(a: float) -> Vector:
    w = (a+pi/4)%(2*pi)
    if a == 1/4*pi: return(Vector(1,1))
    elif a == 3/4*pi: return(Vector(-1,1))
    elif a == 5/4*pi: return(Vector(-1,-1))
    elif a == 7/4*pi: return(Vector(1,-1))
    elif w>0 and w<1/2*pi:
        return Vector(1,tan(a))
    elif w>1/2*pi and w<pi:
        return Vector(-tan(a-pi/2),1)
    elif w>pi and w<3/2*pi:
        return Vector(-1,-tan(a-pi))
    elif w>3/2*pi and w<2*pi:
        return Vector(tan(a-3*pi/2),-1)

def find_g_prio_opt(l: list) -> list:
    min = [100000000000, [l[0][0],0], [l[1][0],1]]
    for a in l[0][1]:
        for b in l[1][1]:
            if a[1] != b[1] and a[0]+b[0]<min[0]:
                min = [a[0]+b[0],[l[0][0], a[1]],[l[1][0], b[1]]]
    return [min[1],min[2]]

def decelerate(s: Seeker, t: Vector, world: World) -> Vector: # TODO optimize values
    if world.torus_distance(s.position, t) < 36*s.velocity.length(): 
        return  world.torus_direction(t, s.position)*2+ s.position 
    else: return t

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal], other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    for camp in camps:
        if camp != own_camp:
            enemy_camp = camp
    t = [s.position for s in own_seekers]


    # goaler
    g_prio = []
    goaler = [3,4]
    for n in goaler:
        s = own_seekers[n]
        n_g_prio = []
        for i,g in enumerate(goals):
            if g.owner is None:
                n_g_prio.append((world.torus_distance(s.position, g.position),i))
            else:
                n_g_prio.append((world.torus_distance(s.position, g.position) - own_camp.width*0.1 * g.scoring_time**2/(100**2)* (g.owner.name == own_camp.owner.name),i))
        g_prio.append((n,n_g_prio))
    g_prio_opt = find_g_prio_opt(g_prio)
    for n in goaler:
        s = own_seekers[n]
        for e in g_prio_opt:
            if e[0]==n:
                g = goals[e[1]]
                break
        if world.torus_distance(s.position, g.position) < 42: # BIG TODO
            s.set_magnet_attractive()
            c = quadratic_point_from_angle(angle_from_vector(world.torus_direction(s.position,own_camp.position)))
            t[n] = own_camp.position
        else:
            s.disable_magnet()
            t[n] = g.position
        c = quadratic_point_from_angle(angle_from_vector(world.torus_direction(s.position,enemy_camp.position)))
        if world.torus_distance(s.position, enemy_camp.position) <= Vector(c.x*enemy_camp.width*2,c.y*enemy_camp.height*2).length():
            s.set_magnet_repulsive()
        t[n] = decelerate(s, t[n], world)
    

    # attack
    attack = [2]
    for n in attack:
        s = own_seekers[n]
        prio_attack = [[world.torus_distance(e.position, enemy_camp.position)+world.torus_distance(s.position, e.position)/4,i] for i,e in enumerate(other_seekers)]
        prio_attack.sort()
        t[n] = other_seekers[prio_attack[0][1]].position
        c = quadratic_point_from_angle(angle_from_vector(world.torus_direction(s.position,enemy_camp.position)))
        if world.torus_distance(s.position, enemy_camp.position) <= Vector(c.x*enemy_camp.width*2,c.y*enemy_camp.height*2).length():
            s.set_magnet_repulsive()
        else: s.set_magnet_disabled()


    # defend
    defend = [1]
    for n in defend:
        s = own_seekers[n]
        s.set_magnet_disabled()
        prio_defend = [[world.torus_distance(e.position, own_camp.position),i] for i,e in enumerate(other_seekers)]
        prio_defend.sort()
        t[n] = other_seekers[prio_defend[0][1]].position

    
    # block
    block = [0]
    for n in block:
        s = own_seekers[n]
        t[n] = enemy_camp.position
        if world.torus_distance(s.position, enemy_camp.position) <= Vector(c.x*enemy_camp.width*3/2,c.y*enemy_camp.height*3/2).length():
            s.set_magnet_repulsive()
        else: s.set_magnet_disabled()



    own_seekers_copy = copy.deepcopy(own_seekers)
    other_seekers_copy = copy.deepcopy(other_seekers)
    for s in own_seekers_copy+other_seekers_copy:
        s.move(world)
    for i, s in enumerate(own_seekers_copy):
        for j, os in enumerate(own_seekers_copy):
             if world.torus_distance(s.position, os.position) <= 2*s.radius and j != i and own_seekers[j].magnet.is_on():
                 own_seekers[i].disable_magnet
        nearest_enemy = world.index_of_nearest(s.position, [x.position for x in other_seekers_copy])
        if world.torus_distance(s.position, other_seekers_copy[nearest_enemy].position) <= 2*s.radius:
            own_seekers[i].disable_magnet()

    for i, s in enumerate(own_seekers):
        if world.torus_distance(s.position, t[i]) <= s.velocity.length(): s.target = t[i]
        else:
            s.target = s.position + world.torus_direction(s.position, t[i]) * (s.base_thrust/s.friction)

    return own_seekers