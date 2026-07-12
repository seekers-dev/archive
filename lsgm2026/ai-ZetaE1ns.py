from seekers import *
import math
from seekers.graphics.debug_drawing import draw_line, draw_text



# defense seekers
TARGET_RADIUS = 60
REPULSIVE_RADIUS = 1.732050808 * TARGET_RADIUS
DISABLE_RADIUS = REPULSIVE_RADIUS + 60

# general
SEEKER_RADIUS = 10

xx = [1,1,1,1,1]
yy = [1,1,1,1,1]

# Liste der vergangenen Geschwindigkeiten der Gegner
speeds = 4 * [5 * [Vector(0,0)]]

dodging_direction = ["left","left","left","left","left"]

cluster_radius = 80

class goal_cluster:
    def __init__(self, goals: list, world: World) -> None:
        self.world = world
        self.goals = goals
        self.position = self.goals[0].position
        for g in self.goals[1:]:    
            self.position += world.torus_difference(self.goals[0].position, g.position) / len(self.goals)
        self.position.x = self.position.x % 768
        self.position.y = self.position.y % 768
        self.seeker = None


    def str(self, goals):
        return [str(goals.index(g)) for g in self.goals]

def build_clusters(world, goals):
    goal_clusters = []

    # find goal clusters
    possible_clusters = []
    for i, g in enumerate(goals):
        
        # find all goals that could form a cluster around g
        near_goals = [g]
        for i in range(len(goals) - 1):
            nearest_goal = world.nearest_goal(g.position, [h for h in goals if h not in near_goals])

            if world.torus_distance(nearest_goal.position, g.position) < cluster_radius:
                near_goals.append(nearest_goal)
            else:
                break

        possible_clusters.append(near_goals)
 
    # create cluster objects
    while possible_clusters != []:
        possible_clusters = sorted(possible_clusters, key=lambda x: len(x))

        goal_clusters.append(goal_cluster(possible_clusters[0], world))
        possible_clusters = [c for c in possible_clusters[1:] \
          if set(c) & set(possible_clusters[0]) == set([])]


    for c in goal_clusters:
        for g in c.goals:   draw_line(c.position, g.position)

    return goal_clusters

def cluster_rank(goal_cluster, world, own_seekers, other_seekers, own_camp):
    camp_distace = math.e ** (-world.torus_distance(own_camp.position, goal_cluster.position) / 100)
    cluster_size = len(goal_cluster.goals)
    # penalize near enemies
    other_seeker_crowd = sum([math.e ** (-world.torus_distance(goal_cluster.position, s.position) \
      / 100) for s in other_seekers]) / len(other_seekers)
    # reward single near seeker penalize more than one near seeker
    own_seeker_crowd = sorted([math.e ** (-world.torus_distance(goal_cluster.position, s.position) \
      / 100) for s in own_seekers], reverse=True)
    own_seeker_crowd[0] = -own_seeker_crowd[0]
    own_seeker_crowd = sum(own_seeker_crowd) / len(own_seekers)

    return other_seeker_crowd * own_seeker_crowd / cluster_size / camp_distace

def projection_coefficient(vector1: Vector, vector2: Vector) -> float:
    # gibt den Koeffizienten aus, um vector2 auf vector1 zu projizieren
    return (vector1.x*vector2.x + vector1.y*vector2.y)/(vector1.x**2 + vector1.y**2)

def projected_vector(vector1: Vector, vector2: Vector) -> Vector:
    # gibt den zu vector1 parallelen Teilvektor von vector2 aus, projiziert also vector2 auf vector1
    return vector1 * projection_coefficient(vector1, vector2)

def direct_vel_cof(position1: Vector, position2: Vector, rel_vel: Vector, world: World) -> float:
    direct_vec = world.torus_difference(position1, position2)
    return projection_coefficient(direct_vec, rel_vel)

def direct_vel(position1: Vector, position2: Vector, rel_vel: Vector, world: World) -> Vector:
    direct_vec = world.torus_difference(position1, position2)
    return projected_vector(direct_vec, rel_vel)

