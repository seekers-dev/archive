from seekers import *
import math
import copy

# seeker[0]
COMPETITIVE_DISTANCE = 38
NORMAL_DISTANCE = 90

# defense seekers
TARGET_RADIUS = 50
REPULSIVE_RADIUS = 1.732050808 * TARGET_RADIUS
DISABLE_RADIUS = REPULSIVE_RADIUS + 50

xx = [1,1,1,1,1]
yy = [1,1,1,1,1]

__color__ = (50, 250, 112)
def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    global xx, yy
    
    # Find other Camp
    for camp in camps:
        if camp != own_camp:
            other_camp = camp
            break

    
    all_goals = list(goals)
    all_goals_score = [0 for i in range(len(all_goals))]
    #w2 = [1, 1, 0.3, 1.3]
    w2 = [1, 1, 0.8, 1.3]
    for i in range(len(all_goals)):
        all_goals_score[i] += w2[0] * world.torus_distance(own_camp.position, all_goals[i].position)
        all_goals_score[i] += w2[1] * world.torus_distance(own_seekers[0].position, all_goals[i].position)

        temp = all_goals.copy()
        temp.remove(all_goals[i])
        if world.torus_distance(all_goals[i].position, world.nearest_goal(all_goals[i].position, temp).position) < 100:
            all_goals_score[i] *= w2[2]
        all_goals_score[i] -= w2[3] * world.torus_distance(all_goals[i].position, other_camp.position)
    
    near_goal = all_goals[all_goals_score.index(min(all_goals_score))]

    # Find distance for seeker[0] to maintain to its goal
    distance = world.torus_distance(near_goal.position, world.nearest_seeker(near_goal.position, other_seekers).position)

    if distance > NORMAL_DISTANCE + 15:
        distance = NORMAL_DISTANCE
    else:
        distance = COMPETITIVE_DISTANCE
        #distance = distance - 15

    # Behaviour seeker[0]
    if world.torus_distance(own_seekers[0].position + 7*own_seekers[0].velocity, near_goal.position) < distance:
        own_seekers[0].magnet.set_attractive()
        own_seekers[0].target = own_camp.position
        if world.torus_distance(own_seekers[0].position + 7*own_seekers[0].velocity, own_camp.position) < 20:
            own_seekers[0].target = Vector(own_seekers[0].position.x - own_seekers[0].velocity.x, own_seekers[0].position.y - own_seekers[0].velocity.y)
    else:
        own_seekers[0].magnet.disable()
        w = 20 / (own_seekers[0].velocity.length() + 0.000000001)
        own_seekers[0].target = Vector(near_goal.position.x + own_seekers[0].velocity.y*w, near_goal.position.y - own_seekers[0].velocity.x*w)
    own_seekers[0].target = Vector(own_seekers[0].target.x % 768, own_seekers[0].target.y % 768)
    
    # Behaviour seeker[1]
    dists = []
    for i in other_seekers:
        dists.append(world.torus_distance(own_camp.position, i.position) + world.torus_distance(own_seekers[0].position, i.position))
    torwart = other_seekers[dists.index(min(dists))]
    if world.torus_distance(torwart.position + (torwart.velocity) * 10, own_camp.position) < 25:
        own_seekers[1].target = own_camp.position
    else:
        own_seekers[1].target = torwart.position + (torwart.velocity) * 10
        
    '''x = own_seekers[1].velocity.length() + 0.0001
    if passed_time == 10:
        own_seekers[1].target = world.nearest_seeker(own_camp.position, other_seekers).position
    own_seekers[1].target = Vector(((((world.nearest_seeker(own_camp.position, other_seekers).position.x + world.nearest_seeker(own_camp.position, other_seekers).velocity.x*world.torus_distance(own_seekers[1].position, own_seekers[1].target)/x)%768)+own_seekers[1].target.x)/2) % 768,
                                    ((((world.nearest_seeker(own_camp.position, other_seekers).position.y + world.nearest_seeker(own_camp.position, other_seekers).velocity.y*world.torus_distance(own_seekers[1].position, own_seekers[1].target)/x)%768)+own_seekers[1].target.y)/2) % 768)
    '''
    # Behaviour defense seekers
    for i in range(2,5):
        # Movement
        own_seekers[i].target = Vector(other_camp.position.x + math.sin((i - 2) * 2 / 3 * math.pi + 0 * passed_time / (TARGET_RADIUS * 4 / 9)) * TARGET_RADIUS,
                                        other_camp.position.y + math.cos((i - 2) * 2 / 3 * math.pi + 0 * passed_time / (TARGET_RADIUS * 4 / 9)) * TARGET_RADIUS)        
        # Magnet control
        nearest_goal_distance = world.torus_distance(own_seekers[i].position, world.nearest_goal(own_seekers[i].position, goals).position)
        if nearest_goal_distance < REPULSIVE_RADIUS and world.torus_distance(own_seekers[i].position, own_seekers[i].target) < 30:
            own_seekers[i].magnet.set_repulsive()
        elif nearest_goal_distance > DISABLE_RADIUS:
            own_seekers[i].magnet.disable()
        if world.torus_distance(own_seekers[i].position, own_seekers[i].target) > 10:
            own_seekers[i].magnet.disable()
        # braking
        if abs(own_seekers[i].velocity.x) < 0.1 and abs(own_seekers[i].velocity.y) < 0.1:
            xx[i] = own_seekers[i].position.x
            yy[i] = own_seekers[i].position.y
        if 5 * world.torus_distance(own_seekers[i].position, own_seekers[i].target) < world.torus_distance(Vector(xx[i],yy[i]), own_seekers[i].target):
            own_seekers[i].target = Vector(own_seekers[i].position.x - own_seekers[i].velocity.x, own_seekers[i].position.y - own_seekers[i].velocity.y)
    
    # avoiding knockouts
    all_disabled_seekers = all_seekers.copy()
    other_activated_seekers = []
    for i in all_seekers:
        if not i.is_disabled:
            all_disabled_seekers.remove(i)
            if i in other_seekers:
                other_activated_seekers.append(i)
    
    for i in range(5):
        if other_activated_seekers:
            if world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_activated_seekers).position) < 30:
                own_seekers[i].magnet.disable()
        """
        if i == 0 and world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_seekers).position) < 25:
            own_seekers[i].target = Vector((2*own_seekers[i].position.x - world.nearest_seeker(own_seekers[i].position, other_seekers).position.x) % 768, (2*own_seekers[i].position.y - world.nearest_seeker(own_seekers[i].position, other_seekers).position.y) % 768)
        """
        if i != 1:
            alls = all_seekers.copy()
            alls.remove(own_seekers[i])
            g = world.nearest_seeker(own_seekers[i].position, alls)
            if world.torus_distance(own_seekers[i].position, g.position) > world.torus_distance(own_seekers[i].position + own_seekers[i].velocity, g.position + g.velocity):
                if world.torus_distance(own_seekers[i].position, g.position) < 20 + 20*g.velocity.length():
                    own_seekers[i].target = Vector((2*own_seekers[i].position.x - g.position.x) % 768, (2*own_seekers[i].position.y - g.position.y) % 768)
                    #own_seekers[i].target = Vector((own_seekers[i].position.x - own_seekers[i].position.y + g.position.y) % 768, (own_seekers[i].position.y + own_seekers[i].position.x - g.position.x) % 768)
        """
        if i != (0 or 1) and (world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position) < 25) and not own_seekers[i].is_disabled:
            own_seekers[i].target = Vector((2*own_seekers[i].position.x - world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position.x) % 768, (2*own_seekers[i].position.y - world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position.y) % 768)
        """
    return own_seekers
