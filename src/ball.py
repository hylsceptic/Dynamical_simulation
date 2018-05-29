import  math, pygame
import utils

def sign(num):
    if num >=0:
        return 1
    else:
        return -1

def crossProduct2D(v1, v2):
    return v1[0]*-v2[1] - v2[0]*-v1[1]

def getPointWithRadian(center, r, radian):
    return [center[0] + r*math.cos(radian), center[1] - r*math.sin(radian)]

def abs2D(v1):
    return math.sqrt(v1[0]**2 + v1[1]**2)

class Ball():

    def __init__(self, radius, velocity, location, color,  mass=1, state=0, angVelocity=0, radian=0):
        self.radius = radius
        self.velocity = velocity
        self.location = location
        self.color = color
        self.mass = mass
        # state = 1: roll in y direction
        #         2: roll in x direction
        #         3: still
        self.state = utils.Bit(state)
        self.angVelocity = angVelocity
        self.radian = radian

    # def getAngleByVector(v):
    #     v=[v[0], -v[1]]


    def  updateRadian(self, dt):
        self.radian += self.angVelocity*dt

    def updateAngVelocity(self, cpoint, momentum):
        ## cpoint: contact point
        v1 = (cpoint[0] - self.location[0], cpoint[1] - self.location[1])
        sig = sign(crossProduct2D(v1, momentum))
        ## J = 2/5*m*r^2,  P*r = J*d(alpha), where alpha is angular velocity
        self.angVelocity += sig*abs2D(momentum)/(2/5*self.mass*self.radius)


    def draw(self, surface):
        location = [int(self.location[0]), int(self.location[1])]
        pygame.draw.circle(surface, self.color, location, self.radius)
        p1 = getPointWithRadian(self.location, self.radius*2/3, self.radian)
        p2 = getPointWithRadian(self.location, self.radius*2/3, self.radian + 2/3*math.pi)
        p3 = getPointWithRadian(self.location, self.radius*2/3, self.radian + 4/3*math.pi)
        pygame.draw.line(surface, [0, 0, 0], p1, p2, 10)
        pygame.draw.line(surface, [0, 0, 0], p1, p3, 10)
        pygame.draw.line(surface, [0, 0, 0], p2, p3, 10)

    def  updateState(self, g):
        if self.state.getBit(1): 
            if abs(self.velocity[1]) > abs(g[1]/10):
                self.state.clearBit(1)
        if self.state.getBit(0):
            if abs(self.velocity[0]) > abs(g[0]/10):
                self.state.clearBit(0)
        # error = self.radius/100
        # sizex, sizey = surface.get_size()
        # if abs(self.velocity[1]) <= abs(g[1]/10):
        #     if g[1] > 0 and abs(sizey - self.location[1] - self.radius) < error:
        #         self.velocity[1] = 0
        #         self.location[1] = sizey - self.radius
        #         self.state.setBit(1)
        #     if g[1] < 0 and abs(self.location[1] - self.radius) < error:
        #         self.velocity[1] = 0
        #         self.location[1] = self.radius
        #         self.state.setBit(1)
        # if abs(self.velocity[0]) <= abs(g[0]/10):
        #     if g[0] > 0 and abs(sizex - self.location[0] - self.radius) < error:
        #         self.velocity[0] = 0
        #         self.location[0] = sizex - self.radius
        #         self.state.setBit(1)
        #     if g[0] < 0 and abs(self.location[0] - self.radius) < error:
        #         self.velocity[0] = 0
        #         self.location[0] = self.radius
        #         self.state.setBit(1)


    def getSpeed(self):
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    def update(self, surface, g, dt, e=1, f=0, fr=0):
            if self.state.getBit(0) and self.state.getBit(1):
                return
            sizex, sizey = surface.get_size()
            dty = dt
            ds = self.velocity[1]*dty + 1/2*g[1]*dty**2

            if not self.state.getBit(1):
                ## if impact the bottom boundary
                if self.location[1] + self.radius + ds > sizey:
                    ds1 = sizey - self.location[1] - self.radius
                    if g[1] == 0:
                        dt1 = (sizey - self.location[1] - self.radius)/self.velocity[1]
                    elif ds1 <= 0:
                        dt1 = 0
                    else:
                        dt1Tmp = math.sqrt(max((self.velocity[1]/g[1])**2 + 2*ds1/g[1], 0)) - self.velocity[1]/g[1]
                        if dt1Tmp >= 0 and dt1Tmp < dty:
                            dt1 = dt1Tmp
                        else:
                            dt1 = - math.sqrt(max((self.velocity[1]/g[1])**2 + 2*ds1/g[1], 0)) - self.velocity[1]/g[1]
                    v1 = self.velocity[1]
                    self.velocity[1] = -(v1 + g[1]*dt1)*e
                    verticaldv = abs(self.velocity[1] - v1)
                    relativeV = abs(self.velocity[0] + self.radius*self.angVelocity)
                    signv = -sign(self.velocity[0] + self.radius*self.angVelocity)
                    if f > 0:
                        maxChangeTvC, maxChangeTvR = verticaldv*f, verticaldv*f/(2/5*self.mass*self.radius)*self.radius
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeV - maxChangeTv)
                        realChangeTv = relativeV - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv

                        cpoint = [self.location[0], self.location[1] + self.radius]
                        self.velocity[0] += signv*momentum
                        self.updateAngVelocity(cpoint, [signv*momentum, 0])
                    
                    self.location[1] = sizey - self.radius
                    dty -= dt1
                    ds = self.velocity[1]*dty + 1/2*g[1]*dty**2
                    if abs(self.velocity[1]) <= abs(g[1]/10):
                        self.velocity[1] = 0
                        self.location[1] = sizey - self.radius
                        self.state.setBit(1)


                ## if impact the up boundary
                if self.location[1] - self.radius + ds < 0:
                    ds1 = - (self.location[1] - self.radius)
                    if g[1] == 0:
                        dt1 = (self.location[1] - self.radius)/self.velocity[1]
                    elif ds1 <= 0:
                        dt1 = 0
                    else:
                        dt1Tmp = math.sqrt(max((self.velocity[1]/g[1])**2 + 2*ds1/g[1], 0)) - self.velocity[1]/g[1]
                        if dt1Tmp >= 0 and dt1Tmp < dty:
                            dt1 =  dt1Tmp
                        else:
                            dt1 = - math.sqrt(max((self.velocity[1]/g[1])**2 + 2*ds1/g[1], 0)) - self.velocity[1]/g[1]
                    v1 = self.velocity[1]
                    self.velocity[1] = -(v1 + g[1]*dt1)*e
                    verticaldv = abs(self.velocity[1] - v1)
                    relativeV = abs(self.velocity[0] - self.radius*self.angVelocity)
                    signv = -sign(self.velocity[0] - self.radius*self.angVelocity)
                    if f > 0:
                        maxChangeTvC, maxChangeTvR = verticaldv*f, verticaldv*f/(2/5*self.mass*self.radius)*self.radius
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeV - maxChangeTv)
                        realChangeTv = relativeV - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv

                        cpoint = [self.location[0], self.location[1] - self.radius]
                        self.velocity[0] += signv*momentum
                        self.updateAngVelocity(cpoint, [signv*momentum, 0])
                    self.location[1] = self.radius

                    dty -= dt1
                    ds = self.velocity[1]*dty + 1/2*g[1]*dty**2
                    if abs(self.velocity[1]) <= abs(g[1]/10):
                        self.velocity[1] = 0
                        self.location[1] = self.radius
                        self.state.setBit(1)

                if not self.state.getBit(1):
                    self.location[1] = self.location[1] + ds
                    self.velocity[1] = self.velocity[1] + g[1] * dty
                
                ## if contact with the left or right boundaries
                if self.state.getBit(0):
                    ## if contact with the left boundary
                    if abs(self.location[0] - self.radius) < 1e-6:
                        relativeV = self.getBoundaryVelocity(math.pi)
                        cpoint = [self.location[0] - self.radius, self.location[1]]
                        signv = -sign(self.velocity[1] + self.radius*self.angVelocity)
                    ## if contact with the right boundary
                    else:
                        relativeV = self.getBoundaryVelocity(0)
                        cpoint = [self.location[0] + self.radius, self.location[1]]
                        signv = -sign(self.velocity[1] - self.radius*self.angVelocity)

                    relativeSpeed = abs2D(relativeV)
                    if relativeSpeed > 0:
                        maxMomentum = abs(g[0])*f*dty*self.mass
                        maxChangeTvC = maxMomentum/self.mass
                        maxChangeTvR = maxMomentum/(2/5*self.mass*self.radius)*self.radius/self.mass
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeSpeed - maxChangeTv)
                        realChangeTv = relativeSpeed - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv*self.mass

                        self.velocity[1] += signv*momentum
                        self.updateAngVelocity(cpoint, [-momentum*relativeV[0]/relativeSpeed, -momentum*relativeV[1]/relativeSpeed]) 
                    self.angVelocity += -sign(self.angVelocity)*min(abs(self.angVelocity), abs(g[0])*dty*fr/(2/5*self.mass*self.radius))

            if not self.state.getBit(0):
                dtx = dt
                ds = self.velocity[0]*dtx + 1/2*g[0]*dtx**2
                ## if impact the right boundary
                if self.location[0] + self.radius + ds > sizex:
                    ds1 = sizex - self.location[0] - self.radius
                    if g[0] == 0:
                        dt1 = (sizex - self.location[0] - self.radius)/self.velocity[0]
                    elif ds1 <= 0:
                        dt1 = 0
                    else:
                        dt1Tmp = math.sqrt((self.velocity[0]/g[0])**2 + 2*ds1/g[0]) - self.velocity[0]/g[0]
                        # print('dt1Tmp', dt1Tmp, dtx)
                        if dt1Tmp >= 0 and dt1Tmp < dtx:
                            dt1 = dt1Tmp
                        else:
                            dt1 = - math.sqrt((self.velocity[0]/g[0])**2 + 2*ds1/g[0]) - self.velocity[0]/g[0]
                            # print('dt1',dt1)
                    v1 = self.velocity[0]
                    self.velocity[0] = -(v1 + g[0]*dt1)*e
                    verticaldv = abs(self.velocity[0] - v1)
                    relativeV = abs(self.velocity[1] - self.radius*self.angVelocity)
                    signv = -sign(self.velocity[1] - self.radius*self.angVelocity)
                    if f > 0:
                        maxChangeTvC, maxChangeTvR = verticaldv*f, verticaldv*f/(2/5*self.mass*self.radius)*self.radius
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeV - maxChangeTv)
                        realChangeTv = relativeV - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv


                        cpoint = [self.location[0] + self.radius, self.location[1]]
                        self.velocity[1] += signv*momentum
                        self.updateAngVelocity(cpoint, [0, signv*momentum])
                    self.location[0] = sizex - self.radius
                    dtx -= dt1
                    ds = self.velocity[0]*dtx + 1/2*g[0]*dtx**2
                    if abs(self.velocity[0]) <= abs(g[0]/10):
                        self.velocity[0] = 0
                        self.location[0] = sizex - self.radius
                        self.state.setBit(0)


                ## if impact the left boundary
                if self.location[0] - self.radius + ds < 0:
                    ds1 = - (self.location[0] - self.radius)
                    if g[0] == 0:
                        dt1 = (self.location[0] - self.radius)/self.velocity[0]
                    elif ds1 <= 0:
                        dt1 = 0
                    else:
                        dt1Tmp = math.sqrt((self.velocity[0]/g[0])**2 + 2*ds1/g[0]) - self.velocity[0]/g[0]
                        if dt1Tmp >= 0 and dt1Tmp < dtx:
                            dt1 =  dt1Tmp
                        else:
                            dt1 = - math.sqrt((self.velocity[0]/g[0])**2 + 2*ds1/g[0]) - self.velocity[0]/g[0]
                    v1 = self.velocity[0]
                    self.velocity[0] = -(v1 + g[0]*dt1)*e
                    verticaldv = abs(self.velocity[0] - v1)
                    relativeV = abs(self.velocity[1] + self.radius*self.angVelocity)
                    signv = -sign(self.velocity[1] + self.radius*self.angVelocity)
                    if f > 0:
                        maxChangeTvC, maxChangeTvR = verticaldv*f, verticaldv*f/(2/5*self.mass*self.radius)*self.radius
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeV - maxChangeTv)
                        realChangeTv = relativeV - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv

                        cpoint = [self.location[0] - self.radius, self.location[1]]
                        self.velocity[1] += signv*momentum
                        self.updateAngVelocity(cpoint, [0, signv*momentum])
                    self.location[0] = self.radius
                    dtx -= dt1
                    ds = self.velocity[0]*dtx + 1/2*g[0]*dtx**2
                    if abs(self.velocity[0]) <= abs(g[0]/10):
                        self.velocity[0] = 0
                        self.location[0] = self.radius
                        self.state.setBit(0)
                            # if self.velocity[0] == 0:
                            #     self.state = 3

                if not self.state.getBit(0):
                    self.location[0] = self.location[0] + ds
                    self.velocity[0] = self.velocity[0] + g[0] * dtx

                ## if contact with the bottom or up boundaries
                if self.state.getBit(1):
                    ## if contact with the up boundary
                    if abs(self.location[1] - self.radius) < 1e-6:
                        relativeV = self.getBoundaryVelocity(1/2*math.pi)
                        cpoint = [self.location[0], self.location[1] - self.radius]
                        signv = -sign(self.velocity[0] - self.radius*self.angVelocity)
                    ## if contact with the bottom boundary
                    else:
                        relativeV = self.getBoundaryVelocity(3/2*math.pi)
                        cpoint = [self.location[0], self.location[1] + self.radius]
                        signv = -sign(self.velocity[0] + self.radius*self.angVelocity)
                    relativeSpeed = abs2D(relativeV)
                    if relativeSpeed > 0:
                        maxMomentum = abs(g[1])*f*dty*self.mass
                        maxChangeTvC = maxMomentum/self.mass
                        maxChangeTvR = maxMomentum/(2/5*self.mass*self.radius)*self.radius/self.mass
                        maxChangeTv = maxChangeTvC + maxChangeTvR
                        newRV = max(0, relativeSpeed - maxChangeTv)
                        realChangeTv = relativeSpeed - newRV
                        momentum = realChangeTv*maxChangeTvC/maxChangeTv*self.mass

                        self.velocity[0] += signv*momentum
                        self.updateAngVelocity(cpoint, [-momentum*relativeV[0]/relativeSpeed, -momentum*relativeV[1]/relativeSpeed]) 
                    self.angVelocity += -sign(self.angVelocity)*min(abs(self.angVelocity), abs(g[1])*dty*fr/(2/5*self.mass*self.radius))


    def getBoundaryPointByAngle(self, angle):
        return [self.location[0] + math.cos(angle), self.location[1] - math.sin(angle)]

    def getBoundaryVelocity(self, radian):
        return [self.velocity[0] + self.angVelocity*self.radius*math.cos(radian + math.pi/2), 
                self.velocity[1] - self.angVelocity*self.radius*math.sin(radian + math.pi/2)]

        # location = [round(self.location[0]), round(self.location[1])]
        # pygame.draw.circle(surface, self.color, location, self.radius)


    def getGravityEnergy(self, masses, G):
        energy = 1/2*self.mass*(self.velocity[0]**2 + self.velocity[1]**2)
        for mass in masses:
            dis = math.sqrt((self.location[0] - mass.location[0])**2 + (self.location[1] - mass.location[1])**2)
            energy += -G*self.mass*mass.mass/dis
        self.energy = energy



    def updateGravity(self, surface, dt, masses, G):
        sizex, sizey = surface.get_size()
        dty = dt
        g = [0, 0]

        # calculate total g
        for mass in masses:
            dis = math.sqrt((self.location[0] - mass.location[0])**2 + (self.location[1] - mass.location[1])**2)
            gscale = G*self.mass*mass.mass/dis**2
            g1 = [gscale*(mass.location[0] - self.location[0])/dis, gscale*(mass.location[1] - self.location[1])/dis]
            g[0] += g1[0]
            g[1] += g1[1]

        
        # update location
        ds = self.velocity[1]*dty + 1/2*g[1]*dty**2

        self.location[1] = self.location[1] + ds
        self.velocity[1] = self.velocity[1] + dt*g[1]
        dtx = dt
        ds = self.velocity[0]*dtx + 1/2*g[0]*dtx**2
        self.location[0] = self.location[0] + ds
        self.velocity[0] = self.velocity[0] + dt*g[0]

        # midify velocity, according to energe
        energy = self.energy
        for mass in masses:
            dis = math.sqrt((self.location[0] - mass.location[0])**2 + (self.location[1] - mass.location[1])**2) 
            energy -= -G*self.mass*mass.mass/dis

        if energy > 0:
            svelocity = math.sqrt(2*energy/self.mass)
            curentVelocity = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
            if curentVelocity <= 0:
                self.velocity = [svelocity*(mass.location[0] - self.location[0]), svelocity*(mass.location[1] - self.location[1])]
            else:
                scale = svelocity/curentVelocity
                self.velocity = [self.velocity[0]*scale, self.velocity[1]*scale]

        # location = [round(self.location[0]), round(self.location[1])]
        # pygame.draw.circle(surface, self.color, location, self.radius)
        # print(g, self.velocity)