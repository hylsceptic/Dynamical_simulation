import math
from random import random
import ball

## Calculate impact of two balls within dt.
## Return 1 if imapcted. Return 0 if not. 

def abs2D(v1):
    return math.sqrt(v1[0]**2 + v1[1]**2)


def dotProduct(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]

def sign(num):
    if num >=0:
        return 1
    else:
        return -1

def getAngleByVector(v):
    v=[v[0], -v[1]]
    angle0 = 0
    if v[0] < 0:
        v = [-v[0], -v[1]]
        angle0 += math.pi
    angle = math.asin(v[1]/math.sqrt(v[0]**2 + v[1]**2))
    return angle + angle0

def impact2Ball(ball1, ball2, dt, g=[0, 0], e=1, f=0):
    ## initial relative distance
    v1  = (ball2.location[0] - ball1.location[0], ball2.location[1] - ball1.location[1])
    ## imitial relative velocity
    v2 = (ball2.velocity[0] - ball1.velocity[0], ball2.velocity[1] - ball1.velocity[1])
    ## scale of relative distance and relative velocity
    dis = math.sqrt(v1[0]**2 + v1[1]**2)
    velocity = math.sqrt(v2[0]**2 + v2[1]**2)

    ## if impact does not happen, then retrun 0.
        ## relative speed = 0
    if velocity <= 0.0: return 0
        ## move apart from each other, cos(v1, v2)
    cs = (v1[0]*v2[0] + v1[1]*v2[1])/dis/velocity
    if cs >= 0: return 0
    s1 = math.sqrt(1 - min(1, cs**2))*dis
        ## never touch
    if s1 - ball1.radius - ball2.radius > 0: return 0    

    ## movement before impact
    dt1 = (math.sqrt(dis**2 - s1**2) - math.sqrt((ball1.radius + ball2.radius)**2 - s1**2))*-cs/velocity
    if dt1 > dt:
        return 0
    ball1.location[0] += ball1.velocity[0]*dt1
    ball1.location[1] += ball1.velocity[1]*dt1
    ball2.location[0] += ball2.velocity[0]*dt1
    ball2.location[1] += ball2.velocity[1]*dt1
    dt2 = dt - dt1

    ## update relative distance
    v1  = (ball2.location[0] - ball1.location[0], ball2.location[1] - ball1.location[1])
    dis = math.sqrt(v1[0]**2 + v1[1]**2)
    
    ## update speed
    vscale = abs(v1[0]*v2[0] + v1[1]*v2[1])/dis
    v = (vscale*v1[0]/dis, vscale*v1[1]/dis)
    if v[0]*v1[0] + v[1]*v1[1] > 0:
        v = [-v[0], -v[1]]
    verticalVball1 = [ (v[0]*(1 + e)*(ball2.mass/(ball1.mass + ball2.mass))),  (v[1]*(1 + e)*(ball2.mass/(ball1.mass + ball2.mass)))]
    verticalVball2 = [-(v[0]*(1 + e)*(ball1.mass/(ball1.mass + ball2.mass))), -(v[1]*(1 + e)*(ball1.mass/(ball1.mass + ball2.mass)))]
    verticalSball1 = abs2D(verticalVball1)
    verticalSball2 = abs2D(verticalVball2)
    ## Tangential speed
    ## relative velocity of centers
    
    angle1 = getAngleByVector(v1)
    angle2 = getAngleByVector([-v1[0], -v1[1]])
    boundvball1 = ball1.getBoundaryVelocity(angle1)
    boundvball2 = ball2.getBoundaryVelocity(angle2)
    relativeTv = [boundvball2[0] - boundvball1[0] - v[0], boundvball2[1] - boundvball1[1] - v[1]]
    relativeTs = abs2D(relativeTv)
    vectorRelativeTv = [relativeTv[0]/relativeTs, relativeTv[1]/relativeTs]
    if relativeTs > 0 and f > 0:
        maxChangeTs1 = verticalSball1*f*(1 + 1/(2/5*ball1.mass))
        maxChangeTs2 = verticalSball2*f*(1 + 1/(2/5*ball2.mass))
        newRv = max(0, relativeTs - maxChangeTs1 - maxChangeTs2)
        realChangeTv = relativeTs - newRv
        realChangeTvB1 = realChangeTv*maxChangeTs1/(maxChangeTs1 + maxChangeTs2)
        realChangeTvB2 = realChangeTv*maxChangeTs2/(maxChangeTs1 + maxChangeTs2)


        ## update ball1
        realChangeTvB1F = realChangeTvB1*1/((1 + 1/(2/5*ball1.mass)))
        ball1.velocity[0] = ball1.velocity[0] + vectorRelativeTv[0]*realChangeTvB1F
        ball1.velocity[1] = ball1.velocity[1] + vectorRelativeTv[1]*realChangeTvB1F
        
        realChangeTvB1F = realChangeTvB1*1/(2/5*ball1.mass)/((1 + 1/(2/5*ball1.mass)))
        momentum = [vectorRelativeTv[0]*realChangeTvB1F*ball1.mass, vectorRelativeTv[1]*realChangeTvB1F*ball1.mass]
        ball1.updateAngVelocity(ball1.getBoundaryPointByAngle(angle1), momentum)
        ## update ball2
        realChangeTvB2F = realChangeTvB2*1/((1 + 1/(2/5*ball1.mass)))
        ball2.velocity[0] = ball2.velocity[0] - vectorRelativeTv[0]*realChangeTvB2F
        ball2.velocity[1] = ball2.velocity[1] - vectorRelativeTv[1]*realChangeTvB2F

        realChangeTvB2F = realChangeTvB2*1/(2/5*ball1.mass)/((1 + 1/(2/5*ball1.mass)))
        momentum = [-vectorRelativeTv[0]*realChangeTvB1F*ball2.mass, -vectorRelativeTv[1]*realChangeTvB1F*ball2.mass]
        ball2.updateAngVelocity(ball2.getBoundaryPointByAngle(angle2), momentum)
        cp = ball2.getBoundaryPointByAngle(angle2)
        print(dotProduct([cp[0] - ball2.location[0], cp[1] - ball2.location[1]], vectorRelativeTv))
        # print(ball2.location, angle2)
        # print(ball1.location, angle1)

    ball1.velocity[0] = ball1.velocity[0] + verticalVball1[0] + dt*g[0]
    ball1.velocity[1] = ball1.velocity[1] + verticalVball1[1] + dt*g[1]
    ball2.velocity[0] = ball2.velocity[0] + verticalVball2[0] + dt*g[0]
    ball2.velocity[1] = ball2.velocity[1] + verticalVball2[1] + dt*g[1]


    # vt = [v2[0] - v[0], v2[1] - v[1]]

    # vtscale = math.sqrt(vt[0]**2 + vt[1]**2)
    # if vtscale > 0:
    #     dvtscale = vtscale - max(0, vtscale - abs(vscale)*f*2)
    #     dvt = (dvtscale/vtscale*vt[0], dvtscale/vtscale*vt[1])
    #     # dvt = vt
    #     ball1.velocity[0] = ball1.velocity[0] - (dvt[0]*(ball2.mass/(ball1.mass + ball2.mass)))
    #     ball1.velocity[1] = ball1.velocity[1] - (dvt[1]*(ball2.mass/(ball1.mass + ball2.mass)))
    #     ball2.velocity[0] = ball2.velocity[0] + (dvt[0]*(ball1.mass/(ball1.mass + ball2.mass)))
    #     ball2.velocity[1] = ball2.velocity[1] + (dvt[1]*(ball1.mass/(ball1.mass + ball2.mass)))

    ## after updated speed, update each ball's state
    ball1.updateState(g)
    ball2.updateState(g)

    ball1.location[0] += ball1.velocity[0]*dt2
    ball1.location[1] += ball1.velocity[1]*dt2
    ball2.location[0] += ball2.velocity[0]*dt2
    ball2.location[1] += ball2.velocity[1]*dt2
    return 1