def orth_vel_cof(position1: Vector, position2: Vector, rel_vel: Vector, world: World) -> float:
    direct_vec = world.torus_difference(position1, position2)
    orth_vec = Vector(direct_vec.y, -direct_vec.x)
    return projection_coefficient(orth_vec, rel_vel)

def orth_vel(position1: Vector, position2: Vector, rel_vel: Vector, world: World) -> Vector:
    direct_vec = world.torus_difference(position1, position2)
    orth_vec = Vector(direct_vec.y, -direct_vec.x)
    return projected_vector(orth_vec, rel_vel)

def danger(own_seeker: Seeker, seeker2: Seeker, own_seekers: list[Seeker], world: World) -> float:
    puffer = world.torus_distance(own_seeker.position, seeker2.position) - 2*SEEKER_RADIUS
    if seeker2 in own_seekers:
        if puffer <= 5:
            return 200 - puffer
        else:
            rel_vel = own_seeker.velocity - seeker2.velocity
    else:
        if puffer <= 5:
            return 300 - puffer
        """elif puffer <= 30:
            return 100 - puffer
        else:"""
        rel_vel = own_seeker.velocity - (seeker2.velocity + world.torus_direction(seeker2.position, own_seeker.position)*seeker2.max_speed)/2
    return 100*direct_vel(own_seeker.position, seeker2.position, rel_vel, world).length()/puffer



