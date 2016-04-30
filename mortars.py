#!/usr/bin/python
'''
Kurt Gibbons - Physics 2425 Fall 2013 Presentation
FYI: some of the equations could be slightly off
'''

from visual import *
from visual.graph import *
from random import *

## Functions #### Functions #### Functions ##
def credit(Theta,wTheta, Vi,BLDG1,BLDG2) :
    print "Mortar Anatomy by Kurt Gibbons\n",
    print "For Physics 2425 Fall 2013 Class Presentation\n",
    print "Professor: Jason Eberle\n",
    print "North Lake Community College\n"
    print "Range     = (%.1f**2/g)*sin2(Theta) = %.1fm" % (Vi,Range(Vi))
    dX,dY,dZ = Distance(BLDG1,BLDG2)
    C = Pathagorean(dX,dY)
    print "Distances = X: %.1f Y: %.1f Z: %.1f" % (dX,dY,dZ)
    print "Total Distance Between Buildings = %.1f" % (C)
    bestTheta1,bestTheta2,InitVel,wV,ADT1,ADT2 = Solver(BLDG1, BLDG2, Vi, Theta, wTheta)
    print "Theta =  %.1f deg or %.1f deg" % (bestTheta1,bestTheta2)
    print "Initial Velocity = %.1f m/s" % (InitVel)
    print "Air Drag Initial Velocity = %.1f m/s" % (wV)
    print "Air Drag Theta =  %.1f deg or %.1f deg" % (ADT1,ADT2)
    
    
def MainWindow(X,Y,Z,Title,fgcolor,bgcolor) :
    #  Input: X,Y,Z (Range of view)
    # Output: playscene
    #Purpose: Position Main Window and size
    playscene=display(title=Title,
                  width=800,height=745,
                  x=600, y=0,
                  autoscale=0,
                  range=(X,Y,Z),
                  foreground=fgcolor,
                  background=bgcolor)
    playscene.autoscale = 0
    return playscene

def Floor(X,Y,Z,L,H,W,ColoR) :
    #  Input: X,Y,Z,L,H,W,Color (Length,Height,Width)
    # Output: Nothing
    #Purpose: Draw Floor
    box(pos = (X,Y,Z), size = (L,H,W), color = ColoR)

def Graphs(X,Y,W,H,Title,Xtitle,Ytitle,ColoR) :
    #  Input: PosX,PosY,Width,Height,Title,Xtitle,Ytitle
    # Output: gdisplay(), gdisplay.plot()
    #Purpose: Window position, graph titles, automake
    bgcolor = color.black
    fgcolor = color.white
    display = gdisplay(X, Y, W, H, 
             title=Title, xtitle=Xtitle, ytitle=Ytitle, 
             foreground=fgcolor, background=bgcolor)
    display_plot = gcurve(color=ColoR)

    return display, display_plot

