from seekers import *
from seekers.debug_drawing import *

__color__ = (40, 200, 255)

seeker_tasks = []
magnet_strength = 0
goal_assignment = []

def decide(own_seekers: list[Seeker], other_seekers: list[Seeker], all_seekers: list[Seeker], goals: list[Goal],
           other_players: list[Player], own_camp: Camp, camps: list[Camp], world: World, passed_time: float):
           
    # find other Camp
    for camp in camps:
        if camp != own_camp:
            other_camp = camp
            break
        
    # calculate magnet strength of a seeker
    magnet_strength = lambda s: len([i for i in own_seekers if i.magnet == s.magnet]) ** -1
    #                                                          ^^^^^^^^^^
    #Attribute Error: ´Seeker´ object has no attribute ´polarity´


    def no_task(s):
        """do nothing"""
        pass


    def score_goal(s): #Läufer
        """find optimal goal, and bring it to the camp"""
    
        # find optimal goal
        # goal_score_weights = [1, 1.5, 2, 5, 3]
        goal_score_weights = [2, 8, 1, 3, 2]
        goal_scores = {g: 0 for g in [i for i in goals if i not in goal_assignment]}
        
        for g, score in goal_scores.items():
            # print(g.id)
            score += goal_score_weights[0] * -world.torus_distance(g.position, own_camp.position) # unser camp
            score += goal_score_weights[1] * -world.torus_distance(g.position, s.position) # nähe zum seeker
            score += goal_score_weights[2] *  world.torus_distance(g.position, 
                        world.nearest_seeker(g.position, other_seekers).position) # nähe zum gegnerischem seeker
            #score += goal_score_weights[3] * +world.torus_distance(g.position, 
                        #world.nearest_seeker(g.position, [i for i in own_seekers if i != s]).position) # nähe zu team mates
            score += goal_score_weights[3] * +world.torus_distance(g.position, 
                        world.nearest_seeker(g.position, [i for i in scorers if i != s]).position)
            score += goal_score_weights[4] * world.torus_distance(world.nearest_goal(g.position, [i for i in goals if i.polarity == g.polarity]).position, g.position)
            #score += goal_score_weights[4] * -sum([world.torus_distance(g.position, other_g.position) for other_g in [i for i in goals if i != g]if other_g.polarity == g.polarity]) # nähe zu anderen goals
            #goal_scores
            goal_scores[g] = score
            #print(goal_scores[0])
        optimal_goal = min(goal_scores, key=goal_scores.get)
        
        #goal_assignment.append(optimal_goal)
        distance = 90
        
        # return to camp
        if world.torus_distance(s.position + 7 * s.velocity,
            optimal_goal.position) < distance:
            
            s.magnet = -optimal_goal.polarity
            s.target = own_camp.position
            
            #if world.torus_distance(own_seekers[0].position + 7 * own_seekers[0].velocity, own_camp.position) \
            #    < 50 * magnet_strength(s):
            if world.torus_distance(s.position + 7 * s.velocity, own_camp.position) \
                < 20 * magnet_strength(s):
                
                s.target = Vector(s.position.x - s.velocity.x,
                s.position.y - s.velocity.y)
           
        # go to goal
        else:
            s.magnet = 0
            s.target = optimal_goal.position
            
    def ram_keeper(s): #Antitorwart
        """neutralize the opponent's goalkeeper"""
        
        goal_scorer = own_seekers[0]
        dists = []
        for i in other_seekers:
            dists.append(world.torus_distance(own_camp.position, i.position) \
                + world.torus_distance(goal_scorer.position, i.position))
        torwart = other_seekers[dists.index(min(dists))]
        if world.torus_distance(torwart.position + (torwart.velocity) * 10, own_camp.position) < 25:
            s.target = own_camp.position
        else:
            s.target = torwart.position + (torwart.velocity) * 10
        
    def be_keeper(s): #Torwart
        """block the opponent's camp
        and distract the opponent to help /steal_goal/"""
        
        #s.target = other_camp.position
        dangerous_goal = world.nearest_goal(other_camp.position, goals)
        #t = Vector(world.nearest_goal(other_camp.position, goals).position) + Vector(other_camp.position)
        #s.target = Vector(int(t[0]) // 2, int(t[1]) // 2)
        s.target = other_camp.position + (0.9**world.torus_distance(dangerous_goal.position, other_camp.position))*(dangerous_goal.position - other_camp.position)/2
        
        if (world.torus_distance(other_camp.position, dangerous_goal.position) < 150) and (world.torus_distance(s.position, dangerous_goal.position) < 100):
            s.magnet = dangerous_goal.polarity
        else:
            s.magnet = 0
            
    def steal_goal(s): #(Diese Rolle existierte letztes Jahr nicht]
        """cooperate with /be_keeper/ to steal the goal of an opponent /score_goal/"""
        
        s.target = other_camp.position + Vector(90, 40)
        
    # initiate seeker_tasks
    if passed_time == 0: 
        global seeker_tasks
        seeker_tasks = [no_task] * len(own_seekers)
    
    seeker_tasks[0] = score_goal  #Läufer
    seeker_tasks[1] = score_goal  #Läufer
    seeker_tasks[2] = be_keeper  #Antitorwart
    seeker_tasks[3] = be_keeper    #Torwart
    seeker_tasks[4] = score_goal
    seeker_tasks[5] = ram_keeper

    scorers = list(filter(lambda n: seeker_tasks[own_seekers.index(n)] == score_goal, own_seekers))

    for i, s in enumerate(own_seekers):  
        seeker_tasks[i](s)
        draw_line(s.position, s.target)
        
        g = world.nearest_seeker(s.position, [a for a in all_seekers if a != i])
        if world.torus_distance(own_seekers[i].position, g.position) > world.torus_distance(own_seekers[i].position + own_seekers[i].velocity, g.position + g.velocity):
            if world.torus_distance(own_seekers[i].position, g.position) < 20 + 20*g.velocity.length():
                own_seekers[i].target = Vector((2*own_seekers[i].position.x - g.position.x) % 800, (2*own_seekers[i].position.y - g.position.y) % 800)
        #s.magnet = -g.polarity
        #s.target = g.position + 20 * Vector(s.velocity.y, -s.velocity.x)/(s.velocity.length() + 0.000000001)

    return own_seekers
