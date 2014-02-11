from visual import *

PI = math.pi
p = PI/180
earthRadius = 15036 

scene2 = display(title='Around the World in 80 Seconds',
     x=0, y=0, width=500, height=500,
     center=(5,0,0), background=(0,0,0))

def convertLatLong(startLat,startLong,endLat,endLong):
    #the following block of code converts latitude and longitude to xyz coordinates
    #have to correct this due to how the texture is mapped
    startLong = startLong + 90
    endLong = endLong + 90
    sLAT = p*startLat
    sLON = p*startLong
    eLAT = p*endLat
    eLON = p*endLong
    
    latxOrigin=-earthRadius*math.cos(sLAT)*math.cos(sLON)
    latyOrigin=earthRadius*math.sin(sLAT)
    latzOrigin=earthRadius*math.cos(sLAT)*math.sin(sLON)
    
    latxDest=-earthRadius*math.cos(eLAT)*math.cos(eLON)
    latyDest=earthRadius*math.sin(eLAT)
    latzDest=earthRadius*math.cos(eLAT)*math.sin(eLON)
    
    return [[latxOrigin,latyOrigin,latzOrigin],[latxDest,latyDest,latzDest]]

def normalVector(a,b):   
    #gets unit vector of origin
    dxO=a[0]/earthRadius #these three are the actual unit vectors. (dxO,dyO,dzO) = origin vector
    dyO=a[1]/earthRadius
    dzO=a[2]/earthRadius

    #gets unit vector of dest
    dxD=b[0]/earthRadius #these three are the actual unit vectors. (dxD,dyD,dzD) = destination vector
    dyD=b[1]/earthRadius
    dzD=b[2]/earthRadius

    cx=(dyO*dzD)-(dyD*dzO) #(cx,cy,cz) = cross product unit vector
    cy=(dxD*dzO)-(dxO*dzD)
    cz=(dxO*dyD)-(dxD*dyO)
    
    #without unit vectors
#     cx = (latyOrigin*latzDest)-(latzOrigin*latyDest);
#     cy = (latzOrigin*latxDest)-(latxOrigin*latzDest);
#     cz = (latxOrigin*latyDest)-(latyOrigin*latxDest);
    
    return [[dxO,dyO,dzO],[dxD,dyD,dzD],[cx,cy,cz]]

#     dxyz = (dxO*dxD)+(dyO*dyD)+(dzO*dzD) #dxyz = dot product scalar of origin and dest unit vectors
#     flightAngle=(1/p)*math.acos(dxyz) #angle in radians of distance between origin and dest

#     return [[latxOrigin,latyOrigin,latzOrigin],[latxDest,latyDest,latzDest],flightAngle,cx,cy,cz,dxyz]

def drawAirport(x,y,z):
    dot = sphere (pos=(x,y,z), radius=200, color = color.white)
    
def cross(a,b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c

def dot(a,b):
    c = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    flightAngle=(1/p)*math.acos(c)
    return [flightAngle,c]
    
def drawArc(cx, cy, cz, r, start_angle, arc_angle, num_segments,startLat,startLong,endLat,endLong,dotProduct):
    pathList = []
    theta = p*arc_angle / float(num_segments - 1) #theta is now calculated from the arc angle instead, the - 1 bit comes from the fact that the arc is open
    tangetial_factor = math.tan(theta)
    radial_factor = math.cos(theta)

    x = r * math.cos(p*start_angle) #we now start at the start angle
    y = r * math.sin(p*start_angle)
    
    oldN = [0,1,0]
    newN = [cx,cy,cz]
    rotationAxis = cross(oldN,newN)
    rotationAngle = math.acos(dotProduct)

    for ii in range(0, num_segments):
        coord = [x + cx, y + cy]
        pathList.append(coord)
        tx = -y; 
        ty = x;
        
        x += tx * tangetial_factor; 
        y += ty * tangetial_factor;
        
        x *= radial_factor; 
        y *= radial_factor;
        
        f = frame()
        path1 = curve(frame = f, pos=pathList, radius=50)
        f.rotate(angle=-PI/2, axis=[1,0,0], origin=scene2.center) #sets curve to x axis on equator
        f.rotate(angle=-PI/2, axis=[0,1,0], origin=scene2.center) #sets curve to begin at 0 longitude
        f.rotate(angle=radians(startLong), axis=[0,1,0], origin=scene2.center)
        f.rotate(angle=radians(startLat), axis=[rotationAxis[0],rotationAxis[1],rotationAxis[2]], origin=scene2.center) #this gets it to the correct plane
        
        rate(60) #updates every half second
#     while 1:
#         rate(30)
# #         f.rotate(angle=radians(-1), axis=[rotationAxis[0],rotationAxis[1],rotationAxis[2]], origin=scene2.center)
#         f.rotate(angle=radians(-1), axis=[cx,cy,cz], origin=scene2.center)

def main():
    ball = sphere (pos=(0,0,0), radius=earthRadius, material = materials.earth)
#     startLat = 41.90
#     startLong = -87.65
#     endLat = 51.51
#     endLong = -0.13
    startLat = 10
    startLong = -14
    endLat = 15
    endLong = 27
    airportCoords = convertLatLong(startLat,startLong,endLat,endLong) #converts starting lat and long to (x,y,z) coords
    drawAirport(airportCoords[0][0],airportCoords[0][1],airportCoords[0][2])
    drawAirport(airportCoords[1][0],airportCoords[1][1],airportCoords[1][2])
    journeyNormal = normalVector(airportCoords[0],airportCoords[1])
    flightAngle = dot(journeyNormal[0],journeyNormal[1])[0]
    dotProduct = dot(journeyNormal[0],journeyNormal[1])[1]
    journeyNormal = journeyNormal[2]
    drawAirport(1000*journeyNormal[0],1000*journeyNormal[1],1000*journeyNormal[2])
    drawAirport(0,0,0)
    path = drawArc(journeyNormal[0],journeyNormal[1],journeyNormal[2],15036,0,flightAngle,120,startLat,startLong,endLat,endLong,dotProduct)
    
if __name__ == "__main__":
    main()