def rectangle2stories(ColoR,GlobalW,GlobalY,GlobalZ,H,W,L,Zone) :
    #  Input: Color, Floor Y, Height, Width, Length, Zone
    # Output: Nothing
    #Purpose: Draw a building dynafloat(Vi**2)/G)*sin(2*ThetaRad)mically
    div = float(2)
    rightX,rightZ = (GlobalW/div)-(GlobalW/div/div/div/div), (GlobalZ/div)  #-(GlobalZ/div/div)
    leftX,leftZ = -rightX, -rightZ
    Lx,Wx = L-.5, W-.5
    rightPosX,rightLPosX,rightPosY = rightX+(L/div), leftX+(L/div), (GlobalY+L/div)
    leftPosX,leftLPosX,leftPosY = rightX-(L/div), leftX -(L/div), (GlobalY+L/div)
    bakPosY,bakPosZ,bakLPosZ = (GlobalY+L/div), rightZ-(W/div), leftZ-(W/div)
    frtPosY,frtPosZ,frtLPosZ  = (GlobalY+L/div), rightZ+(W/div), leftZ+(W/div)
    botPosY,topPosY  = GlobalY+H, GlobalY+L
    
    if Zone == 'right' :        # GREEN
        Floor1Rit = box(pos = (rightPosX,rightPosY,rightZ), size = (H,L,W), color = ColoR)
        Floor1Let = box(pos = (leftPosX,leftPosY,rightZ), size = (H,L,W), color = ColoR)
        Floor1Bak = box(pos = (rightX,bakPosY,bakPosZ), size = (L,L,H), color = ColoR)
        Floor1Frt = box(pos = (rightX,frtPosY,frtPosZ), size = (L,L,H), color = ColoR)
        Floor1Bot = box(pos = (rightX,botPosY,rightZ), size = (L,H,W), color = ColoR)
        Floor1Top = box(pos = (rightX,topPosY,rightZ), size = (L,H,W), color = ColoR)
        Floor2Top = box(pos = (Floor1Top.x,Floor1Top.y+Lx,Floor1Top.z), size = (Lx,H,Wx), color = ColoR)
        Floor2Rit = box(pos = (Floor2Top.x+(Lx/div),Floor2Top.y-(Lx/div),Floor1Rit.z), size = (H,Lx,Wx), color = ColoR)
        Floor2Let = box(pos = (Floor2Top.x-(Lx/div),Floor2Top.y-(Lx/div),Floor1Rit.z), size = (H,Lx,Wx), color = ColoR)
        Floor2Bak = box(pos = (Floor2Top.x,Floor2Top.y-(Lx/div),Floor1Rit.z-(Wx/div)), size = (Lx,Lx,H), color = ColoR)
        Floor2Frt = box(pos = (Floor2Top.x,Floor2Top.y-(Lx/div),Floor1Rit.z+(Wx/div)), size = (Lx,Lx,H), color = ColoR)
        return Floor2Top
         
    elif Zone == 'left' :       # RED
        Floor1Rit = box(pos = (rightLPosX,rightPosY,leftZ), size = (H,L,W), color = ColoR)
        Floor1Let = box(pos = (leftLPosX,leftPosY,leftZ), size = (H,L,W), color = ColoR)
        Floor1Bak = box(pos = (leftX,bakPosY,bakLPosZ), size = (L,L,H), color = ColoR)
        Floor1Frt = box(pos = (leftX,frtPosY,frtLPosZ), size = (L,L,H), color = ColoR)
        Floor1Bot = box(pos = (leftX,botPosY,leftZ), size = (L,H,W), color = ColoR)
        Floor1Top = box(pos = (leftX,topPosY,leftZ), size = (L,H,W), color = ColoR)
        Floor2Top = box(pos = (Floor1Top.x,Floor1Top.y+Lx,Floor1Top.z), size = (Lx,H,Wx), color = ColoR)
        Floor2Rit = box(pos = (Floor2Top.x+(Lx/div),Floor2Top.y-(Lx/div),Floor1Rit.z), size = (H,Lx,Wx), color = ColoR)
        Floor2Let = box(pos = (Floor2Top.x-(Lx/div),Floor2Top.y-(Lx/div),Floor1Rit.z), size = (H,Lx,Wx), color = ColoR)
        Floor2Bak = box(pos = (Floor2Top.x,Floor2Top.y-(Lx/div),Floor1Rit.z-(Wx/div)), size = (Lx,Lx,H), color = ColoR)
        Floor2Frt = box(pos = (Floor2Top.x,Floor2Top.y-(Lx/div),Floor1Rit.z+(Wx/div)), size = (Lx,Lx,H), color = ColoR)
        return Floor2Top

def ProjectileBall(r,X,Y,Z,BallColor,TrailColor,Vx,Vy,Vz,Ax,Ay,Az) : 
    #  Input: Radius, BallPos X,Y,Z, Colors, Vector Vx, Vy, Vz 
    # Output: ball, trail, velocity
    #Purpose: Create Ball
    bball = sphere(pos = (X,Y,Z), radius = r, color = BallColor)
    bball.trail = curve(color=TrailColor, retain = 1)
    bball.velocity = vector(Vx,Vy,Vz)
    bball.acceleration = vector(Ax,Ay,Az)
    return bball, bball.trail, bball.velocity, bball.acceleration

