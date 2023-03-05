import csv
import math
import random

# CONFIGURATION
teamsfile = 'teams.csv' # CSV file with rows being (team, program ranking, lat, long)
score_mult = 0.7        # higher = prioritizes program strength similarity over geography
num_confs = 32
iterations = 1000
size_penalty = 0.75     # higher = stricter about similar-sized conferences but also increases chances of completely fucking up. Would not recommend adjusting





score_min = 999
score_max = -999
lat_min = 90
lat_max = -90
long_min = 180
long_max = -180

teams = []
with open(teamsfile, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        name = row[0]
        score = float(row[1]) * score_mult
        lat = float(row[2])
        long = float(row[3])
        teams.append((name, score, lat, long))
        
        score_min = min(score_min, score)
        score_max = max(score_max, score)
        lat_min = min(lat_min, lat)
        lat_max = max(lat_max, lat)
        long_min = min(long_min, long)
        long_max = max(long_max, long)
        
s1 = ((score_min*4) + score_max) / 5
s2 = ((score_max*4) + score_min) / 5
a1 = ((lat_min*4) + lat_max) / 5
a2 = ((lat_max*4) + lat_min) / 5
o1 = ((long_min*4) + long_max) / 5
o2 = ((long_max*4) + long_min) / 5   
conf_centers = []

for i in range(num_confs):
    conf_centers.append((i, random.uniform(s1, s2), random.uniform(a1, a2), random.uniform(o1, o2)))
    

    
def calc_dist(t1, t2):
    return math.sqrt((t1[1] - t2[1])**2 + (t1[2] - t2[2])**2 + (t1[3] - t2[3])**2)

def reset_confs():
    ret = []
    
def find_center(i, conf):
    scores = 0
    lats = 0
    longs = 0
    num_teams = len(conf)
    if (num_teams == 0):
        return (i, random.uniform(s1, s2), random.uniform(a1, a2), random.uniform(o1, o2))
    for team in conf:
        scores += team[1]
        lats += team[2]
        longs += team[3]
    return (i, scores/num_teams, lats/num_teams, longs/num_teams)
    

def iterate(conf_centers):
    confs = []
    confs2 = []
    for i in range(num_confs):
        confs.append([])   
        confs2.append([])
    
    for team in teams:
        min_dist = 999
        min_i = -1
        for i in range(num_confs):
            dist = calc_dist(team, conf_centers[i])
            if (dist < min_dist):
                min_dist = dist
                min_i = i
        
        confs[min_i].append(team)
        
    for team in teams:
        min_dist = 999
        min_i = -1
        for i in range(num_confs):
            dist = calc_dist(team, conf_centers[i]) * (len(confs[i]) ** size_penalty)
            if (dist < min_dist):
                min_dist = dist
                min_i = i
        
        confs2[min_i].append(team)
    
    new_conf_centers = []
    for i in range(num_confs):
        new_conf_centers.append(find_center(i, confs2[i]))
        
    return(new_conf_centers, confs)
    

for it in range(iterations):
    stuff = iterate(conf_centers)
    conf_centers = stuff[0]
    confs = stuff[1]

for i in range(num_confs):
    print(conf_centers[i])
    for team in confs[i]:
        print(team[0] + ', ')
    