__color__ = (100, 250, 200)
def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    global xx, yy, dodging_direction, SEEKER_RADIUS, speeds
    # Find other Camp
    for camp in camps:
        if camp != own_camp:
            other_camp = camp
            break

    if passed_time == 0:
        SEEKER_RADIUS = all_seekers[0].radius
        for i in range(4):
            for j in range(5):
                speeds[i][j] = Vector(0, 0)

    # set speeds and speeds_index
    speeds_index = passed_time % 5
    for i in range(4):
        speeds[i][speeds_index] = other_seekers[i].velocity

    sucher = [own_seekers[2], own_seekers[3]]

    goal_clusters = build_clusters(world, goals)
    goal_clusters = sorted(goal_clusters, \
        key=lambda x: cluster_rank(x, world, sucher, other_seekers, own_camp))

    taken_seekers = []
    # let seekers keep their cluster
    for s in sucher:
        near_cluster = world.nearest_goal(s.position, goal_clusters)
        if world.torus_distance(s.position, near_cluster.position) < 90:
            near_cluster.seeker = s
            taken_seekers.append(s)

    # give remaining seekers a cluster
    for i, c in enumerate(goal_clusters): 
        draw_text(str(i), c.position)
        if len(taken_seekers) < len(sucher):    c.seeker = world.nearest_seeker(c.position, \
        [s for s in sucher if s not in taken_seekers])
        taken_seekers.append(c.seeker)

    # BASIC MOVEMENT
    for i, s in enumerate(sucher):
        s_cluster = [c for c in goal_clusters if c.seeker == s]
        if len(s_cluster) != 0: s_cluster = s_cluster[0]
        else:                   continue

        if world.torus_distance(s_cluster.position, s.position) < 90:
            s.magnet.set_attractive()
            s.target = own_camp.position
            if world.torus_distance(s.position + 7*s.velocity, own_camp.position) < 20:
                s.target = Vector(s.position.x - s.velocity.x, s.position.y - s.velocity.y)

        else:
            s.magnet.disable()
            s.target = s_cluster.position
    
    # Behaviour seeker[1]
    rammability = []
    for i in other_seekers:
        rammability.append(
            world.torus_distance(own_camp.position, i.position) + world.torus_distance(own_seekers[0].position, i.position)
            + 0.01/(0.01 + direct_vel_cof(own_seekers[1].position, i.position, (own_seekers[1].velocity + world.torus_direction(own_seekers[1].position, i.position)*own_seekers[1].max_speed)/2 - i.velocity, world))
            )

    torwart_index = rammability.index(min(rammability))
    torwart = other_seekers[torwart_index]
    
    avg_acc = Vector(
                sum((speeds[torwart_index][(speeds_index - i)%5].x - speeds[torwart_index][(speeds_index - i - 1)%5].x) * 0.8 ** i for i in range(5)),
                sum((speeds[torwart_index][(speeds_index - i)%5].y - speeds[torwart_index][(speeds_index - i - 1)%5].y) * 0.8 ** i for i in range(5))
                ) / sum(0.8 ** i for i in range(5))
    time_distance = 20
    calc_speed = torwart.velocity
    own_seekers[1].target = torwart.position
    for i in range(time_distance):
        calc_speed += avg_acc
        if calc_speed.length() > torwart.max_speed:
            calc_speed = calc_speed.normalized() * torwart.max_speed
        own_seekers[1].target += calc_speed
    own_seekers[1].target -= 40*orth_vel(own_seekers[1].position, torwart.position, own_seekers[1].velocity - torwart.velocity, world)

    # Behaviour defense seekers
    for i in [0]:
        # Movement
        own_seekers[i].target = other_camp.position
        # Magnet control
        nearest_goal_distance = world.torus_distance(own_seekers[i].position, world.nearest_goal(own_seekers[i].position, goals).position)
        if nearest_goal_distance < REPULSIVE_RADIUS and world.torus_distance(own_seekers[i].position, own_seekers[i].target) < 100:
            own_seekers[i].magnet.set_repulsive()
        elif nearest_goal_distance > DISABLE_RADIUS:
            own_seekers[i].magnet.disable()
        if world.torus_distance(own_seekers[i].position, own_seekers[i].target) >= 100:
            own_seekers[i].magnet.disable()
        # braking
        if abs(own_seekers[i].velocity.x) < 0.1 and abs(own_seekers[i].velocity.y) < 0.1:
            xx[i] = own_seekers[i].position.x
            yy[i] = own_seekers[i].position.y
        if 6 * world.torus_distance(own_seekers[i].position, own_seekers[i].target) < world.torus_distance(Vector(xx[i],yy[i]), own_seekers[i].target):
            own_seekers[i].target = Vector(own_seekers[i].position.x - own_seekers[i].velocity.x, own_seekers[i].position.y - own_seekers[i].velocity.y)
    
    # avoiding knockouts
    all_disabled_seekers = all_seekers.copy()
    other_activated_seekers = []
    for i in all_seekers:
        if not i.is_disabled:
            all_disabled_seekers.remove(i)
            if i in other_seekers:
                other_activated_seekers.append(i)
    
    for i in range(4):
        if other_activated_seekers:
            if world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_activated_seekers).position) < 30:
                own_seekers[i].magnet.disable()

        if i not in [1,2,3]:
            alls = all_seekers.copy()
            alls.remove(own_seekers[i])
            danger_list = [danger(own_seekers[i], s, own_seekers, world) for s in alls]
            dangerous_seeker = alls[danger_list.index(max(danger_list))]
            g = dangerous_seeker
            if True:
                if max(danger_list) > 13:
                    own_seekers[i].magnet.disable()
                if max(danger_list) > 10:
                    if 0.01 < abs(orth_vel_cof(own_seekers[i].position, g.position, own_seekers[i].velocity - g.velocity, world)):
                        if 0 < orth_vel_cof(own_seekers[i].position, g.position, own_seekers[i].velocity - g.velocity, world):
                            dodging_direction[i] = "right"
                        else:
                            dodging_direction[i] = "left"

                    if dodging_direction[i] == "right":
                        a = (-0.7) * math.pi
                    else:
                        a = 0.7 * math.pi
                    p = own_seekers[i].position
                    q = g.position - p
                    own_seekers[i].target = p + Vector(q.x*math.cos(a) - q.y*math.sin(a), q.x*math.sin(a) + q.y*math.cos(a))
        if i in [2,3]: # Sucher nutzen das Ausweichen aus 2024
            alls = all_seekers.copy()
            alls.remove(own_seekers[i])
            g = world.nearest_seeker(own_seekers[i].position, alls)
            if world.torus_distance(own_seekers[i].position, g.position) > world.torus_distance(own_seekers[i].position + own_seekers[i].velocity, g.position + g.velocity):
                if world.torus_distance(own_seekers[i].position, g.position) < 20 + 20*g.velocity.length():
                    own_seekers[i].target = Vector((2*own_seekers[i].position.x - g.position.x) % 768, (2*own_seekers[i].position.y - g.position.y) % 768)

    return own_seekers