def BoxLabel( ColoR,X,Y,Vel,Pos,D,Title ) :
    #  Input: color, X & Y Position, Vel, Angle Init, Time, Distance, Title
    # Output: Label
    #Purpose: place info onto the float(Vi**2)/G)*sin(2*ThetaRad)screen 
    #Xlab,Y2lab,Vi,Theta,t,p2ball.pos.x-bldg2a.pos.x
    Label=label(color=ColoR,pos=(X,Y,0),box=true,font='monospace')
    Label.text=unicode('{%s} Velocity: X:%.1f Y:%.1f Z:%.1f m/s\n'
                        '\t\tPosition: X:%.1f Y:%.1f Z:%.1f m\n'
                        'Current Height: %.1fm Distance from Launch: %.1f m\n'
                        'Trajectory Y: %.1f deg'
                                %(Title,Vel[0],Vel[1],Vel[2],
                                Pos[0],Pos[1],Pos[2],
                                fabs(Pos[1]+(-floorPosY)),fabs(D),
                                Trajectory(Pos[0])),'utf-8')
    return Label

def BottomLabel( X,Y,Z,D,VelI,Angle,T ) :
    #  Input: X Y Z Position, Distance, Vel Initial, Angle Initial, Current Velocity
    # Output: Label
    #Purpose: place info onto the screen 
    #(bldg2a.pos.x-bldg1a.pos.x),-VelocityX,VelocityY,p2ball.velocity*dt*speed)
    Label=label(pos=(X,Y,Z),box=true,font='monospace')
    Label.text=unicode('Total Distance: %.1f m Initial Velocity: %.1f m/s \n'
                       'Launch Angle: %.1f deg  Range: %.1f Time %.1f sec' 
                       % (fabs(D),VelI,Angle,Range(VelI),T),'utf-8')
    return Label

def AllBottomLabel( X,Y,Z,D,VelI,Angle,wVi,wT,T ) :
    #  Input: X Y Z Position, Distance, Vel Initial, Angle Initial, Current Velocity
    # Output: Label
    #Purpose: place info onto the screen 
    #(bldg2a.pos.x-bldg1a.pos.x),-VelocityX,VelocityY,p2ball.velocity*dt*speed)
    Label=label(pos=(X,Y,Z),box=true,font='monospace')
    Label.text=unicode('Total Distance: %.1f m Initial Velocity w/o Wind: %.1f m/s \n'
                       'Launch Angle w/o Wind: %.1f deg  Range: %.1f \n'
                       'Initial Velocity w/ Wind: %.1f m/s \n'
                       'Launch Angle w/ Wind: %.1f deg  Range: %.1f \n'
                       'Time %.1f sec' 
                       % (fabs(D),VelI,Angle,Range(VelI),wVi,wT,Range(wVi),T),'utf-8')
    return Label

def Range(Vi) :
    #  Input: Cheating using Gloabal Variables 'oops
    # Output: Calculated Range
    #Purpose: Printout Range of Projectiles
    return (float(Vi**2)/G)*sin(2*ThetaRad)

def Trajectory(X) :
    #  Input: Cheating using Gloabal Variables 'oops
    # Output: Calculated Trajectory
    #Purpose: Printout Range of Projectiles
    return ( tan(ThetaRad)*X ) - ( float(G*(X**2)) / (2*(Vi*cos(ThetaRad))**2) )

def Distance(BLDG1, BLDG2) :
    #  Input: XYZ Positions
    # Output: XYZ Distances
    #Purpose: Get distances
    return fabs(BLDG1[0] - BLDG2[0]),fabs(BLDG1[1] - BLDG2[1]),fabs(BLDG1[2] - BLDG2[2])

def Pathagorean(X,Y) :
    #  Input: X & Y
    # Output: Hypotenus
    #Purpose: Caclulate hypotenus
    return sqrt(X**2+Y**2)

