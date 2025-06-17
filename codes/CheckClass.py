#!/usr/bin/env python3
# .................................................... Class particle
class particle:
  color='red'
  # ............................................... Method __init__()
  def __init__(self,mass,x,y,vx,vy):
    self.m=mass
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.px=self.m*vx
    self.py=self.m*vy
    # ................................................. Method move()
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
# ................................................
pt1=particle(10,10,5,3.5,1.5)
pt2=particle(20,15,-4,-2.1,-2.2)
centerx=(pt1.m*pt1.x+pt2.m*pt2.x)/(pt1.m+pt2.m)
centery=(pt1.m*pt1.y+pt2.m*pt2.y)/(pt1.m+pt2.m)
print('momentum1 = ({:.1f},{:.1f})'.format(pt1.px,pt1.py))
print('momentum2 = ({:.1f},{:.1f})'.format(pt2.px,pt2.py))
print('center of mass = ({:.3f},{:.3f})'.format(centerx,centery))
print('color1 = ',pt1.color,', color2 = ',pt2.color)
print('initial position particle 1: ({:.3f},{:.3f})'.format(pt1.x,pt1.y))
pt1.move()
print('final position particle 1: ({:.3f},{:.3f})'.format(pt1.x,pt1.y))
print('Use of __dict__:')
print('pt1.__dict__: ',pt1.__dict__)
print('Keys of pt1 = ',pt1.__dict__.keys())
print('Values of pt1 = ',pt1.__dict__.values())
print('List of values of pt1 = ',list(pt1.__dict__.values()))
#print(particle.__dict__)