def generateSpecifiedBalls(num, velocity, radius, location, resolution, state):
    balls = []
    for i in range(num):
        balls.append(ball.Ball(radius[i], velocity[i], location[i], [255*random(), 255*random(), 255*random()], state=state[i]))
    return balls



def generateRandomBalls(num, maxv, minv, radius, resolution):
    balls = []
    for i in range(num):
        while 1:
            location = [resolution[0]*random(), resolution[1]*random()]
            if location[0] + radius > resolution[0] or location[0] - radius < 0 \
                or location[1] + radius > resolution[1] or location[1] - radius < 0: continue
            sig = 0
            for eachBall in balls:
                if math.sqrt((location[0] - eachBall.location[0])**2 + (location[1] - eachBall.location[1])**2) - radius - eachBall.radius < 0: 
                    sig = 1
                    break
            if sig == 1: continue
            vx = minv + (maxv - minv)*random()
            vy = minv + (maxv - minv)*random()
            balls.append(ball.Ball(radius, [vx, vy], location, [255*random(), 255*random(), 255*random()]))
            break
    return balls


## detect all the  balls in the same canvas, and update their states.

def detectAllImpactAndUpdate(totalballs, resolution, k, LocationTable, dt, g=[0, 0], e=1, f=0):

    for x in range(k):
        for y in range(k):
            balls = []
            for eachBall in LocationTable[x][y]:
                balls.append(eachBall)
            num1 = len(balls)
            if x + 1 < k:
                for eachBall in LocationTable[x + 1][y]:
                    balls.append(eachBall)
            if y + 1 < k:
                for eachBall in LocationTable[x][y + 1]:
                    balls.append(eachBall)
            if x + 1 < k and y + 1 < k:
                for eachBall in LocationTable[x + 1][y + 1]:
                    balls.append(eachBall)
            if x - 1 > 0 and y + 1 < k:
                for eachBall in LocationTable[x - 1][y + 1]:
                    balls.append(eachBall)
            num2 = len(balls)
            for i in range(num1):
                ball1 = balls[i]
                if ball1.isImpact == 1: continue
                for j in range(i + 1, num2):
                    ball2 = balls[j]
                    if  ball2.isImpact == 1:
                        continue
                    isImpact = impact2Ball(ball1, ball2, dt, g, e=e, f=f)
                    ball1.isImpact, ball2.isImpact = isImpact, isImpact

    return LocationTable 


## create a table lists all the balls in the list. 

def createLocationTable(balls, resolution, k):
    LocationTable = []
    for x in range(k):
        pX = []
        for y in range(k):
            pX.append([])
        LocationTable.append(pX)
    width, height = resolution[0]/k, resolution[1]/k
    for eachBall in balls:
        # print(eachBall.location[0], eachBall.location[1], int(eachBall.location[0]/width), int(eachBall.location[1]/height))
        LocationTable[int(eachBall.location[0]/width)][int(eachBall.location[1]/height)].append(eachBall)
        eachBall.isImpact = 0
    return LocationTable


class Bit():
    def __init__(self, num):
        self.bits = num
    def getBit(self, n):
        return ((self.bits >> n & 1) != 0)

    def setBit(self, n):
        self.bits = self.bits | (1 << n)

    def clearBit(self, n):
        self.bits = self.bits & ~(1 << n)