def Solver(pointA, pointB, Vi, Theta, wTheta):
    #  Input: bldg1 & bldg2 positions
    # Output: Correct Initial Velocity & Angle
    #Purpose: Solve for the correct Inputs
    dX,dY,dZ = Distance(pointA,pointB)
    C = Pathagorean(dX,dY)
    BestTheta1 = degrees((.5)*asin( (9.8*Range(Vi))/float(Vi**2) ))
    BestTheta2 = (180-BestTheta1) / 2
    InitialVelocity = sqrt( G*(float(C)/sin(2*radians(Theta))) )
    ADVi = sqrt( G*(float(C)/sin(2*radians(wTheta))) )
    ADTheta1 = degrees((.5)*asin( (9.8*Range(ADVi))/float(ADVi**2) ))
    ADTheta2 = (180-BestTheta1) / 2
    return BestTheta1, BestTheta2, InitialVelocity,ADVi,ADTheta1, ADTheta2
    
#~#~#~# Main #~#~#~# #~#~#~# Main #~#~#~# #~#~#~# Main #~#~#~#
#Projectile Variables
speed = 1               # Animation Speed ( 4 instant -- 1 slow )
dt = 0.025               # change in time 
G = 9.8                 # m/s**2
t = 0                   # Time
Vi = 51                 # m/s (Initial Velocity)        
Theta = 83.8
ThetaRad = radians(Theta)     # degrees (Launch Angle Theta)
Theta2 = ThetaRad
# Red Mortar
Direction1 = radians(1)  # Adjustment for aiming in degrees   
# Green Mortar
Direction2 = -Direction1 # Adjustment for aiming in degrees

VelocityX1 = Vi*cos(Theta2)
VelocityY1 = Vi*sin(Theta2)

VelocityX2 = Vi*cos(ThetaRad)
VelocityY2 = Vi*sin(ThetaRad)


m = 2.01                #0.145  # mass of 60mm is 2.01 kg, 120mm is 13.65 kg
A = 0.00421             # 
rho = 1.29              # density of air 1.2kg/m^3
C = 0.5                 # drag coefficient of mass
D = (rho*C*A)/2
g = vector(0,-9.8,0)    # gravity vector

# WIND MORTARS
# W = -3 #-3                  # m/s (negative towards screen, positive towards viewer)
# Wind = vector(0,0,W)    # wind vector
wVi = 51                # m/s (Initial Velocity)        
wTheta = 83.8
wThetaRad = radians(wTheta)     # degrees (Launch Angle Theta)
wVelocityX = wVi*cos(wThetaRad)
wVelocityY = wVi*sin(wThetaRad)
# Red Mortar
wDirection1 = radians(.5)  # Adjustment for aiming in degrees then rads
# Green Mortar
#wDirection2 = radians(-12) # Adjustment for aiming in degrees


# Screen Variables
width = .1              # width of elements
floorPosY = -20         # -10
floorW = 65
floorL = 25
# Create Scene
scene = MainWindow(floorL,floorW,floorW,'Mortar Anatomy Demonstration',color.white,color.black)
#scene.center = (25,-20,0)
Floor(0,floorPosY,0,floorW,width,floorL,color.yellow)

# objects
ran1,ran2 = randint(1, 9)+random(), randint(1, 9)+random()      # random bldg size
bldg1  = rectangle2stories(color.red,floorW,floorPosY,ran1,width,randint(3, 5),1,'left')
bldg1a = rectangle2stories(color.red,floorW,floorPosY,ran1,width,randint(1, 3),1+random(),'left')
bldg2  = rectangle2stories(color.green,floorW,floorPosY,ran2,width,randint(3, 5),1,'right')
bldg2a = rectangle2stories(color.green,floorW,floorPosY,ran2,width,randint(1, 3),1+random(),'right')

credit(Theta,wTheta,Vi,bldg1a.pos,bldg2a.pos)

# Projectile Graphs
gh,gw = 190, 570    # graph height, graph width
Mortar1Pos, Mortar1Pos_plot = Graphs(0,0,gw,gh,'Red Shooter Position','t(s)','x(m)',color.red)
Mortar1Graph, Mortar1Graph_plot = Graphs(0,185,gw,gh,'Red Shooter Position & Velocity','x(m)','v(m/s)',color.red)

