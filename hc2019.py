import numpy as np
import queue
import heapq
import math

print("-- Start --")

R = 10000
C = 10000
F = 1000
N = 10000
B = 10000
T = 1e9
start = []
finish = []
stime = []
ftime = []
rtime = []
startx = 0
starty = 0
endx = 0
endy = 0
startxx = 0
startyy = 0
endxx = 0
endyy = 0
startdx = 0
startdy = 0
enddx = 0
enddy = 0

fnames = ["input.txt", "output.txt"]
#fnames = ["b_should_be_easy.in", "b_should_be_easy.out"]
#fnames = ["c_no_hurry.in", "c_no_hurry.out"]
# fnames = ["d_metropolis.in", "d_metropolis.out"]
#fnames = ["e_high_bonus.in", "e_high_bonus.out"]

def distance(a1, b1, a2, b2):
    return abs(a1-a2) + abs(b1-b2)

def badness(a, b):
    da = abs(a - startx) / startdx
    da = math.sqrt(4+da*da) * startdx
    db = abs(b - starty) / startdy
    db = math.sqrt(4+db*db) * startdy
    return da+db

def doride(car, ride): # (eff, car, pts)
    r,c,t = car
    t2 = t + distance(r,c, start[ride][0], start[ride][1])
    if t2 + rtime[ride] > ftime[ride]:
        return (-1,0,0)
    elif t2 <= stime[ride]:
        pts = B + rtime[ride]
        endtime = stime[ride] + rtime[ride]
        eff = pts / (endtime - t)
        bad = badness(finish[ride][0], finish[ride][1])
        bad = min(bad, T-endtime)
        return (endtime-pts+B-rtime[ride]/4000, (finish[ride][0], finish[ride][1], endtime), pts)
    else:
        pts = rtime[ride]
        endtime = t2 + rtime[ride]
        eff = pts / (endtime - t)
        bad = badness(finish[ride][0], finish[ride][1])
        bad = min(bad, T-endtime)
        return (endtime-pts+B-rtime[ride]/4000, (finish[ride][0], finish[ride][1], endtime), pts)

# Start reading & parsing the input file
print("Start reading & parsing the input file")

with open(fnames[0], 'r') as f:
    line = f.readline().split(' ')
    R = int(line[0])
    C = int(line[1])
    F = int(line[2])
    N = int(line[3])
    B = int(line[4])
    T = int(line[5])
    stime = [0]*N
    ftime = [0]*N
    rtime = [0]*N
    for i in range(N):
        line = f.readline().split(' ')
        s1 = int(line[0])
        s2 = int(line[1])
        f1 = int(line[2])
        f2 = int(line[3])
        start.append((s1, s2))
        finish.append((f1, f2))
        stime[i] = int(line[4])
        ftime[i] = int(line[5])
        rtime[i] = distance(s1,s2, f1,f2)
        startx += s1
        starty += s2
        startxx += s1*s1
        startyy += s2*s2
        endx += f1
        endy += f2
        endxx += f1*f1
        endyy += f2*f2
        
print("Done reading & parsing.")

startx /= N
starty /= N
startxx /= N
startyy /= N
endx /= N
endy /= N
endxx /= N
endyy /= N
startdx = math.sqrt(startxx - startx*startx)
startdy = math.sqrt(startyy - starty*starty)
enddx = math.sqrt(endxx - endx*endx)
enddy = math.sqrt(endyy - endy*endy)

print(startx, starty, startdx, startdy)

curcars = [0]*F
for i in range(F):
    curcars[i] = (0,0,0) # r, c, time
ridedone = [0]*N

Q = []
for i in range(F):
    for j in range(N):
        eff, car, pts = doride(curcars[i], j)
        #print(eff, car)
        if eff != -1:
            heapq.heappush(Q, (eff, (i, j, car, curcars[i][2], pts))) # (-eff, (F, N, carstate, lastendtime, pts))

ans = []
for i in range(F):
    ans.append([])
totalscore = 0

counter = 0
print("Q %d" % len(Q))
while Q:
    counter += 1
    if counter % 500000 == 0:
        print("Q %d" % len(Q))
    eff, data = heapq.heappop(Q)
    #print(eff, data)
    i,j,car,endtime,pts = data
    if endtime == curcars[i][2] and not ridedone[j]:
        ans[i].append(j)
        curcars[i] = car
        ridedone[j] = 1
        totalscore += pts
    elif not ridedone[j]:
        eff, car, pts = doride(curcars[i], j)
        if eff >= 0:
            heapq.heappush(Q, (eff, (i, j, car, curcars[i][2], pts))) # (-eff, (F, N, carstate, lastendtime))

# print(ans)
print(totalscore)

# Writing solutino to file
print("-- Writing solution to file --")
with open(fnames[1], 'w') as f:
    for i in range(F):
        f.write("%d " % len(ans[i]))
        for j in range(len(ans[i])):
            f.write("%d " % ans[i][j])
        f.write("\n")
        
print("-- Finish program --")