from seekers import *
from seekers.debug_drawing import *
import copy
import math
__color__ = (40, 200, 255)

COMPETITIVE_DISTANCE = 38
NORMAL_DISTANCE = 90
WORLDSIZE = 800

verteiler = []
magnet_strength = 0

Rammbockindizes = []
Torwaerter = []

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
    global Rammbockindizes, Torwaerter
    available_goals = goals
    # find other Camp
    for camp in camps:
        if camp != own_camp:
            other_camp = camp
            break
        
    # calculate magnet strength of a seeker
    magnet_strength = lambda s: len([i for i in own_seekers if i.magnet == s.magnet]) ** -1
    #                                                          ^^^^^^^^^^
    #Attribute Error: ´Seeker´ object has no attribute ´polarity´


    # ===== possible tasks, that can be assigned to seekers =======================================
    def no_task(s):
        """do nothing"""
        pass

    def score_goal(s): #Läufer
        """find optimal goal, and bring it to the camp"""
    
        # find optimal goal
        near_goal = world.nearest_goal(s.position, goals)
        near_goal = goals[(own_seekers.index(s)+4)%6]
        
        distance = world.torus_distance(near_goal.position, world.nearest_seeker(near_goal.position, 
                   other_seekers).position)
        if distance > NORMAL_DISTANCE + 15:
            distance = NORMAL_DISTANCE
        else:
            distance = COMPETITIVE_DISTANCE
        #distance = NORMAL_DISTANCE
        """# return to camp
        if world.torus_distance(s.position + 7 * s.velocity,
            near_goal.position) < distance:
            
            s.magnet = -near_goal.polarity
            s.target = own_camp.position
            
            #if world.torus_distance(own_seekers[0].position + 7 * own_seekers[0].velocity, own_camp.position) \
            #    < 50 * magnet_strength(s):
            if world.torus_distance(s.position, own_camp.position) < 100 and world.torus_distance(s.position, own_camp.position) \
                < world.torus_distance(s.position + 5 * s.velocity, own_camp.position):
                print("Bremsen! time: ", passed_time)
                s.target = s.position - 10*s.velocity

        else:
            s.magnet = 0
            s.target = near_goal.position + Vector()"""
        #if distance == COMPETITIVE_DISTANCE:
            #print("Das ist MEIN Goal!!! time: ", passed_time)

        if world.torus_distance(s.position + 7*s.velocity, near_goal.position) < distance:
            if world.torus_distance(s.position + 7*s.velocity, near_goal.position) < 30 and not distance == COMPETITIVE_DISTANCE:
                if passed_time % 2 == own_seekers.index(s) % 2:
                    s.magnet = -near_goal.polarity
                else:
                    s.magnet = 0
            else:
                s.magnet = -near_goal.polarity
            s.target = own_camp.position - 30*s.velocity
            if world.torus_distance(s.position, own_camp.position) < 150 and world.torus_distance(s.position, own_camp.position) \
                < world.torus_distance(s.position + 50 * s.velocity, own_camp.position):
                s.target = Vector(s.position.x - 20*s.velocity.x, s.position.y - 20*s.velocity.y)
                #print("Bremsen! time: ", passed_time)
        else:
            s.magnet = 0
            w = 40 / (s.velocity.length() + 0.000000001)
            s.target = Vector(near_goal.position.x + s.velocity.y*w, near_goal.position.y -s.velocity.x*w)
        s.target = Vector(s.target.x % WORLDSIZE, s.target.y % WORLDSIZE)


            
    def ram_keeper(s): #Antitorwart
        global Rammbockindizes
        Rammbockindizes.append(own_seekers.index(s))
        """KOENNEN WIR BITTE RAMMER NENNEN"""
    
        """neutralize the opponent's goalkeeper"""
        
        goal_scorer = world.nearest_seeker(own_camp.position, own_seekers)
        dists = []
        for i in other_seekers:
            dists.append(world.torus_distance(own_camp.position, i.position) \
                + world.torus_distance(goal_scorer.position, i.position))
        torwart = other_seekers[dists.index(min(dists))]
        if world.torus_distance(torwart.position + (torwart.velocity) * 10, own_camp.position) < 25:
            s.target = own_camp.position
        else:
            s.target = torwart.position + (torwart.velocity) * 10
            s.target = torwart.position + torwart.velocity * (world.torus_distance(s.position, torwart.position)/((torwart.velocity - s.velocity).length()+0.000001))
        
    def be_keeper(s): #Torwart
        global Torwaerter
        if s not in Torwaerter:
            Torwaerter.append(s)
        if s.is_disabled:
            Torwaerter.remove(s)
        """KOENNEN WIR BITTE TORWART NENNEN"""
    
        """block the opponent's camp
        and distract the opponent to help /steal_goal/"""
        
        dangerous_goal = world.nearest_goal(other_camp.position, goals)
        angle = own_seekers.index(s)*2*math.pi/(len(Torwaerter)+0.000000001) - passed_time/70
        if len(Torwaerter)==0: Zielposition = s.position #gegen Fehlermeldungen
        if len(Torwaerter)==1: Zielposition = other_camp.position
        if len(Torwaerter)==2: Zielposition = other_camp.position + 120*(dangerous_goal.position - other_camp.position)/(world.torus_distance(dangerous_goal.position, other_camp.position)+0.0000001)
        if len(Torwaerter)>2: Zielposition = other_camp.position + Vector(100*math.cos(angle), 100*math.sin(angle)) #kein einziges mal getestet, Versuch auf eigene Gefahr
        if len(Torwaerter) != 0: 
            if s == world.nearest_seeker(other_camp.position, Torwaerter): Zielposition = other_camp.position
        s.target = Zielposition + (0.8**world.torus_distance(dangerous_goal.position + 10*dangerous_goal.velocity, other_camp.position))*(dangerous_goal.position + 10*dangerous_goal.velocity - other_camp.position)/2
        #print(len(Torwaerter))
        if (world.torus_distance(other_camp.position, dangerous_goal.position) < 150) and (world.torus_distance(s.position, dangerous_goal.position) < 100):
            s.magnet = dangerous_goal.polarity
            if world.torus_distance(s.position, other_camp.position) > 70:
                s.magnet = -dangerous_goal.polarity
        else:
            s.magnet = 0
        
    def steal_goal(s): #(Diese Rolle existierte letztes Jahr nicht) (Und wird dieses Jahr wieder nicht existieren :P)
        """cooperate with /be_keeper/ to steal the goal of an opponent /score_goal/"""
        
        s.target = other_camp.position + Vector(90, 40)
        
    # initiate verteiler
    if passed_time == 0: 
        global verteiler
        verteiler = [no_task] * len(own_seekers)
    verteiler[0] = be_keeper   #Torwart
    verteiler[1] = be_keeper   #Torwart
    verteiler[2] = score_goal  #Läufer
    verteiler[3] = score_goal  #Läufer
    verteiler[4] = score_goal  #Läufer
    verteiler[5] = ram_keeper  #Antitorwart
    #for i in range(6):
    #    verteiler[i] = score_goal
    for i in [0]:
        draw_line(own_seekers[i].position, own_seekers[i].target)
    #verteiler[4] = steal_goal  #[neu] coming "soon"

    for i, s in enumerate(own_seekers):
        verteiler[i](s)

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
            if world.torus_distance(own_seekers[i].position,
            world.nearest_seeker(own_seekers[i].position, other_activated_seekers).position) < 30:
                own_seekers[i].magnet = 0
        """
        if i == 0 and world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, other_seekers).position) < 25:
            own_seekers[i].target = Vector((2*own_seekers[i].position.x - world.nearest_seeker(own_seekers[i].position, other_seekers).position.x) % 768, (2*own_seekers[i].position.y - world.nearest_seeker(own_seekers[i].position, other_seekers).position.y) % 768)
        """
        if not i in Rammbockindizes:
            alls = all_seekers.copy()
            alls.remove(own_seekers[i])
            g = world.nearest_seeker(own_seekers[i].position, alls)
            if world.torus_distance(own_seekers[i].position, g.position) \
            > world.torus_distance(own_seekers[i].position + own_seekers[i].velocity, g.position + g.velocity):
                if world.torus_distance(own_seekers[i].position, g.position) < 20 + 20*g.velocity.length():
                    own_seekers[i].target = Vector((2*own_seekers[i].position.x - g.position.x) % 800,
                                                    (2*own_seekers[i].position.y - g.position.y) % 800)
                    #own_seekers[i].target = Vector((own_seekers[i].position.x - own_seekers[i].position.y + g.position.y) % 768, (own_seekers[i].position.y + own_seekers[i].position.x - g.position.x) % 768)
        """
        if i != (0 or 1) and (world.torus_distance(own_seekers[i].position, world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position) < 25) and not own_seekers[i].is_disabled:
            own_seekers[i].target = Vector((2*own_seekers[i].position.x - world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position.x) % 768, (2*own_seekers[i].position.y - world.nearest_seeker(own_seekers[i].position, all_disabled_seekers).position.y) % 768)
        """
    return own_seekers