Mortar2Pos, Mortar2Pos_plot = Graphs(0,370,gw,gh,'Green Shooter Position & Time','t(s)','x(m)',color.green)
Mortar2Graph, Mortar2Graph_plot = Graphs(0,570,gw,gh,'Green Shooter Position & Velocity','x(m)','v(m/s)',color.green)

# Presentation Objects
#  Input: Radius, BallPos X,Y,Z, Colors, Vector Vx, Vy, Vz 
p1ball,p1ball.trail,p1ball.velocity,p1ball.acceleration = ProjectileBall(.5,bldg1a.pos.x,bldg1a.pos.y,bldg1a.pos.z,
                                                                    color.red,color.blue,
                                                                    VelocityX1,VelocityY1,0,
                                                                    0,-G,0)
p2ball,p2ball.trail,p2ball.velocity,p2ball.acceleration = ProjectileBall(.5,bldg2a.pos.x,bldg2a.pos.y,bldg2a.pos.z,
                                                                    color.green,color.blue,
                                                                    -VelocityX2,VelocityY2,0,
                                                                    0,-G,0)
W1ball,W1ball.trail,W1ball.velocity,W1ball.acceleration = ProjectileBall(.5,bldg1a.pos.x,bldg1a.pos.y,bldg1a.pos.z,
                                                                                color.white,color.white,
                                                                                wVelocityX,wVelocityY,0,
                                                                                0,-G,0)
# W2ball,W2ball.trail,W2ball.velocity,W2ball.acceleration = ProjectileBall(.5,bldg2a.pos.x,bldg2a.pos.y,bldg2a.pos.z,
#                                                                                 color.white,color.white,
#                                                                                 wVelocityX,wVelocityY,0,
#                                                                                 0,-G,0)                                                                                

Xlab,Y1lab,Y2lab = -50,40,20    # Position of labels

PresentWith = 'Wind'        # Select to show Wind or not, All, Wind, NoWind
scene.mouse.getclick()      # wait for mouse click
    
if PresentWith == 'NoWind' :
    while (p2ball.pos.y and p1ball.pos.y) > (floorPosY + 1) :
        if scene.mouse.clicked:             # Control play with mouse click
            scene.mouse.getclick()
            scene.mouse.getclick()    
        rate(speed/dt)     
        t += dt
        # Red Mortar
        p1ball.pos += vector(0,0,Direction1)+p1ball.velocity*dt + 0.5 * p1ball.acceleration*dt**2
        p1ball.velocity += p1ball.acceleration*dt
        p1ball.acceleration = g
        p1ball.trail.append( pos = p1ball.pos )
        Mortar1Pos_plot.plot(pos =(t,p1ball.pos.y))
        Mortar1Graph_plot.plot(pos =(p1ball.velocity.y,p1ball.pos.y))
        M1Label = BoxLabel( color.red,Xlab,Y1lab,p1ball.velocity,
                            p1ball.pos,p1ball.pos.x-bldg1a.pos.x, 'Red Mortar' )
    
        # Green Mortar
        p2ball.pos += vector(0,0,Direction2)+p2ball.velocity*dt + 0.5 * p2ball.acceleration*dt**2
        p2ball.velocity += p2ball.acceleration*dt
        p2ball.acceleration = g
        p2ball.trail.append( pos = p2ball.pos )
        Mortar2Pos_plot.plot(pos =(t,p2ball.pos.y))
        Mortar2Graph_plot.plot(pos =(p2ball.velocity.y,p2ball.pos.y))
        M2Label = BoxLabel( color.green,Xlab,Y2lab,p2ball.velocity,
                            p2ball.pos,p2ball.pos.x-bldg2a.pos.x,'Green Mortar' )
        
        Readings = BottomLabel(-scene.range.x/4,-scene.range.y/2,0,(bldg1a.pos.x-bldg2a.pos.x),
                                Vi,Theta,t)

elif PresentWith == 'Wind' :
    while (W1ball.pos.y) > (floorPosY + 1) :
        if scene.mouse.clicked:             # Control play with mouse click
            scene.mouse.getclick()
            scene.mouse.getclick() 
        rate(speed/dt)     
        t += dt
        
        # Red Wind Mortar
        W1ball.pos += vector(0,0,wDirection1)+W1ball.velocity*dt + 0.5 * W1ball.acceleration*dt**2
        W1ball.velocity += W1ball.acceleration*dt
        W1ball.acceleration = g -(D/m)*mag(W1ball.velocity)*W1ball.velocity
        W1ball.trail.append( pos = W1ball.pos )
        Mortar1Pos_plot.plot(pos =(t,W1ball.pos.y))
        Mortar1Graph_plot.plot(pos =(W1ball.velocity.y,W1ball.pos.y))
        M1Label = BoxLabel( color.red,Xlab,Y1lab,W1ball.velocity,W1ball.pos,
                            W1ball.pos.x-bldg1a.pos.x, 'Red Wind Mortar' )
        
#         #Green Wind Mortar
#         W2ball.pos += vector(0,0,wDirection2)+W2ball.velocity*dt + 0.5 * W2ball.acceleration*dt**2
#         W2ball.velocity += W2ball.acceleration*dt
#         W2ball.acceleration = g*m -(D/m)*mag(W2ball.velocity)*W2ball.velocity + Wind
#         W2ball.trail.append( pos = W2ball.pos )
#         Mortar2Pos_plot.plot(pos =(t,W2ball.pos.y))
#         Mortar2Graph_plot.plot(pos =(W2ball.velocity.y,W2ball.pos.y))
#         M2Label = BoxLabel( color.green,Xlab,Y2lab,W2ball.velocity,W2ball.pos,
#                             W2ball.pos.x-bldg2a.pos.x, 'Green Wind Mortar' )
        
        Readings = BottomLabel(-scene.range.x/4,-scene.range.y/2,0,(bldg1a.pos.x-bldg2a.pos.x),
                                wVi,wTheta,t)
                                
elif PresentWith == 'All' :
    while (W1ball.pos.y and W2ball.pos.y and p2ball.pos.y and p1ball.pos.y) > (floorPosY + 1) :
        if scene.mouse.clicked:             # Control play with mouse click
            scene.mouse.getclick()
            scene.mouse.getclick() 
        rate(speed/dt)     
        t += dt
        
        # Red Mortar
        p1ball.pos += vector(0,0,Direction1)+p1ball.velocity*dt + 0.5 * p1ball.acceleration*dt**2
        p1ball.velocity += p1ball.acceleration*dt
        p1ball.acceleration = g
        p1ball.trail.append( pos = p1ball.pos )
        Mortar1Pos_plot.plot(pos =(t,p1ball.pos.y))
        Mortar1Graph_plot.plot(pos =(p1ball.velocity.y,p1ball.pos.y))

        # Green Mortar
        p2ball.pos += vector(0,0,Direction2)+p2ball.velocity*dt + 0.5 * p2ball.acceleration*dt**2
        p2ball.velocity += p2ball.acceleration*dt
        p2ball.acceleration = g
        p2ball.trail.append( pos = p2ball.pos )
    
        # Red Wind Mortar
        W1ball.pos += vector(0,0,wDirection1)+W1ball.velocity*dt + 0.5 * W1ball.acceleration*dt**2
        W1ball.velocity += W1ball.acceleration*dt
        W1ball.acceleration = g -(D/m)*mag(W1ball.velocity)*W1ball.velocity 
        W1ball.trail.append( pos = W1ball.pos )
        
#         #Green Wind Mortar
#         W2ball.pos += vector(0,0,wDirection2)+W2ball.velocity*dt + 0.5 * W2ball.acceleration*dt**2
#         W2ball.velocity += W2ball.acceleration*dt
#         W2ball.acceleration = g -(D/m)*mag(W2ball.velocity)*W2ball.velocity 
#         W2ball.trail.append( pos = W2ball.pos )
#         Mortar2Pos_plot.plot(pos =(t,W2ball.pos.y))
#         Mortar2Graph_plot.plot(pos =(W2ball.velocity.y,W2ball.pos.y))
       
        Readings = AllBottomLabel(-scene.range.x/4,-scene.range.y/2,0,(bldg1a.pos.x-bldg2a.pos.x),
                                Vi,Theta,wVi,wTheta,t)
